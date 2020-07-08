# Landmatrix API Documentation

The Landmatrix API is available at [https://dev.landmatrix.org/graphql/](https://dev.landmatrix.org/graphql/) and provides **deal** as well as **investor** data sets.
The API requires you to write your queries in [GraphQL syntax](https://graphql.org/learn/) and returns the matching data sets as a [JSON](https://www.json.org/json-en.html) formatted response.


### Data types and fields
#### Deals
_A deal is an transaction associated with a particular piece of land or area._

The deal data schema including all available fields can be found in the `Schema` section at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/).

#### Investors
_Investors are people or associations who or which are associated with a land deal._

The Investor data schema including all available fields can be found in the `Schema` section at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/).


### Query examples

#### Deal data by ID

If you want to receive a specific deal by ID you can pass the ID as an argument to the query. In this case you are querying for the data type `deal`.
```
{
  deal(id: 3) {
    geojson
  }
}
```
will return
```
{
  "data": {
    "deal": {
      "geojson": {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [
                93.98784269999999,
                19.810093
              ]
            },
            "properties": {
              "name": "Rakhine, Myanmar",
              "type": "point"
            }
          }
        ]
      }
    }
  }
}
```

_Deal IDs can for example be found [in the data section](https://landmatrix.org/data/) of the Landmatrix web application._

#### All deal data

Data on all deals available can be recieved by querying for `deals`.
```
# This will return data of the first 5 deals (ordered by ID).
{
  deals(limit: 5) {
    id
    country
    geojson
  }
}
```

#### Investor data by ID

To find a specific investor by ID simply pass the ID to the `investor` query:
```
{
  investor(id: 1010) {
    id
    name
    country {
      name
    }
  }
}
```
is going to return
```
{
  "data": {
    "investor": {
      "id": 1010,
      "name": "I.D.C Investment",
      "country": {
        "name": "Denmark"
      }
    }
  }
}
```

#### All investor data

Analogous to the deals, data on multiple investors can be queried with the `investors` query.
```
# This will return `id` and `name` of the first 5 investors ordered ascending by ID.
{
  investors(limit: 5) {
    id
    name
  }
}
```



### Filters

In most use cases you may want to specify some fields and conditions you want to have your query results filtered by.
You can pass a `filter` array to your query as an argument.

#### Filter examples

If you want to apply a filter you can directly incorporate the filter array into your query like this:
```
{
  deals(filters: { field: "timestamp", operation: GE, value: "2020-03-02" }) {
    id
    deal_size
  }
}
```

You can also chain multiple filters by combining them into a filter array.
The filters will be logically combined with an `AND` operator.

```
{
  deals(
    filters: [
      { field: "timestamp", operation: GE, value: "2010-03-02" }
      { field: "target_country.name", operation: EQ, value: "Myanmar" }
    ]
  ) {
    id
    target_country {
      id
      name
    }
  }
}
```
Note that you can filter on subfields like e.g. `target_country.name` by chaining them with a `.`.

If you want to create a logical `OR` filter on a specific field you can use the `IN` operator in combination with an array of values:
```
{
  deals(
    filters: [
      { field: "target_country.name", operation: IN, value: ["Myanmar", "Bangladesh"] }
    ]
  ) {
    id
    deal_size
  }
}
```


#### Logical operators

Available logical operators are:

* `EQ`: equals
* `IN`: in/part of
* `CONTAINS`: contains
* `LT`: less than
* `LE`: less or equal than
* `GT`: greater than
* `GE`: greater or equal than
