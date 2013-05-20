            elif action == 'i/faces':
                # TODO: Temporary, remove when done
                names = set(['George_W_Bush', 'Colin_Powell', 'Tony_Blair', 'Donald_Rumsfeld', 'Gerhard_Schroeder',
                             'Ariel_Sharon', 'Hugo_Chavez', 'Junichiro_Koizumi', 'Serena_Williams', 'John_Ashcroft'])
                self._slice_validate(start_row, stop_row, 'r')
                import cv2
                r = None
                labels = {}
                pos = 0
                neg = 0
                data = []
                lab = []
                num_train = 2000
                for n, (cur_row, cur_cols) in enumerate(hadoopy_hbase.scanner(thrift, self.table,
                                                                              start_row=start_row, per_call=10,
                                                                              stop_row=stop_row, columns=['data:image', 'meta:class'])):
                    cur_class = cur_cols['meta:class']
                    if cur_class not in names:
                        continue
                    if cur_class not in labels:
                        labels[cur_class] = len(labels)
                    label = labels[cur_class]
                    image = cv2.imdecode(np.fromstring(cur_cols['data:image'], np.uint8), 0)
                    # Crop
                    image = np.ascontiguousarray(image[62:-62, 62:-62])
                    #if n == 0:
                    #    cv2.imwrite('out.png', image)
                    if n < num_train:
                        lab.append(label)
                        data.append(image)
                    else:
                        if r is None:
                            r = cv2.createLBPHFaceRecognizer()
                            r.train(data, np.array(lab))
                            print('TRAINED-----------------------')
                        pred = r.predict(image)[0]
                        print((pred, label))
                        if pred == label:
                            pos += 1
                        else:
                            neg += 1
                    print((cur_class, image.shape, n, pos, neg, pos / float(pos + neg + .00000001)))
