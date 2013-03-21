# Tables


## merchant

the table that holds metadata about a claimed merchant profile

```gherkin
| field_name        | field_type  | description                                                      |
| id                | integer     | the primary key of this table                                    |
| verified          | boolean     | a merchant can use our platform only after verified by this flag |
| show_yelp_ratings | boolean     | flag that determines whether we should show yelp ratings or no   |
| email             | string      | the of the person in charge for that business                    |
| first_name        | string      | meh.                                                             |
| last_name         | string      | meh.                                                             |
| password          | string      | meh.                                                             |
| phone             | phone field | meh.                                                             |
| zipcode           | integer     |                                                                  |
| address           | string      |                                                                  |
| city_id           | integer     | relates to geo_city                                              |
```

## merchant-tags

maps which tags this business uses

```gherkin
| field_name  | field_type | description                             |
| id          | integer    | the primary key of this table           |
| merchant_id | integer    | the id of the merchant                  |
| tag_id      | integer    | the id of the tag in the yipit database |
```

## business-tracking

works kinda like a m2m table


### columns

```gherkin
| field_name | field_type | description                                              |
| id         | integer    | the primary key of this table                            |
| my_id      | integer    | the id of the business who subscribed for yipit merchant |
| target_id  | integer    | the id of the business being tracked                     |
```


## custom_merchant_deal

The table that holds information for the custom deals created by our merchants

### columns

```gherkin
| field_name   | field_type | description                                                                       |
| id           | integer    | the primary key of this table                                                     |
| title        | string     | the title of the deal                                                             |
| subtitle     | string     | the subtitle of the deal                                                          |
| description  | longtext   | should be able to take *A LOT* of text                                            |
| header_image | string     | a URL pointing to the image that will be used in the header of the email campaign |
```


## custom_merchant_deal_bullet

The table that holds information for the custom deals created by our merchants

### columns

```gherkin
| field_name     | field_type | description                                                |
| id             | integer    | the primary key of this table                              |
| custom_deal_id | integer    | the id of the related `custom_merchant_deal` table (above) |
| content        | string     | the string that holds the bullet text                      |
```
