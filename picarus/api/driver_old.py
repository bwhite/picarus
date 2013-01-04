    def get_feature_hasher(self):  # TODO: Fix with model key
        return pickle.loads(self._get_feature_hasher())

    def _get_feature_hasher(self):  # TODO: Fix with model key
        out = self.hb.get(self.models_table, self.feature_hasher_row, self.feature_hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def get_masks_hasher(self):  # TODO: Fix with model key
        return pickle.loads(self._get_mask_hasher())

    def _get_mask_hasher(self):  # TODO: Fix with model key
        out = self.hb.get(self.models_table, self.masks_hasher_row, self.masks_hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def _get_feature_index(self):  # TODO: Fix with model key
        out = self.hb.get(self.models_table, self.feature_index_row, self.feature_index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

    def _get_masks_index(self):  # TODO: Fix with model key
        out = self.hb.get(self.models_table, self.masks_index_row, self.masks_index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value


    def evaluate_masks(self, cm_ilp):
        # Go through each mask and compare it to the annotation results
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[self.masks_gt_column])
        cms = {'train': np.zeros((self.texton_num_classes, self.texton_num_classes), dtype=np.int32),
               'test': np.zeros((self.texton_num_classes, self.texton_num_classes), dtype=np.int32)}
        ilps = []
        if cm_ilp:
            ilp_weights = json.load(open('ilp_weights.js'))  # load weights from previous run
            ilp_weights['ilp_tables'] = np.asfarray(ilp_weights['ilp_tables'])
        for row, columns in row_cols:
            gt = picarus.api.np_fromstring(columns[self.masks_gt_column])
            ilp_pred = np.fromstring(self.hb.get(self.images_table, row, self.feature_prediction_column)[0].value, dtype=np.double)[0]
            print(ilp_pred)
            masks = picarus.api.np_fromstring(self.hb.get(self.images_table, row, self.masks_column)[0].value)
            if cm_ilp:
                try:
                    bin_index = [x for x, y in enumerate(ilp_weights['bins']) if y >= ilp_pred][0]
                except IndexError:
                    bin_index = ilp_weights['ilp_tables'].shape[1]
                if bin_index != 0:
                    bin_index -= 1
                print('bin_index[%d][%f]' % (bin_index, ilp_pred))
                masks *= ilp_weights['ilp_tables'][:, bin_index]
            masks_argmax = np.argmax(masks, 2)
            gt_sums = np.sum(gt.reshape(-1, gt.shape[2]), 0).tolist()
            print(gt_sums)
            if row.startswith('sun397train'):
                cm = cms['train']
                ilps.append({'gt_sums': gt_sums, 'ilp_pred': ilp_pred, 'gt_size': gt.shape[0] * gt.shape[1]})
            else:
                cm = cms['test']
            for mask_num in range(gt.shape[2]):
                if not np.any(gt[:, :, mask_num]):
                    continue
                print(mask_num)
                preds = masks_argmax[gt[:, :, mask_num].nonzero()]
                h, bins = np.histogram(preds, np.arange(self.texton_num_classes + 1))
                np.testing.assert_equal(bins, np.arange(self.texton_num_classes + 1))
                cm[mask_num] += h
            json.dump({'cms': {'train': cms['train'].tolist(), 'test': cms['test'].tolist()}, 'cm_ilp': cm_ilp, 'ilps': ilps}, open('eval.js', 'w'))
            for split in ['train', 'test']:
                cm = cms[split]
                print(split)
                print(cm)
                if np.any(cm):
                    print(((cm / float(np.sum(cm))) * 100).astype(np.int32))
        classes = [z[1] for z in sorted([(y['mask_num'], x) for x, y in self.texton_classes.items()])]
        title_suffix = 'w ilp)' if cm_ilp else 'w/o ilp)'
        fn_suffix = '_ilp.png' if cm_ilp else '.png'
        save_confusion_matrix(cms['test'], classes, 'confmat_test' + fn_suffix, title='Confusion Matrix (test ' + title_suffix)
        save_confusion_matrix(cms['train'], classes, 'confmat_train' + fn_suffix, title='Confusion Matrix (train ' + title_suffix)

    def evaluate_masks_stats(self):
        data = json.load(open('eval.js'))
        ilps = data['ilps']
        class_ilps = [[] for x in range(self.texton_num_classes)]
        ilp_preds = []
        for x in ilps:
            for y, z in enumerate(np.array(x['gt_sums']) / float(x['gt_size'])):
                class_ilps[y].append((x['ilp_pred'], z))
            ilp_preds.append(x['ilp_pred'])
        for x in class_ilps:
            x.sort()

        # Make ilp bins (roughly equal # of items each)
        ilp_preds.sort()
        num_ilp_bins = 5
        elements_per_bin = int(np.round(len(ilp_preds) / num_ilp_bins))
        bins = []
        for x in range(num_ilp_bins + 1):
            bins.append(ilp_preds[x * elements_per_bin])

        mask_num_to_class = dict((y['mask_num'], x) for x, y in self.texton_classes.items())
        ilp_tables = []
        for y, x in enumerate(class_ilps):
            ilp_confs, class_probs = zip(*x)
            weighted_counts, bins2 = np.histogram(ilp_confs, bins, weights=class_probs)
            counts, bins3 = np.histogram(ilp_confs, bins)
            if y == 0:
                print 'bin_counts', counts
            ilp_tables.append((weighted_counts.astype(np.double) / counts).tolist())
            print mask_num_to_class[y], ilp_tables[-1]
        json.dump({'ilp_tables': ilp_tables, 'bins': bins}, open('ilp_weights.js', 'w'))
        print(len(ilps))
        print(ilps[0])

    def evaluate_nbnn(self):
        c = picarus.modules.LocalNBNNClassifier(10, 16, num_points=1000, scale=1)

        def inner(num_rows, **kw):
            row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                             columns=[self.image_column, self.indoor_class_column], **kw)
            for x, (_, cols) in enumerate(row_cols):
                print(repr(x))
                if x >= num_rows:
                    break
                yield cols[self.indoor_class_column], imfeat.image_fromstring(cols[self.image_column])
        c.train(inner(5000, start_row='sun397train'))
        cms = {}
        for cur_class, image in inner(40):
            pred_class = c.analyze(image)[0]['class']
            try:
                cms.setdefault(cur_class, {})[pred_class] += 1
            except KeyError:
                cms[cur_class][pred_class] = 1
            print cur_class, pred_class
        print(cms)




    def get_feature_classifier(self):  # TODO: Fix with model key
        cp = picarus.api.Classifier()
        cp.ParseFromString(self._get_feature_classifier())
        return cp

    def _get_feature_classifier(self):  # TODO: Fix with model key
        out = self.hb.get(self.models_table, self.feature_classifier_row, self.feature_classifier_column)
        if not out:
            raise ValueError('Classifier does not exist!')
        return out[0].value

    def build_masks_index(self):  # TODO: Fix with model key
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, 'masks')
        si.feature = pickle.dumps(self._get_texton())
        si.feature_format = si.PICKLE
        si.hash = self._get_mask_hasher()
        si.hash_format = si.PICKLE
        hasher = pickle.loads(si.hash)
        class_params = sorted(hasher.class_params.items(), key=lambda x: [0])
        weights = np.hstack([x[1]['w'] for x in class_params])
        index = image_search.LinearHashJaccardDB(weights)
        self._build_index(si, index, self.images_table, self.masks_hash_column, self.class_column, self.models_table, self.masks_index_row, self.masks_index_column)


    def masks_to_hash(self):  # TODO: Fix with model key
        self._feature_to_hash(self.get_masks_hasher(), self.images_table, self.masks_column, self.images_table, self.masks_hash_column)


    def masks_to_ilp(self, **kw):
        self._masks_to_ilp(self.images_table, self.masks_column, self.masks_ilp_column, **kw)

    def _masks_to_ilp(self, input_table, input_column, output_column, **kw):
        cmdenvs = {'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'hadoop/masks_to_ilp.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_column], single_value=True,
                             cmdenvs=cmdenvs, **kw)




        self.feature_dict = {'name': 'picarus._features.HOGBoVW', 'kw': {'clusters': json.load(open('clusters.js')), 'levels': 2, 'sbin': 16, 'blocks': 1}}
        self.feature_name = 'bovw_hog_levels2_sbin16_blocks1_clusters100'

    def image_to_masks(self):  # TODO: Fix with model key
        self._image_to_feature(self._get_texton(), self.images_table, self.image_column, self.images_table, self.masks_column)

    def image_to_superpixels(self):  # TODO: Fix with model key
        self._image_to_superpixels(self.images_table, self.image_column, self.images_table, self.superpixel_column)

    def _image_to_superpixels(self, input_table, input_column, output_table, output_column):  # Merge with above
        cmdenvs = {'HBASE_TABLE': output_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'hadoop/image_to_superpixels.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_column], single_value=True,
                             cmdenvs=cmdenvs, jobconfs={'mapred.task.timeout': '6000000'})

    def masks_to_hasher(self, **kw):  # TODO: Fix with model key
        hash_bits = 8
        hasher = image_search.HIKHasherGreedy(hash_bits=hash_bits)
        self._features_to_hasher(hasher, self.images_table, self.masks_column, self.models_table, self.masks_hasher_row, self.masks_hasher_column, **kw)


if 0:
    # OLD
    #feature_key = base64.b64decode('ZmVhdDrIeSo7m/TCXqJSzAMzahddGOZzow==')
    #hasher_key = 'hash:C\x95\x18\xfd\x8d5\x12\x0e\xb6\x96\xe4\xe0)+\x98%\xc1"\x1e8'
    #index_key = 'srch:\x1f\xf7\xbc\x9a;\xea8\x17\x12\x87X\xcb\t\x1a\x8aNxl\x9du'
    #image_retrieval.create_tables()
    #print image_retrieval.get_hasher()
    #print type(image_retrieval.get_hasher())
    #image_retrieval.image_thumbnail()
    #image_retrieval.image_resize()
    #image_retrieval._feature()
    #image_retrieval._masks()

    #image_retrieval._hash(start_row='sun397train')
    #image_retrieval._hashes()
    #image_retrieval._build_index(start_row='sun397train')

    #image_retrieval._learn_masks_hasher(start_row='sun397train')
    #image_retrieval._mask_hashes()
    #image_retrieval._build_mask_index()

    #image_retrieval.image_resize()
    #image_retrieval.image_thumbnail()
    #image_retrieval.annotation_masks_to_hbase()
    #image_retrieval.evaluate_nbnn()
    #image_retrieval.cluster_points_local(max_rows=1000)
    if 0:
        #image_retrieval.image_to_feature()
        image_retrieval.image_to_masks()
        #image_retrieval.features_to_hasher(start_row='sun397train', max_rows=1000)
        image_retrieval.masks_to_hasher(start_row='sun397train', max_rows=1000)
        #image_retrieval.feature_to_hash()
        image_retrieval.masks_to_hash()
        #image_retrieval.build_feature_index()
        image_retrieval.build_masks_index()
        #open('sun397_feature_index.pb', 'w').write(image_retrieval._get_feature_index())
        open('sun397_masks_index.pb', 'w').write(image_retrieval._get_masks_index())
        # Classifier
        #image_retrieval.features_to_classifier(start_row='sun397train', max_per_label=5000)
        #open('sun397_indoor_classifier.pb', 'w').write(image_retrieval._get_feature_classifier())
        #image_retrieval.feature_to_prediction()
        #image_retrieval.prediction_to_conf_gt(stop_row='sun397train')
    #image_retrieval.image_to_superpixels()
    #image_retrieval.masks_to_ilp()
    #image_retrieval.evaluate_masks(False)
    #image_retrieval.evaluate_masks_stats()
