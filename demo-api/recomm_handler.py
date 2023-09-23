from railib import api
import json

def handle_recommendation(trxResponse : api.TransactionAsyncResponse):
    recommendations = []
    for r in trxResponse.results:
        relation = r['relationId']
        table = r['table']
        if str.startswith(relation, '/:output/:id'):
            for i in range(table.num_rows):
                recomm = find_recomm_by_hash(table[0][i], recommendations)
                recomm['id'] = table[1][i].as_py()
        if str.startswith(relation, '/:output/:name'):
            for i in range(table.num_rows):
                recomm = find_recomm_by_hash(table[0][i], recommendations)
                recomm['name'] = table[1][i].as_py()
        if str.startswith(relation, '/:output/:similarity'):
            for i in range(table.num_rows):
                recomm = find_recomm_by_hash(table[0][i], recommendations)
                recomm['similarity'] = table[1][i].as_py()

    for recomm in recommendations:
        recomm.pop('hash', None)
        print(json.dumps(recomm, indent=4, sort_keys=True))
        
    return recommendations

def find_recomm_by_hash(raw_hash, orders):
    hash = raw_hash[0].as_py() + raw_hash[1].as_py()
    for o in orders:
        if o['hash'] == hash:
            return o
    order = { 'hash': hash }
    orders.append(order)
    return order
