# hash索引、B+树索引、主键索引、非主键索引

## 什么叫回表查询

假设如下创建的一张表：

```mysql
create table xyz(
    id int primary key, 
    k int not null, 
    name varchar(16),
    index (k)
)engine = InnoDB;
```

并插入几条测试数据。

```mysql
INSERT INTO xttblog(id, k, name) VALUES(1, 2, 'aaa'),
    (2, 1, 'bbb'),
    (3, 3, 'ccc');
```


假设，现在我们要查询出 id 为 2 的数据。那么执行 `select * from xttblog where ID = 2;` 这条 SQL 语句就不需要回表。原因是根据主键的查询方式，则只需要搜索 ID 这棵 B+ 树。<font color=red>主键是唯一的，根据这个唯一的索引，MySQL 就能确定搜索的记录。</font>

但当我们使用 k 这个索引来查询 k = 2 的记录时就要用到回表。`select * from xttblog where k = 2; `原因是通过 k 这个普通索引查询方式，则需要<font color=red>先搜索 k 索引树，然后得到主键 ID 的值为 1，再到 ID 索引树搜索一次</font>。这个过程虽然用了索引，但实际上底层进行了两次索引查询，这个过程就称为<font color=red>回表</font>。

## Hash索引

在理想的情况下，key非常分散，不存在Hash碰撞的话，采用Hash索引可以唯一得确定一个key的位置，并且这个位置上就只有一个key，所以查找时间复杂度是**O（1）**，非常快，这是Hash索引的最主要优势。

但是呢，Hash索引不是没有缺点，<font color=green>不存在Hash碰撞这是理想情况</font>，通常情况下，同一个Hash值都不只有一个key，也就是说你根据一个key找到了他的hash值位置之后，但是这个位置还有别的key，所以你还得从这个位置找到真正的key，至于怎么找，这个和具体的hash碰撞处理方式有关，最常用的<font color=green>扩展链表法</font>，就是在hash位置上放置链表，此时，就存在一个链表查询的过程，如果hash碰撞比较严重，查询的时间复杂度就远不止O(1)，那么hash索引的优势就失去了。

其次，<font color=green>Hash索引是不排序的，因此它只适用于等值查询</font>，如果你要查询一定的范围内的数据，那么hash索引是无能为力的，只能把数据挨个查，而不能仅仅是查询到头尾数据之后，从头读到位。

并且，hash索引<font color=green>也无法根据索引完成排序, 因为hash函数的不可预测</font>.这也是它的不足之一。hash索引任何时候<font color=green>都避免不了回表查询</font>数据.

## B+树索引

<font color=orange>稳定，B+树是一颗严格平衡搜索的树</font>，从<font color=orange>根节点到达每一个叶子节点的路径长度都是一样</font>的，并且每个节点可以有多个孩子节点（<font color=orange>高扇出</font>），所以可以尽可能的把树的高度降到很低。这么做的好处是可以降低读取节点的次数，这就是的B+树非常适合做外部文件索引了。在外部文件索引中，必须要读取到一个节点之后，才能知道它所有的孩子几点的位置，而读取一个节点对应一次IO，所以读取叶子节点的IO数就等于树的高度了，因此树的高度越低，所需要的IO次数就越少。B+树是一颗搜索树，所有的数据都放在叶子节点上，并且这些数据是按顺序排列的。所以在范围查询中，只需要找到范围的上下界节点，就可以得到整个范围内的数据，而且还有一个好处，由于这些数据都是排好序的，所以<font color=orange>无需对数据进行再次排序</font>。

<font color=orange>主键索引和非主键索引的区别</font>是：<font color=orange>非主键索引的叶子节点存放的是主键</font>的值，而<font color=orange>主键索引的叶子节点存放的是整行数据</font>，其中非主键索引也被称为二级索引，而<font color=orange>主键索引也被称为聚簇索引</font>。

## 总结：

1.Hash索引在不存在hash碰撞的情况下，之需一次读取，查询复杂度为O（1），比B+树快。

2.但是Hash索引是无序的，所以只适用于等值查询，而不能用于范围查询，自然也不具备排序性。根据hash索引查询出来的数据，还有再次进行排序

3.B+树索引的复杂度等于树的高度，一般为3-5次IO。但是B+树叶子节点上的数据是排过序的，因此可以作用于范围查找，而且查询的数据是排过序的，无需再次排序。对于像`SELECT xxx FROM TABLE1 WHERE xxx LIKE 'aaa%'`这样涉及到模糊匹配的查询，本质上也是范围查询。

4.还有一点，数据库中的多列索引中，只能用B+树索引。数据在B+树的哪个结点上，只取决于最左边的列上的key，在结点中在一次按照第二列、第三列排序。所以B+树索引有<font color=blue>最左原则</font>的特性。
