from railib import api
import json

def handle_order(trxResponse : api.TransactionAsyncResponse):
    orders = []
    for r in trxResponse.results:
        relation = r['relationId']
        if str.startswith(relation, '/:output/:date'):
            table = r['table']
            for i in range(table.num_rows):
                order = find_order_by_hash(table[0][i], orders)
                order['date'] = table[1][i].as_py()

        if str.startswith(relation, '/:output/:id'):
            table = r['table']
            for i in range(table.num_rows):
                order = find_order_by_hash(table[0][i], orders)
                order['id'] = table[1][i].as_py()

        if str.startswith(relation, '/:output/:products'):
            table = r['table']
            for i in range(table.num_rows):
                order = find_order_by_hash(table[0][i], orders)
                product = find_prod_by_hash(table[1][i], order)
                if str.startswith(relation, '/:output/:products/HashValue/:category'):
                    product['category'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:products/HashValue/:description'):
                    product['description'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:products/HashValue/:id'):
                    product['id'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:products/HashValue/:name'):
                    product['name'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:products/HashValue/:price'):
                    product['price'] = table[2][i].as_py()
        if str.startswith(relation, '/:output/:user'):
            table = r['table']
            for i in range(table.num_rows):
                order = find_order_by_hash(table[0][i], orders)
                user = get_order_user_by_hash(table[1][i], order)
                if str.startswith(relation, '/:output/:user/HashValue/:birthday'):
                    user['birthday'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:user/HashValue/:firstname'):
                    user['firstname'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:user/HashValue/:id'):
                    user['id'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:user/HashValue/:lastname'):
                    user['lastname'] = table[2][i].as_py()
                if str.startswith(relation, '/:output/:user/HashValue/:username'):
                    user['username'] = table[2][i].as_py()
    
    # pop 'hash' from each order and product
    for o in orders:
        o.pop('hash', None)
        for p in o['products']:
            p.pop('hash', None)
        o['user'].pop('hash', None)
        # print pretty json
        print(json.dumps(o, indent=4, sort_keys=True))
        
    return orders

def find_order_by_hash(raw_hash, orders):
    hash = raw_hash[0].as_py() + raw_hash[1].as_py()
    for o in orders:
        if o['hash'] == hash:
            return o
    order = { 'hash': hash }
    orders.append(order)
    return order

def find_prod_by_hash(raw_hash, order):
    hash = raw_hash[0].as_py() + raw_hash[1].as_py()
    if 'products' not in order:
        order['products'] = []
    for p in order['products']:
        if p['hash'] == hash:
            return p
    product = { 'hash': hash }
    order['products'].append(product)
    return product

def get_order_user_by_hash(raw_hash, order):
    hash = raw_hash[0].as_py() + raw_hash[1].as_py()
    if 'user' not in order:
        order['user'] = {'hash': hash}
    return order['user']