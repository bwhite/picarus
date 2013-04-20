import hadoopy_hbase
import base64
import json

a = hadoopy_hbase.connect()
for row, columns in hadoopy_hbase.scanner(a, 'models', columns=['meta:']):
    print(row)
    print(columns)
    continue
    columns_out = {}
    # Store input in binary instead of ub64
    columns_out['meta:input'] = base64.urlsafe_b64decode(columns['meta:input'])
    try:
        fi = json.loads(columns['meta:factory_info'])
        # Make inputs binary and not ub64
        fi['inputs'] = {x: base64.b64encode(base64.urlsafe_b64decode(str(y)))
                        for x, y in fi['inputs'].items()}
        # Make slices encoded using commas and b64 instead of / and ub64
        fi['slices'] = [','.join([base64.b64encode(base64.urlsafe_b64decode(y))
                                  for y in str(x).split('/')])
                        for x in fi['slices']]
        columns_out['meta:factory_info'] = json.dumps(fi)
    except KeyError:
        pass
    print(columns_out)
    mutations = []
    for x, y in columns_out.items():
        mutations.append(hadoopy_hbase.Mutation(column=x, value=y))
    #a.mutateRow('models', row, mutations)
