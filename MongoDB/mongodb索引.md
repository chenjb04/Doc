[toc]

# 索引

MongoDB 的索引是基于 B-tree数据结构及对应算法形成的。树索引存储特定字段或字段集的值，按字段值排序。索引条目的排序支持有效的等式匹配和基于范围的查询操作。

# 索引类型

MongoDB 中索引的类型大致包含单键索引、复合索引、多键值索引、地理索引、全文索引、 散列索引等

## 单键索引

MongoDB 支持文档集合中任何字段的索引，在默认情况下，所有集合在 _id 字段上都有一个索引，应用程序和用户可以添加额外的索引来支持重要的查询操作。

对于单字段索引和排序操作，索引键的排序顺序（即升序或降序）无关紧要，因为 MongoDB 可以在任意方向上遍历索引。

语法

在3.0之前版本是ensureIndex

```
db.collection.createlndex ( { key: 1 } )  //1 为升序，-1 为降序
```

实例

创建数据

```
db.inventory.insert([
{ "_id" : 1, "item" : "f1", type: "food", quantity: 500 },
{ "_id" : 2, "item" : "f2", type: "food", quantity: 100 },
{ "_id" : 3, "item" : "p1", type: "paper", quantity: 200 },
{ "_id" : 4, "item" : "p2", type: "paper", quantity: 150 },
{ "_id" : 5, "item" : "f3", type: "food", quantity: 300 },
{ "_id" : 6, "item" : "t1", type: "toys", quantity: 500 },
{ "_id" : 7, "item" : "a1", type: "apparel", quantity: 250 },
{ "_id" : 8, "item" : "a2", type: "apparel", quantity: 400 },
{ "_id" : 9, "item" : "t2", type: "toys", quantity: 50 },
{ "_id" : 10, "item" : "f4", type: "food", quantity: 75 }])
```

创建索引

```
db.inventory.createIndex({quantity:1})
```

查看执行计划

```
db.inventory.find({quantity: {$gte:100, $lte:200}}).explain("executionStats")
```

## 复合索引

MongoDB 支持复合索引，其中复合索引结构包含多个字段

语法

```
db.collection.createIndex ({ <key1> : <type>, <key2> : <type2>, ...})
```

实例

```
db.inventory.createIndex({quantity:1, item:1})
```

## 多键值索引

若要为包含数组的字段建立索引，MongoDB 会为数组中的每个元素创建索引键。这些多键值索引支持对数组字段的高效查询

语法

```
db.collecttion.createlndex( { <key>: < 1 or -1 > })
```

实例

```
db.survey.insert ({item : "ABC", ratings: [ 2, 5, 9 ]})
db.survey.createIndex({ratings:1})
```

## 地理索引

地理索引包含两种地理类型，如果需要计算的地理数据表示为类似于地球的球形表面上的坐标，则可以使用 2dsphere 索引。

通常可以按照坐标轴、经度、纬度的方式把位置数据存储为 GeoJSON 对象。GeoJSON 的坐标参考系使用的是 wgs84 数据。如果需要计算距离（在一个欧几里得平面上），通常可以按照正常坐标对的形式存储位置数据，可使用 2d 索引

语法

```
db.collection.createlndex( { <location field> : "2dsphere"})

db.<collection>.createIndex(
{
    <location field> : "2d",
    <additional field> : <value>
},
{
    <index-specification options>
}
)
```

实例

```
db.places.insert(
{ 
    loc : { type: "Point", coordinates: [ -73.97, 40.77 ] },
    name: "Central Park",
    category : "Parks"
}
)
db.places.insert(
{
    loc : { type: "Point", coordinates:[ -73.88, 40.78 ] },
    name: "La Guardia Airport",
    category : "Airport"
}
)
db.places.createIndex ({loc : "2dsphere"})
db.places.find({loc : "2dsphere"}).explain()
```

## 全文索引

MongoDB 的全文检索提供三个版本，用户在使用时可以指定相应的版本，如果不指定则默认选择当前版本对应的全文索引。

语法

```
db.collection.createIndex ({ key: "text" })
```

## 散列索引

散列（Hashed）索引是指按照某个字段的散列值来建立索引，目前主要用于 MongoDB Sharded Cluster 的散列分片，散列索引只能用于字段完全匹配的查询，不能用于范围查询等

语法

```
db.collection.createlndex( { _id : "hashed" })
```

MongoDB 支持散列任何单个字段的索引，但是不支持多键（即数组）索引

# 索引参数

上面列出的都是索引的类别，在每个索引的类别上还可以加上一些参数，使索引更加具有针对性，常见的参数包括稀疏索引、唯一索引、过期索引等。

## 稀疏索引

稀疏索引只检索包含具有索引字段的文档，即使索引字段包含空值，检索时也会跳过所有缺少索引字段的文档。因为索引不包含集合的所有文档，所以说索引是稀疏的。相反，非稀疏索引包含集合中的所有文档，存储不包含索引字段的文档的空值。

语法

```
db.collection.createlndex ({ "key" : 1 }, { sparse : true })
```

## 唯一索引

如果设置了唯一索引，新插入文档时，要求 key 的值是唯一的，不能有重复的出现

语法

```
db.collection.createlndex ({ "key" : 1 }, { unique: true })
```

## 过期索引

过期索引是一种特殊的单字段索引，MongoDB 可以用来在一定时间或特定时间后从集合中自动删除文档。

过期索引对于处理某些类型的信息非常有用，例如，机器生成的事务数据、日志和会话信息，这些信息只需要在数据库中存在有限的时间，不需要长期保存。

语法

```
db.collection.createlndex( {"key" : 1 }, { expireAfterSeconds: 3600 })
```

# 查看索引

语法

```
db.collection.getIndexes()
```

# 删除索引

语法

```
db.collection.dropIndex()
# 删除id之外的所有索引
db.collection.dropIndexes()
```

实例

```
 db.inventory.dropIndex({quantity:1})
 db.inventory.dropIndexes()
```

# 修改索引

若要修改现有索引，则需要删除现有索引并重新创建索引。

