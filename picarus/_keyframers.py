import keyframe

def select_keyframer(keyframer_name):
    return {'decision_tree': keyframe.DecisionTree,
            'surf': keyframe.SURF,
            'uniform': keyframe.Uniform,
            'histogram': keyframe.Histogram}[keyframer_name]
    
