def register_frames(row):
    import tempfile
    import viderator
    import cv2
    import distpy
    import time
    hamming = distpy.Hamming()
    thrift = hadoopy_hbase.connect()
    fp = tempfile.NamedTemporaryFile()

    def get_column(column):
        return thrift.getRowWithColumns('videos', row,
                                        [column])[0].columns[column].value
    video_chunks = int(get_column('meta:video_chunks'))
    for x in range(video_chunks):
        fp.write(get_column('data:video-%d' % x))
    fp.flush()
    brisk = cv2.BRISK(40, 4, 1.)  # TODO: Get from model
    mask = None
    prev_descs = None
    prev_points = None
    match_thresh = 75
    min_inliers = 10
    frames_matched = []
    for frame_num, frame_time, frame in viderator.frame_iter(fp.name, frame_skip=3):
        matched = False
        st = time.time()
        if mask is None:
            mask = np.ones((frame.shape[0], frame.shape[1]))
        points, descs = brisk.detectAndCompute(frame, mask)
        points = np.array([x.pt for x in points])
        #print((frame_num, points, descs))
        if prev_descs is not None:
            matches = (hamming.cdist(prev_descs, descs) < match_thresh).nonzero()
            print(matches)
            a = np.array(prev_points[matches[0], :], dtype=np.float32)
            b = np.array(points[matches[1], :], dtype=np.float32)
            #print(a)
            #print(b)
            if a.shape[0] >= min_inliers and b.shape[0] >= min_inliers:
                h, i = cv2.findHomography(a, b, cv2.RANSAC)
                if np.sum(i) >= min_inliers:
                    matched = True
                print((h, i))
        frames_matched.append(matched)
        prev_descs = descs
        prev_points = points
        print(time.time() - st)
    print(matched)

class VideosHBaseTable(DataHBaseTable):

    def __init__(self, _auth_user):
        super(VideosHBaseTable, self).__init__(_auth_user, 'videos')

    def _column_write_validate(self, column):
        if column.startswith('data:video-'):
            return
        if column.startswith('meta:'):
            return
        bottle.abort(403)

    def post_row(self, row, params, files):
        action = params['action']
        with thrift_lock() as thrift:
            manager = PicarusManager(thrift=thrift)
            print(params)
            # TODO: Allow io/ so that we can write back to the image too
            if action == 'i/register/sequential':
                self._row_validate(row, 'r')
                register_frames(row)
                return {}

#    elif table == 'videos':
#        return VideosHBaseTable(_auth_user)
