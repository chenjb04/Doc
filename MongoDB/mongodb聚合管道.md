[toc]

# aggregate

MongoDB中聚合(aggregate)主要用于处理数据(诸如统计平均值,求和等)，并返回计算后的数据结果。有点类似sql语句中的 count(*), sum(), avg()。

语法

```
db.collection.aggregate(AGGREGATE_OPERATION)
```

实例

```
db.example.insert([
{
   title: 'MongoDB Overview', 
   description: 'MongoDB is no sql database',
   by_user: 'w3cschool.cc',
   url: 'http://www.w3cschool.cc',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 100
},
{
   title: 'NoSQL Overview', 
   description: 'No sql database is very fast',
   by_user: 'w3cschool.cc',
   url: 'http://www.w3cschool.cc',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 10
},
{
   title: 'Neo4j Overview', 
   description: 'Neo4j is no sql database',
   by_user: 'Neo4j',
   url: 'http://www.neo4j.com',
   tags: ['neo4j', 'database', 'NoSQL'],
   likes: 750
}])
```

计算每个作者写的文章数，类似于sql

```sql
select by_user, count(*) from example group by by_user
```

使用aggregate

```
db.example.aggregate({$group: {_id:"$by_user", num:{$sum:1}}})
```

结果

```
{ "_id" : "Neo4j", "num" : 1 }
{ "_id" : "w3cschool.cc", "num" : 2 }
```

常见聚合表达式

| 表达式    | 描述                                           | 实例                                                         |
| :-------- | :--------------------------------------------- | :----------------------------------------------------------- |
| $sum      | 计算总和。                                     | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : "$likes"}}}]) |
| $avg      | 计算平均值                                     | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$avg : "$likes"}}}]) |
| $min      | 获取集合中所有文档对应值得最小值。             | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$min : "$likes"}}}]) |
| $max      | 获取集合中所有文档对应值得最大值。             | db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}]) |
| $push     | 在结果文档中插入值到一个数组中。               | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$push: "$url"}}}]) |
| $addToSet | 在结果文档中插入值到一个数组中，但不创建副本。 | db.mycol.aggregate([{$group : {_id : "$by_user", url : {$addToSet : "$url"}}}]) |
| $first    | 根据资源文档的排序获取第一个文档数据。         | db.mycol.aggregate([{$group : {_id : "$by_user", first_url : {$first : "$url"}}}]) |
| $last     | 根据资源文档的排序获取最后一个文档数据         | db.mycol.aggregate([{$group : {_id : "$by_user", last_url : {$last : "$url"}}}]) |

# 聚合管道

MongoDB 的聚合框架就是将文档输入处理管道，在管道内完成对文档的操作，最终将文档转换为聚合结果。

最基本的管道阶段提供过滤器，其操作类似查询和文档转换，可以修改输出文档的形式。其他管道操作提供了按特定字段对文档进行分组和排序的工具，以及用于聚合数组内容（包括文档数组）的工具。

此外，在管道阶段还可以使用运算符来执行诸如计算平均值或连接字符串之类的任务。聚合管道可以在分片集合上运行。

![](C:\Users\vt\AppData\Roaming\Typora\typora-user-images\image-20200804140706224.png)

相当于sql语句

```sql
select cust_id,sum(amount)as total from orders where status= "A"
```

# $project

控制数据列的显示规则。可以用来重命名、增加或删除字段(域)，也可以用于创建计算结果以及嵌套文档。

示例

```
db.books.insert(
{
  "_id" : 1,
  title: "abc123",
  isbn: "0001122223334",
  author: { last: "zzz", first: "aaa" },
  copies: 5
}
)
```

## 输出指定字段

```
db.books.aggregate({$project:{title:1, author:1, _id:0}})
```

很像之前的投影``books.find({},{'title':1,'author':1,'_id':0})``

## 输出嵌入式文档中的 filed

```
db.books.aggregate({$project: {"author.last":1}})
```

结果

```
{ "_id" : 1, "author" : { "last" : "zzz" } }
```

## 改变输出结构

```
db.books.aggregate({$project:{"lastname": "$author.last"}})
```

结果

```
{ "_id" : 1, "lastname" : "zzz" }
```

相当于sql中`select author.last as lastname from books`

# $match

用于过滤数据，只输出符合条件的文档。$match使用MongoDB的标准查询操作。

插入数据

```
db.articles.insert([{ "_id" : 1, "author" : "dave", "score" : 80, "views" : 100 },{ "_id" : 2, "author" : "dave", "score" : 85, "views" : 521 },{ "_id" : 3, "author" : "ahn", "score" : 60, "views" : 1000 },{ "_id" : 4, "author" : "li", "score" : 55, "views" : 5000 },{ "_id" : 5, "author" : "annT", "score" : 60, "views" : 50 },{ "_id" : 6, "author" : "li", "score" : 94, "views" : 999 },{ "_id" : 7, "author" : "ty", "score" : 95, "views" : 1000 }])
```

- 输出autho等于dave的文档

```
db.articles.aggregate({$match:{author:"dave"}})
```

结果

```
{ "_id" : 1, "author" : "dave", "score" : 80, "views" : 100 }
{ "_id" : 2, "author" : "dave", "score" : 85, "views" : 521 }
```

- 统计 articles 集合中 score在70~90中间，或者views大于等于1000

使用find

```
db.articles.find({$or:[{score:{$gt:70,$lt:90}},{views:{$gte:1000}}]})
```

结果

```
{ "_id" : 1, "author" : "dave", "score" : 80, "views" : 100 }
{ "_id" : 2, "author" : "dave", "score" : 85, "views" : 521 }
{ "_id" : 3, "author" : "ahn", "score" : 60, "views" : 1000 }
{ "_id" : 4, "author" : "li", "score" : 55, "views" : 5000 }
{ "_id" : 7, "author" : "ty", "score" : 95, "views" : 1000 }
```

使用match

```
db.articles.aggregate({$match: {$or:[{score:{$gt:70,$lt:90}},{views:{$gte:1000}}]}})
```

- 统计 articles 集合中 score在70~90中间，或者views大于等于1000 个数

  ```
  db.articles.aggregate({$match: {$or:[{score:{$gt:70,$lt:90}},{views:{$gte:1000}}]}}, {$group: {_id:null, count:{$sum:1}}})
  ```

  结果

  ```
  { "_id" : null, "count" : 5 }
  ```

# $group

将集合中的文档分组，可用于统计结果。

插入数据

```
db.sales.insert([
{ "_id" : 1, "item" : "abc", "price" : 10, "quantity" : 2, "date" : ISODate("2014-03-01T08:00:00Z") },
{ "_id" : 2, "item" : "jkl", "price" : 20, "quantity" : 1, "date" : ISODate("2014-03-01T09:00:00Z") },
{ "_id" : 3, "item" : "xyz", "price" : 5, "quantity" : 10, "date" : ISODate("2014-03-15T09:00:00Z") },
{ "_id" : 4, "item" : "xyz", "price" : 5, "quantity" : 20, "date" : ISODate("2014-04-04T11:21:39.736Z") },
{ "_id" : 5, "item" : "abc", "price" : 10, "quantity" : 10, "date" : ISODate("2014-04-04T21:23:13.331Z") }
])
```

- 使用 $group 将文档按月、日、年组分组, 计算平均数量以及每个组的文档数

  ```
  db.sales.aggregate(
     [
        {
          $group : {
             _id : { month: { $month: "$date" }, day: { $dayOfMonth: "$date" }, year: { $year: "$date" } },
             averageQuantity: { $avg: "$quantity" },
             count: { $sum: 1 }
          }
        }
     ]
  )
  ```

  结果

  ```
  { "_id" : { "month" : 3, "day" : 15, "year" : 2014 }, "averageQuantity" : 10, "count" : 1 }
  { "_id" : { "month" : 4, "day" : 4, "year" : 2014 }, "averageQuantity" : 15, "count" : 2 }
  { "_id" : { "month" : 3, "day" : 1, "year" : 2014 }, averageQuantity" : 1.5, "count" : 2 }
  ```

- 计算总价格和平均数量以及集合中的所有文件数

  ```
  db.sales.aggregate({$group: {_id:null, totalPrice:{$sum: {$multiply:["$price", "$quantity"]}}, count: {$sum:1}}})
  ```

  结果

  ```
  { "_id" : null, "totalPrice" : 290, "count" : 5 }
  ```

- $group 将item字段去重

  ```
  db.sales.aggregate({$group: {_id:"$item"}})
  ```

  结果

  ```
  { "_id" : "xyz" }
  { "_id" : "abc" }
  { "_id" : "jkl"}
  ```

- 按authors分组, 收集books中的titles

  插入数据

  ```
  db.books.insert([
  { "_id" : 8751, "title" : "The Banquet", "author" : "Dante", "copies" : 2 },
  { "_id" : 8752, "title" : "Divine Comedy", "author" : "Dante", "copies" : 1 },
  { "_id" : 8645, "title" : "Eclogues", "author" : "Dante", "copies" : 2 },
  { "_id" : 7000, "title" : "The Odyssey", "author" : "Homer", "copies" : 10 },
  { "_id" : 7020, "title" : "Iliad", "author" : "Homer", "copies" : 10 }
  ])
  ```

  ```
  db.books.aggregate({$group :{_id:"$author", books: {$push: "$title"}}})
  ```

  结果

  ```
  { "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
  { "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] 
  }
  ```

-  按author分组，收集 $$ROOT 系统变量(代表文档自身)

  ```
   db.books.aggregate({$group :{_id:"$author", books: {$push: "$$ROOT"}}})
  ```

  结果

  ```
  { "_id" : "Dante", "books" : [ { "_id" : 8751, "title" : "The Banquet", "author" : "Dante", "copies" : 2 }, { "_id" : 8752, "title" : "Divine Comedy", "author" : "Dante", "copies" : 1 }, { "_id" : 8645, "title" : "Eclogues", "author" : "Dante", "copies" : 2 } ] }
  { "_id" : "Homer", "books" : [ { "_id" : 7000, "title" : "The Odyssey", "author" : "Homer", "copies" : 10 }, { "_id" : 7020, "title" : "Iliad", "author" : "Homer", "copies" : 10 } ] }
  ```

# $unwind

将文档中的某一个数组类型字段拆分成多条，每条包含数组中的一个值。

语法

```
{ $unwind: <field path> }

{
  $unwind:
    {
      path: <field path>,  #拆分路径
      includeArrayIndex: <string>, #指定数组索引号
      preserveNullAndEmptyArrays: <boolean>  #防止数据丢失
    }
}
```

插入数据

```
db.inventory.insert({ "_id" : 1, "item" : "ABC1", sizes: [ "S", "M", "L"] })
```

使用$unwind 让数组中的每个元素输出一个文档

```
db.inventory.aggregate({$unwind: "$sizes"})
或者
db.inventory.aggregate({$unwind: {path:"$sizes"}})
```

结果

```
{ "_id" : 1, "item" : "ABC1", "sizes" : "S" }
{ "_id" : 1, "item" : "ABC1", "sizes" : "M" }
{ "_id" : 1, "item" : "ABC1", "sizes" : "L" }
```

插入数据

```
db.inventory.insert([
{ "_id" : 1, "item" : "ABC", "sizes" : [ "S", "M", "L" ] },
{ "_id" : 2, "item" : "EFG", "sizes" : [ ] },
{ "_id" : 3, "item" : "IJK", "sizes" : "M" },
{ "_id" : 4, "item" : "LMN" },
{ "_id" : 5, "item" : "XYZ", "sizes" : null }
])
```

**如果`sizes`字段不能解析成数组，但又不属于情况(不存在，null，或一个空数组，处理方式：丢弃)，`$unwind` 将视为一个单数组操作。**

指定索引号 includeArrayIndex

```
db.inventory.aggregate( [ { $unwind: { path: "$sizes", includeArrayIndex: "arrayIndex" } }])
```

结果

```
{ "_id" : 1, "item" : "ABC", "sizes" : "S", "arrayIndex" : NumberLong(0) }
{ "_id" : 1, "item" : "ABC", "sizes" : "M", "arrayIndex" : NumberLong(1) }
{ "_id" : 1, "item" : "ABC", "sizes" : "L", "arrayIndex" : NumberLong(2) }
{ "_id" : 3, "item" : "IJK", "sizes" : "M", "arrayIndex" : null }
```

数据出现了丢失情况，sizes为不存在，[] 或者null时，数据丢失

```
db.inventory.aggregate( [
   { $unwind: { path: "$sizes", preserveNullAndEmptyArrays: true } }
] )
```

结果

```
{ "_id" : 1, "item" : "ABC", "sizes" : "S" }
{ "_id" : 1, "item" : "ABC", "sizes" : "M" }
{ "_id" : 1, "item" : "ABC", "sizes" : "L" }
{ "_id" : 2, "item" : "EFG" }
{ "_id" : 3, "item" : "IJK", "sizes" : "M" }
{ "_id" : 4, "item" : "LMN" }
{ "_id" : 5, "item" : "XYZ", "sizes" : null }
```

# $lookup

执行左连接到一个集合(unsharded)，必须在同一数据库中

$lookup添加了一个新的数组字段，该字段的元素是 `joined`集合中的匹配文档。
语法

```
{
   $lookup:
     {
       from: <collection to join>,   #右集合
       localField: <field from the input documents>,  #左集合 join字段
       foreignField: <field from the documents of the "from" collection>, #右集合 join字段
       as: <output array field>   #新生成字段（类型array）
     }
}
```

| Field          | Description                                                  |
| :------------- | :----------------------------------------------------------- |
| `from`         | 右集合，指定在同一数据库中执行连接的集合。此集合不能shared分片。 |
| `localField`   | 指定左集合（db.collectionname）匹配的字段。如果左集合不包含localField，$lookup 视为null值来匹配。 |
| `foreignField` | 指定from集合（右集合）用来匹配的字段。如果集合不包含该字段，$lookup 视为null值来匹配。 |
| `as`           | 指定要添加到输入文档的新数组字段的名称。新的数组字段包含from集合中匹配的文档。如果在文档中指定的名称已经存在，现有的领域覆盖。 |

实例

左集合orders

```
db.orders.insert([
{ "_id" : 1, "item" : "abc", "price" : 12, "quantity" : 2 },
{ "_id" : 2, "item" : "jkl", "price" : 20, "quantity" : 1 },
{ "_id" : 3 }
])
```

右集合inventory

```
db.inventory.insert([
{ "_id" : 1, "sku" : "abc", "description" : "product 1", "instock" : 120 },
{ "_id" : 2, "sku" : "def", "description" : "product 2", "instock" : 80 },
{ "_id" : 3, "sku" : "ijk", "description" : "product 3", "instock" : 60 },
{ "_id" : 4, "sku" : "jkl", "description" : "product 4", "instock" : 70 },
{ "_id" : 5, "sku" : null, "description" : "Incomplete" },
{ "_id" : 6 }
])
```

以下聚合操作对 `orders左集合` 左连接 `inventory右集合`，通过 orders下的`item` 与 `inventory集合的sku`：

值得注意：

- 两个集合必须在同一个`db`,
- `orders`是左集合，左连接；
- item是`orders`左集合字段；
- sku是`inventory`右集合字段
- `item`为null, 左连接, 右集合 `sku`为null

```
db.orders.aggregate([ { $lookup: { from: "inventory", localField: "item", foreignField: "sku", as: "inventory_docs" } }]).pretty()
```

结果

```json
{
        "_id" : 1,
        "item" : "abc",
        "price" : 12,
        "quantity" : 2,
        "inventory_docs" : [
                {
                        "_id" : 1,
                        "sku" : "abc",
                        "description" : "product 1",
                        "instock" : 120
                }
        ]
}
{
        "_id" : 2,
        "item" : "jkl",
        "price" : 20,
        "quantity" : 1,
        "inventory_docs" : [
                {
                        "_id" : 4,
                        "sku" : "jkl",
                        "description" : "product 4",
                        "instock" : 70
                }
        ]
}
{
        "_id" : 3,
        "inventory_docs" : [
                {
                        "_id" : 5,
                        "sku" : null,
                        "description" : "Incomplete"
                },
                {
                        "_id" : 6
                }
        ]
}
```

# $out

将查询结果输出到指定的集合

插入数据

```
db.books.insert([
{ "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] },
{ "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
])
```

```
db.books.aggregate( [
    { $group : { _id : "$author", books: { $push: "$title" } } },
    { $out : { db: "reporting", coll: "authors" } }
] )
```

​	