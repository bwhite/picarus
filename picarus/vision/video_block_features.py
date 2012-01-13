#!/usr/bin/env python
import hadoopy
import tempfile
import cStringIO as StringIO
import Image
import vidfeat
import pyffmpeg
import keyframe
import imfeat
import numpy as np
import os
import cv
import distpy
import sys
import impoint


def shot_map(features):
    """
    Args:
        features: Video level features (see map input)

    Returns:
        Dict of intermediate features
    """
    keyframe_clusters = np.asfarray([24, 269, 3469, 94, 844])
    keyframe_clusters = keyframe_clusters.reshape((keyframe_clusters.size, 1))
    num_transitions = 0
    prev_keyframe = None
    shot_lens = []
    bo_shot_lengths = np.zeros(len(keyframe_clusters))
    d = distpy.L2Sqr()
    keyframes = [(x['frame_num'], x['frame_time'], x['keyframe']) for x in features['frame_features']]
    for frame_num, frame_time, iskeyframe in keyframes:
        num_transitions += int(iskeyframe)
        if iskeyframe:
            if prev_keyframe is not None:
                shot_lens.append(frame_num - prev_keyframe)
                bo_shot_lengths[d.nn(keyframe_clusters, np.asfarray([shot_lens[-1]]))[1]] += 1
            prev_keyframe = frame_num
    return {'shot_lengths': shot_lens, 'num_transitions': num_transitions,
            'bo_shot_lengths': bo_shot_lengths, 'num_frames': len(keyframes)}


def shot_reduce(features):
    """
    Args:
        features: List of results of the keyframe_map

    Returns:
        Numpy array of features
    """
    shot_lengths = []
    num_transitions = 0
    num_frames = 0
    bo_shot_lengths = 0
    for feature in features:
        shot_lengths += feature['shot_lengths']
        num_transitions += feature['num_transitions']
        bo_shot_lengths += feature['bo_shot_lengths']
        num_frames += feature['num_frames']
    sys.stderr.write('NumKeyframes: %d\n' % (num_transitions))
    min_len = np.min(shot_lengths) if shot_lengths else 0
    med_len = np.median(shot_lengths) if shot_lengths else 0
    max_len = np.max(shot_lengths) if shot_lengths else 0
    std_len = np.std(shot_lengths) if shot_lengths else 0
    if shot_lengths:
        bo_shot_lengths /= len(shot_lengths)
    return {'shot_trans_per_duration': float(num_transitions) / float(num_frames), 'shot_min_length': min_len,
            'shot_median_length': med_len, 'shot_max_length': max_len, 'shot_std_length': std_len, 'shot_bo_length': bo_shot_lengths}


def face_map(features):
    face_clusters = np.asfarray([0.21785626, 0.50042658, 0.2856845, 0.37226103, 0.15279431])
    face_clusters = face_clusters.reshape((face_clusters.size, 1))
    d = distpy.L2Sqr()
    bo_face_widths = np.zeros(len(face_clusters))
    print(features['frame_features'][0].keys())
    face_widths = [(x['face_widths'].tolist() if 'face_widths' in x else []) for x in features['frame_features']]
    print(len(face_widths))
    for frame_face_widths in face_widths:
        for w in frame_face_widths:
            bo_face_widths[d.nn(face_clusters, np.asfarray([w]))[1]] += 1
    return {'bo_face_widths': bo_face_widths, 'face_widths': face_widths}


def face_reduce(features):
    """
    Args:
        features: List of results of the keyframe_map

    Returns:
        Numpy array of features
    """
    bo_face_widths = 0
    face_widths = []
    for feature in features:
        bo_face_widths += feature['bo_face_widths']
        face_widths += feature['face_widths']
    num_faces = np.array(map(len, face_widths))
    face_width = np.nan_to_num(np.median(sum(face_widths, [])))
    return {'face_max_frame': np.max(num_faces), 'face_mean_frame': np.mean(num_faces), 'face_median_width': face_width, 'face_bo_width': bo_face_widths}


def scene_map(features):
    preds = [x['predictions']['indoors'] for x in features['frame_features']]
    out = []
    for p in preds:
        out.append(p[0][0] * p[0][1])
    return {'indoors': out}


def scene_reduce(features):
    """
    Args:
        features: List of results of the keyframe_map

    Returns:
        Numpy array of features
    """
    return {'scene_indoors': np.nan_to_num(np.median(sum([f['indoors'] for f in features], [])))}


def camera_map(features):
    med_dists = []
    for frame_feat0, frame_feat1 in zip(features['frame_features'], features['frame_features'][1:]):
        surf0, surf1 = frame_feat0['surf'], frame_feat1['surf']
        surf_inst = impoint.SURF()
        matches = surf_inst.match(surf0, surf1)
        if 30 < len(matches) and 10 < min(len(surf0), len(surf1)):
            pairs = [np.asfarray([surf0[x]['x'] - surf1[y]['x'], surf0[x]['y'] - surf1[y]['y']]) for x, y in matches]
            dists = [np.linalg.norm(x) for x in pairs]
            med_dists.append(np.nan_to_num(np.median(dists)))
    sys.stderr.write('Med_dists: %d\n' % len(med_dists))
    return {'med_dists': med_dists}


def camera_reduce(features, full_features):
    """
    Args:
        features: List of results of the keyframe_map

    Returns:
        Numpy array of features
    """
    med_dists = np.asfarray(sum([x['med_dists'] for x in features], []))
    return {'camera_std_frame_median_distance': np.std(med_dists),
            'camera_std_frame_mean_distance': np.mean(med_dists),
            'camera_matches_per_duration': med_dists.size / float(full_features[0]['duration'])}


class Mapper(object):

    def __init__(self):
        pass

    def map(self, event_filename, features):
        """

        Args:
            event_filename: A tuple in the form of (event, filename)
            features: Dictionary of

            frame_features: List of dictionaries of features (frame level)
            file_size: Size in bytes
            duration: Duration in seconds

            where each frame feature is a dictionary of

            frame_time: Time in seconds
            frame_num: Frame number
            prev_frame_num: Previous frame number (useful if there is a frame skip)
            keyframe: Boolean True/False
            surf: List of surf points (see impoint)
            face_widths:
            face_heights:
            predictions: Dictionary of predictions

        Yields:
            A tuple in the form of (feature_name, features)
            event_filename: Name of the feature
            features: Partial features
        """
        sys.stderr.write('%s\n' % str(event_filename))
        s = np.array([features['file_size']], dtype=np.float64)
        try:
            t = features['duration']
        except KeyError:
            try:
                t = features['frame_features'][0]['duration']
            except IndexError:
                return
        out = {'faces': face_map(features),
               'shots': shot_map(features),
               'scene': scene_map(features),
               'camera': camera_map(features),
               'duration': t,
               'file_size': s}
        yield event_filename, out


def basic_reduce(features):
    t = features[0]['duration']
    s = float(features[0]['file_size'])
    return {'basic_file_size': s, 'basic_bytes_per_sec': t / s, 'basic_duration': t}


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, event_filename, features):
        """

        Args:
            event_filename: Name of the feature
            features: Partial features

        Yields:
            A tuple in the form of (event_filename, features)
            event_filename: Name of the feature
            features: Partial features
        """
        features = list(features)
        out_feat = {}
        out_feat.update(basic_reduce(features))
        out_feat.update(face_reduce([x['faces'] for x in features]))
        out_feat.update(shot_reduce([x['shots'] for x in features]))
        out_feat.update(camera_reduce([x['camera'] for x in features], features))
        out_feat.update(scene_reduce([x['scene'] for x in features]))
        yield (event_filename[0], event_filename[1]), out_feat


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
