# make和new之间区别与联系

1. 关键字new的函数声明
`func new(Type) *Type` Type是指变量的类型，new会根据变量类型返回一个指向该类型的指针。

2. new底层调用的是 runtime.newobject 申请内存空间， newobject 的底层调用 mallocgc 在**堆上** 按照 type.size 的大小申请内存，因此new只会为结构体申请一片内存空间，不会为结构体中的指针申请内存空间，所以对成员指针解引用操作，就因为访问无效的内存空间而出现 panic。

3. 例如 由于切片的底层为：
    ```go
    type slice struct {
    array unsafe.Pointer    //指向用于存储切片数据的指针
    len   int
    cap   int
    }
    ```
    new 切片时，只会为结构体 slice 申请内存，而不会为当中的 array 字段申请内存，因此用 (*nums)[0] 取指会发生 panic 。因此如果需要对<font color=red>`slice`、`map`、`channel`进行内存申请，则必须使用`make`申请内存</font>

4. **相同点**

- 都是Go语言中用于内存申请的关键字

- 底层都是通过<font color=red>mallocgc</font>申请内存

5. **不同点**

- <font color=red>`make`返回点是复合结构体本身而`new`返回的是指向变量内存的指针</font>

- <font color=red>`make`**只能**为`channel`，`slice`，`map`申请内存空间</font>


