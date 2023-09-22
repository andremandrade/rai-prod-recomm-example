import order_handler
from flask import Flask
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

# resp = api.exec(ctx, database, engine, all_orders_query(), readonly=True)
# show.results(resp)
# order_handler.handle_order(resp)