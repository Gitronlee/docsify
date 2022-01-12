# 简述Golang的map实现原理

## 一、map的实现
1. map类型的变量本质上是个指针，这些键值对实际上是<font color=red>通过哈希表来存储</font>的。
2. 当发生哈希冲突时，通常有两种思路来解决<font color=red>一是开放地址法二是拉链法</font>（拉链法中会把发生冲突的键值对用链表结构串起来，按照key查找时，<font color=red>首先根据hash值定位到同一个桶，然后通过比较key的值来锁定键值对</font>。go应该是用的拉链法）
3. map的实现及存储过程
    ```go
    type hmap struct {
        count     int;//已经存储的键值对个数
        flags     uint8
        B         uint8;//常规桶个数等于2^B
        noverflow uint16;//使用的溢出桶数量
        hash0     uint32; //hash seed
        buckets    unsafe.Pointer; //常规桶起始地址
        oldbuckets unsafe.Pointer; //扩容时保存原来常规桶的地址
        nevacuate  uintptr; //渐进式扩容时记录下一个要被迁移的旧桶编号

        extra *mapextra
    }
    ```
- map使用的桶每个桶里可以存储8个键值对，并且为了内存使用更加紧凑，8个tophash、8个键放一起，8个值放一起。
- <font color=red>常规桶个数等于2^B</font>，如果哈希表<font color=red>要分配的桶的数目大于2^4，那么就会预分配2^(B-4)个溢出桶备用</font>。常规桶和溢出桶在内存中是连续的，只是前2^B个用作常规桶，后面的用作溢出桶。
- hmap结构体<font color=red>最后有一个extra字段，指向一个mapextra结构体，记录溢出桶相关</font>的信息。
- 当前桶存满了以后，检查hmap.extra.nextoverflow还有可用的溢出桶，就在这个桶后面链上这个溢出桶，然后继续往这个溢出桶里存。

## 二、负载因子（Load Factor）
1. 哈希表中存储的键值对数量和桶数量的比值，也就是map要扩容的阈值(简单理解为单个桶不能超过6.5个kv)。负载因子默认6.5（Go <font color=green>官方测试发现发现：负载因子太大了，会有很多溢出的桶。太小了，就会浪费很多空间</font>，根据测试报告硬编码为6.5）``` loadFactor = keyCount / bucketCount```
2. 扩容有两种：
- “<font color=green>一次性扩容</font>”，就是一次性把所有键值对挪到新的桶里。但是如果键值对数量很多，每次扩容占用的时间太长就会造成性能<font color=green>瞬时明显抖动</font>，所以通常会选择“渐进式扩容”。
- <font color=green>渐进式扩容方式下</font>，旧桶里的键值对是分多次挪到新桶里的，在触发扩容后，先分配新桶，然后<font color=green>标记当前哈希表正在扩容，并在哈希表的读写操作中判断若在扩容中，则迁移一部分键值</font>对到新桶里

## 三、扩容
### 翻倍扩容过程
1. map的扩容有两种情况，如果<font color=orange>超过负载因子就会触发翻倍扩容</font>。```hmap.count / 2^hmap.B > 6.5```
2. 通过渐进式扩容的方式，<font color=orange>每次读写map时检测到当前map处在扩容阶段`(hmap.oldbuckets != nil)`，就执行一次迁移工作</font>，把编号为hmap.nevacuate 的旧桶迁移到新桶，<font color=orange>每个旧桶的键值对都会分流到两个新桶中</font>
3. 编号为hmap.nevacuate的旧桶迁移结束后会增加这个编号值，直到所有旧桶迁移完毕，把hmap.oldbuckets置为nil，一次翻倍扩容结束.

### 等量扩容
1. 如果常规桶数目不大于2^15，那么使用的溢出桶数目超过常规桶;如果常规桶数目大于2^15，那么使用溢出桶数目一旦超过2^15时触发等量扩容。
这是什么场景呢？其实就是有很多键值对被删除的情况。
2. 把这些键值对重新安排到等量的新桶中，虽然哈希值没变，常规桶数目没变，每个键值对还是会选择与旧桶一样的新桶编号，但是能够存储的更加紧凑.

## 四、其他
1. 在Go语言中<font color=blue>可以通过“==”来比较是否相等的类型，都可以作为map的key类型</font>。而不可比较的类型，例如slice，它的类型元数据里是没有提供可用的equal方法的。因此并不能用作map的key，连带着含有slice的结构体类型也不可以。
2. 因为扩容过程中会发生键值对迁移，键值对的地址也会发生改变，所以才说<font color=blue>map的元素是不可寻址的</font>，如果要取一个value的地址则不能通过编译。