            elif action == 'io/garbage':
                self._slice_validate(start_row, stop_row, 'rw')
                columns_removed = set()
                columns_kept = set()
                # TODO: Update these to use the new job system
                # TODO: Get all user models and save those too
                
                active_models = set()
                for cur_row, cur_cols in thrift.scanner(self.table,
                                                        start_row=start_row,
                                                        stop_row=stop_row, keys_only=True):
                    for k in cur_cols.keys():
                        if not (k.startswith('meta:') or k.startswith('thum:') or k == 'data:image' or k in active_models):
                            if k not in columns_removed:
                                columns_removed.add(k)
                                print(columns_removed)
                                print(len(columns_removed))
                        else:
                            if k not in columns_kept:
                                columns_kept.add(k)
                                print(columns_kept)
                                print(len(columns_kept))
                return {'columnsRemoved': list(columns_removed), 'columnsKept': list(columns_kept)}
            elif action == 'i/dedupe/identical':
                self._slice_validate(start_row, stop_row, 'r')
                # TODO: Update these to use the new job system
                col = params['column']
                features = {}
                dedupe_feature = lambda x, y: features.setdefault(base64.b64encode(hashlib.md5(y).digest()), []).append(base64.b64encode(x))
                for cur_row, cur_columns in thrift.scanner(self.table, columns=[col],
                                                           start_row=start_row, per_call=10,
                                                           stop_row=stop_row):
                    dedupe_feature(cur_row, cur_columns[col])
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps([{'rows': y} for x, y in features.items() if len(y) > 1])
