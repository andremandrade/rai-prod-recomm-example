# Show products_csv base relation

## Basics

### Base relations

#### Insert cars

```rel
def new_cars = 
    :id    , 1, 1;
    :name  , 1, "Honda CR-V";
    :price , 1, 30825.00
def new_cars = 
    :id    , 2, 2;
    :name  , 2, "Toyota RAV4";
    :price , 2, 29610.00

def insert:cars = new_cars
```

#### Check cars

```rel
def output = cars:price
```

#### Delete all cars

```rel
def delete:cars = cars
````

### Derived relations

```rel
def sum_car_prices = sum[cars:price]

def output  = sum_car_prices
```

### Models

Install [car.rel](../model/basics/car.rel) model

#### Check the installed model

```rel
def output = sum_car_prices
```

## Columnar

```rel
def output = products_csv:Price

def output = first[products_csv]
```

## Tabled

```rel
def output = products_csv
```

## Convert types

```rel
def output:parse_int = row, id : parse_int[id], products_csv:ID(row, id)

def output:parse_float = row, price : parse_float[price], products_csv:Price(row, price)

def output:parse_date = pos, bd: parse_date[bd, "Y-m-d"], users_json[_](pos, :Birthday, bd)
```

## Show products derived relation

```rel
def output = products
```

## Show users_csv

```rel
def output:users_json = users_json[_]
def output:users_json_gnf = attr, pos, val : users_json[_](pos, attr, val)
```

### Show order

```rel
def result = attr in {:id; :date}, o : orders[attr, o]
def result = :products, o, attr, p : products[attr, p], orders:products(o, p)
def result = :user, o, attr, u : users[attr, u], orders:user(o, u)
def output = result:date
```

### Graph of users interests

```rel
def output = graphviz[interest_graph]
```

### Show similarity

```rel
def output = recommendation:product_by_id[10]
```
