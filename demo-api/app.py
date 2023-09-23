import order_handler
import recomm_handler
from flask import Flask, request
from railib import api, config, show

app = Flask(__name__)

database = "andre-ise23-demo1"
engine = "andre-ise-s"

cfg = config.read(profile="sales-team")
ctx = api.Context(**cfg)

@app.route("/api/order")
def get_order():
    resp = api.exec(ctx, database, engine, all_orders_query(), readonly=True)
    return order_handler.handle_order(resp)

def all_orders_query():
    return """
    //beginrel
    def result = attr in {:id; :date}, o : orders[attr, o]
    def result = :products, o, attr, p : products[attr, p], orders:products(o, p)
    def result = :user, o, attr, u : users[attr, u], orders:user(o, u)
    def output = result
    //endrel
    """
    
@app.route("/api/recommendation")
def get_recommendation():
    args = request.args
    prod_id = args.get('prod_id')
    resp = api.exec(ctx, database, engine, 
                    recommendation_query(prod_id), readonly=True)
    return recomm_handler.handle_recommendation(resp)

def recommendation_query(prod_id):
    return f"""
    //beginrel
    def output = recommendation:product_by_id[{prod_id}]
    //endrel
    """