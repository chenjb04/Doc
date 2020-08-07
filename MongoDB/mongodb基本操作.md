[toc]

# 创建数据库

### 语法

```
use DATABASE_NAME
```

如果数据库不存在，则创建，如果存在，则切换到指定数据库

### 实例

```
> use blog
switched to db blog
> db
blog
```

### 查看当前数据库

```
db
```

### 显示所有的数据库

```
show dbs 或者 show databases
```

新创建的数据库不会显示，插入一条数据时才会显示

### 查看当前数据库的collection

```
show collections
```

MongoDB 中**默认的数据库为 test**，如果你没有创建新的数据库，集合将存放在 test 数据库中

# 删除数据库

### 语法

```
db.dropDatabase()
```

删除当前数据库，默认为 test，你可以使用 db 命令查看当前数据库名。

### 实例

```
> show dbs
READ_ME_TO_RECOVER_YOUR_DATA  0.000GB
admin                         0.000GB
blog                          0.000GB
config                        0.000GB
local                         0.000GB
test                          0.000GB
> db.dropDatabase()
{ "dropped" : "blog", "ok" : 1 }
```

# 创建集合

### 语法

```
db.createCollection(name, options)
```

在命令中, name 是要创建的集合的名称. Options 是一个文档，用于指定配置的集合

| 参数    | 类型     | 描述                               |
| :------ | :------- | :--------------------------------- |
| Name    | String   | 要创建的集合名称                   |
| Options | Document | （可选）指定有关内存大小和索引选项 |

选项参数是可选的，所以只需要到指定的集合名称。以下是可以使用的选项列表：

| 字段        | 类型    | 描述                                                         |
| :---------- | :------ | :----------------------------------------------------------- |
| capped      | Boolean | （可选）如果为true，则启用封顶集合。封顶集合是固定大小的集合，当它达到其最大大小，会自动覆盖最早的条目。如果指定true，则需要也指定size字段。 |
| autoIndexID | Boolean | （可选）如果为true，自动创建索引_id字段, 默认值是false。     |
| size        | number  | （可选）指定集合最大可使用字节。如果封顶如果是 true，那么你还需要指定这个字段。 |
| max         | number  | （可选）指定封顶集合允许在文件的最大数量。Size限制优先于此限制。如果一个封顶集合达到大小size限制，未达到文件的最大数量，MongoDB删除旧的文件。如果您更喜欢使用max，确保为上限的集合所需的大小限制，足以包含文档的最大数量。 |

当插入文档，MongoDB 第一检查大小字段封顶集合，然后它会检查最大的字段。

### 示例

```
 db.createCollection("example")
{ "ok" : 1 }
> show collections
blog
example

> db.createCollection("test", {capped: true, size: 5242880, max: 5000})
{ "ok" : 1 }
> show collections
blog
example
test
```

在MongoDB中，可以不需要创建集合。当插入一些文档自动创建的集合。

# 删除集合

### 语法

```
db.COLLECTION_NAME.drop()
```

### 示例

```
> db.test.drop()
true
> show collections
blog
example
```

# 数据类型

- String : 这是最常用的数据类型来存储数据。在MongoDB中的字符串必须是有效的UTF-8。
- Integer : 这种类型是用来存储一个数值。整数可以是32位或64位，这取决于您的服务器。
- Boolean : 此类型用于存储一个布尔值 (true/ false) 。
- Double : 这种类型是用来存储浮点值。
- Min/ Max keys : 这种类型被用来对BSON元素的最低和最高值比较。
- Arrays : 使用此类型的数组或列表或多个值存储到一个键。
- Timestamp : 时间戳。这可以方便记录时的文件已被修改或添加。
- Object : 此数据类型用于嵌入式的文件。
- Null : 这种类型是用来存储一个Null值。
- Symbol : 此数据类型用于字符串相同，但它通常是保留给特定符号类型的语言使用。
- Date : 此数据类型用于存储当前日期或时间的UNIX时间格式。可以指定自己的日期和时间，日期和年，月，日到创建对象。
- Object ID : 此数据类型用于存储文档的ID。
- Binary data : 此数据类型用于存储二进制数据。
- Code : 此数据类型用于存储到文档中的JavaScript代码。
- Regular expression : 此数据类型用于存储正则表达式

# 插入文档

要将数据插入MongoDB 集合中，可以使用 MongoDB 的 insert() 方法，同时 MongoDB 针对插入一条还是多条数据，提供了更可靠的 insertOne() 和 insertMany() 方法。

MongoDB 向集合里插入记录时，无须事先对数据存储结构进行定义。如果待插入的集合不存在，则插入操作会默认创建集合。

### insert

语法

```
db.collection.insert(
   <document or array of documents>,
   {
     writeConcern: <document>,
     ordered: <boolean>
   }
)
```

实例

```
db.example.insert({"name": "xiaoming", "age": 18})
```

插入文档中，如果我们不指定_id参数，然后MongoDB 本文档分配一个唯一的ObjectId。

**如果指定_id参数，值必须唯一，以避免重复键错误。**

_id 是12个字节的十六进制数，唯一一个集合中的每个文档。 12个字节被划分如下

```
_id: ObjectId(4 bytes timestamp, 3 bytes machine id, 2 bytes process id, 3 bytes incrementer)
```

insert还可以插入多条数据，可以传递一个数组 insert() 命令的文件。

```
db.example.insert([{"name": "xiaozhang", "age": 20}, {"name":"xiaogang", "age": 17}])
```

### insertOne

语法

```
db.collection.insertOne(
   <document>,
   {
      writeConcern: <document>
   }
)
```



插入一条文档

```
 db.example.insertOne({"name":"xiaohong", "age": 18})
```

### insertMany

语法

```
db.collection.insertMany(
   [ <document 1> , <document 2>, ... ],
   {
      writeConcern: <document>,
      ordered: <boolean>
   }
)
```

ordered表示插入时的顺序，默认true有序插入。

**在插入多条时，如果遇到错误，剩余的文档将不会被插入，如果设置ordered为false，会继续插入剩余的文档。**

插入多条文档

```
db.example.insertMany([{"nmae":"xiaoli", "age": 25},{"name":"xiaozhao","age":22}])
```

### insert 和save区别

save() 方法等同于`insert()`方法

``save``决定是插入一个文档还是更新，取决于_id参数。如果能根据_id找到一个已经存在的文档，那么就更新。如果没有传入_id参数或者找不到存在的文档，那么就插入一个新文档。

实例

```
db.example.save({"name":"xiaochen", "age": 15})
```

直接插入 无_id参数，等价于``insert``

```
db.example.save({"_id": ObjectId("5f27bc051ddc24e683f0053e"), "name": "xiaochen", "age": 18})
```

指定_id参数且存在于集合，则更新文档

# 查询文档

### find

语法

```
db.collection.find(query, projection)
```

query 为可选项，设置查询操作符指定查询条件；projection 也为可选项，表示使用投影操作符指定返回的字段，如果忽略此选项则返回所有字段。

实例

```
db.example.find().pretty()
```

pretty() 方法,结果显示在一个格式化的方式

### findOne

只返回一条结果

```
db.example.findOne()
```

### 查询条件

| 操作符         | 格式                                                | 实例                                                         | 与 RDBMS where 语句比较                            |
| -------------- | --------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| 等于（=）      | {<key> : {<value>}}                                 | db.test.find( {price : 24} )                                 | where price = 24                                   |
| 大于（>）      | {<key> : {$gt : <value>}}                           | db.test.find( {price : {$gt : 24}} )                         | where price > 24                                   |
| 小于（<）      | {<key> : {$lt : <value>}}                           | db.test.find( {price : {$lt : 24}} )                         | where price < 24                                   |
| 大于等于（>=） | {<key> : {$gte : <value>}}                          | db.test.find( {price : {$gte : 24}} )                        | where price >= 24                                  |
| 小于等于（<=） | {<key> : {$lte : <value>}}                          | db.test.find( {price : {$lte : 24}} )                        | where price <= 24                                  |
| 不等于（!=）   | {<key> : {$ne : <value>}}                           | db.test.find( {price : {$ne : 24}} )                         | where price != 24                                  |
| 与（and）      | {key01 : value01, key02 : value02, ...}             | db.test.find( {name : "《MongoDB 入门教程》", price : 24} )  | where name = "《MongoDB 入门教程》" and price = 24 |
| 或（or）       | {$or : [{key01 : value01}, {key02 : value02}, ...]} | db.test.find( {$or:[{name : "《MongoDB 入门教程》"},{price : 24}]} ) | where name = "《MongoDB 入门教程》" or price =     |

### and语法

语法

如果通过多个键分离','，那么 MongoDB 处理 AND 条件

```
db.collection.find({key1:value1, key2:value2}).pretty()
```

或者

```
db.collection.find(
   {
      $and: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```

实例

查询名字是xiaozhao并且年龄22

```
db.example.find({"name":"xiaozhao", "age":22}).pretty()
```

### or语法

OR条件的基础上要查询文件，需要使用$or关键字

```
db.collection.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```

实例

查询年龄大于20或者name等于xiaogang数据

```
db.example.find({$or:[{"age":{$gt:20}},{"name":"xiaogang"}]}).pretty()
```

### not

查询年龄不大于20的文档

```
db.example.find({"age": {$not:{$gt:20}}})
```

### nor

不属于

查询年龄不等于17的文档

```
db.example.find( {$nor:[ {"age":17} ]})
```

### in nin

比较运算符

语法

```
{field : {$in: [<value1>, <value2>...]}}
```

实例

查询年龄在17,18,20

```
db.example.find({"age": {$in:[17,18,20]}})
```

nin 不存在

查询年龄不在17,18,20

```
db.example.find({"age": {$nin:[17,18,20]}})
```

### exists

包含字段文档

语法

```
{field : {$exists: <boolean>}}
```

实例

查询包含age字段的值

```
db.example.find({"age":{$exists:true}})
```

### type

字段类型

语法

```
{field : {$type: <Bson type>}}
```

实例

查询名字是string类型的文档

```
db.example.find({"name":{$type:"string"}})
```

1 表示 显示指定列 0表示不显示指定列

```
db.example.find({},{"name":"1","_id": 0})
```

数组使用$slice

返回contact·数组的第一个字段

```
db.example.find({}, {contact: {$slice:1}})
```

### 数组操作符

插入数组文档

```
db.example.insert([{name:"jack",balance:2000,contact:["123456","Alabama", "US"]}, {name:"karen",balance:2500, contact:[["456", '454545'],"beijing", "china"]}])
```

#### all

$all主要用来查询数组中的包含关系，查询条件中只要有一个不包含就不返回

实例

查询contact包含beiing和china的文档

```
db.example.find({contact: {$all: ["beijing", "china"]}}).pretty()
```

#### elemMatch

$elemMatch 数组查询操作用于查询数组值中至少有一个能完全匹配所有的查询条件的文档

查询contact值大于1小于900000000000的文档

```
db.example.find({contact: {$elemMatch: {$gt :"1", $lt:"90000000"}}}).pretty()
```

### regex

正则表达式运算符

语法

```
{field: {: /parttern/, : '<options>'}}
{field: {: /parttern/<options>}}
```

在和$in一起使用时，只能使用第二种

实例

查询name已xiao开头或者j开头的文档

```
db.example.find({name: {$in : [/^xiao/,/^j/]}}).pretty()
```

查询名字包含ang且忽略大小写的文档

```
db.example.find({name: {$regex : /ang/, $options:"i"}}).pretty()
```

### limit

限制查询结果个数

```
b.example.find().limit(2)
```

### skip

Skip() 函数用于略过指定个数的文档

```
db.example.find().skip(1)
```

跳过第一个结果，返回剩余的结果

**skip在limit之前执行**

### count

返回查询结果总个数

```
db.example.find().count()
```

### sort

sort() 函数用于对查询结果进行排序，1 是升序，-1 是降序

对年龄降序排序

```
db.example.find().sort({"age": -1})
```

**sort在skip之前执行**

# 更新文档

MongoDB 使用 update() 和 save() 方法来更新集合中的文档

### update

语法

```
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```

- query : update的查询条件，类似sql update查询内where后面的。
- update : update的对象和一些更新的操作符（如$,$inc…）等，也可以理解为sql update查询内set后面的
- upsert : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew，true为插入，默认是false，不插入。
- multi : 可选，mongodb 默认是false，只更新找到的第一条记录，如果这个参数为true，就把按条件查出来多条记录全部更新。
- writeConcern :可选，抛出异常的级别。

示例

把xiaozhao的年龄改为20

```
db.example.update({"name":"xiaozhao"}, {$set:{"age": 20}})
```

update默认只更新符合条件的一条数据，如果要改变多条，需要设置参数置`multi`为true

把年龄18的都改为20

```
db.example.update({"age": 18}, {$set:{"age": 20}},{multi:true})
```

**文档id不可改变**

#### 更新操作符

##### set

set 更新或者新增字段

语法

```
{$set: {<field1>:<value1>}}
```

##### unset

删除字段

语法

```
{$set: {<field1>:""}}
```

实例

```
db.example.update({name: "xiaoli"},{$unset: {name:""}})
```

##### rename

重命名字段

语法

```
{$rename: {<field1>:<newname>}}
```

实例

把lili的gender重命名为sex字段

```
db.student.update({name: "lili"},{$rename: {"gender": "sex"}}) 
```

#### 数组操作符

##### addToSet

往数组中添加元素

如果数组中存在这个值，那么不会添加重复值

实例

往book数组中添加hhahah

```
db.books.update({"_id": "Homer"}, {$addToSet: {books: "hahha"}}
```

##### each

插入内嵌数组时，值单独 处理

实例

```
db.books.update({"_id": "Homer"}, {$addToSet: {"books": {$each: ['page', 'name']}}})
```

##### pop

删除数组元素

只能删除第一个(-1)或者最后一个(1) 删除最后一个元素后 会保留[]

实例

删除最后一个元素

```
db.books.update({"_id": "Homer"}, {$pop: {"books": 1}})
```

##### pull

删除特定元素 模糊程度更高

实例

```
db.books.update({"_id": "Homer"}, {$pull: {"books": {$regex: /ha/}}})
```

##### pullAll

删除特定元素 相当于 pull + in

##### push

添加元素

### updateOne

更新一条数据

```
db.example.updateOne({"age": 20}, {$set:{"age": 18}})
```

### updateMany

更新多条符合条件的数据

```
db.example.updateMany({"age": 20}, {$set:{"age": 18}})
```

### save

``save``决定是插入一个文档还是更新，取决于_id参数。如果能根据_id找到一个已经存在的文档，那么就更新。如果没有传入_id参数或者找不到存在的文档，那么就插入一个新文档。

# 删除文档

###  remove

remove() 函数可以接受一个查询文档作为可选参数来有选择性地删除符合条件的文档。删除文档是永久性的，不能撤销，也不能恢复

语法

```
db.collection.remove(
    <query>,
    {
        justOne: <boolean>, writeConcern: <document>
    }
)
```

- query :（可选）删除的文档的条件。
- justOne : （可选）如果设为 true 或 1，则只删除一个文档。默认false
- writeConcern :（可选）抛出异常的级别。

示例

删除年龄为23的数据

```
db.example.remove({"age": 23})
```

如果有多个记录且要删除的只有第一条记录，那么设置remove()方法中justOne参数设置1或者是true

```
db.example.remove({"age": 18},1)
或者
db.example.remove({"age": 18}, {justOne:1})
```

### deleteOne

只会删除一条

```
db.example.deleteOne({"age": 18})
```

deleteMany

删除多条

```
db.example.deleteMany({"age":18})
```



