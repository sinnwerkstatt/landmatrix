# Landmatrix API Documentation

The Landmatrix API is available at [https://landmatrix.org/graphql/](https://landmatrix.org/graphql/)
and provides **deal** as well as **investor** data sets.
The API requires you to write your queries in [GraphQL syntax](https://graphql.org/learn/)
and returns the matching data sets as a [JSON](https://www.json.org/json-en.html) formatted response.


## Data types and fields
### Deals
_A deal is a transaction associated with a particular piece of land or area._

The deal data schema including all available fields can be found in the `Schema`
section at [landmatrix.org/graphql/](https://landmatrix.org/graphql/).

### Investors
_Investors are entities or associations which are associated with a land deal._

The Investor data schema including all available fields can be found in the `Schema`
section at [landmatrix.org/graphql/](https://landmatrix.org/graphql/).

## Query examples

### Deal by ID

If you want to receive a specific deal by ID you can pass the ID as an argument to the
query. In this case you are querying for the data type `deal`.
```graphql
{
  deal(id: 4) {
    id
    current_intention_of_investment
    current_negotiation_status
    geojson
  }
}
```
will return
```json
{
  "data": {
    "deal": {
      "id": 4,
      "current_intention_of_investment": [
        "LIVESTOCK"
      ],
      "current_negotiation_status": "ORAL_AGREEMENT",
      "geojson": {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [
                91.10173340000006,
                22.8246384
              ]
            },
            "properties": {
              "id": 9811,
              "name": "Noakhali, Bangladesh",
              "type": "point",
              "spatial_accuracy": "ADMINISTRATIVE_REGION"
            }
          }
        ]
      }
    }
  }
}
```

_Deal IDs can be found [in the data section](https://landmatrix.org/list/deals/) of
the Land Matrix._

### Multiple Deals

Data on all deals available can be recieved by querying for `deals`.
```graphql
# This will return data of the first 5 deals (ordered by ID).
{
  deals(limit: 5) {
    id
    country {
      id
      name
    }
    geojson
  }
}
```

### Investor by ID

To find a specific investor by ID simply pass the ID to the `investor` query:
```graphql
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
```json
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

### Multiple investors

Analogous to the deals, data on multiple investors can be queried with the `investors`
query.

```graphql
# This will return "id" and "name" of the first 5 investors ordered ascending by ID.
{
  investors(limit: 5) {
    id
    name
  }
}
```



## Filters

In most use cases you may want to specify some fields and conditions you want to have
your query results filtered by.
You can pass a `filter` array to your query as an argument.

### Filter examples

If you want to apply a filter you can directly incorporate the filter array into your
query like this:
```graphql
{
  deals(filters: { field: "created_at", operation: GE, value: "2020-03-02" }) {
    id
    deal_size
  }
}
```

You can also chain multiple filters by combining them into a filter array.
The filters will be logically combined with an `AND` operator.

```graphql
{
  deals(
    filters: [
      { field: "modified_at", operation: GE, value: "2010-03-02" }
      { field: "country.name", operation: EQ, value: "Myanmar" }
    ]
  ) {
    id
    country {
      id
      name
    }
  }
}
```
Note that you can filter on subfields like e.g. `country.name` by chaining them with a `.`.

If you want to create a logical `OR` filter on a specific field you can use the `IN`
operator in combination with an array of values:
```graphql
{
  deals(
    filters: [
      { field: "country.name", operation: IN, value: ["Myanmar", "Bangladesh"] }
    ]
  ) {
    id
    deal_size
    country {
      name
    }
  }
}
```


### Logical operators

Available logical operators are:

* `EQ`: equals
* `IN`: in/part of
* `CONTAINS`: contains
* `LT`: less than
* `LE`: less or equal than
* `GT`: greater than
* `GE`: greater or equal than
