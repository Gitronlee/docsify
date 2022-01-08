# Go 语言高级编程笔记

本文记录读《Go语言高级编程》（ 作者 *柴树杉 曹春晖*）时的笔记。
## 一、语言基础
### 1.2 “Hello, World”的革命

1. `http.HandleFunc("/", ...)`的意思为：针对根路径/请求注册了响应处理函数
2. 通过`http.ListenAndServe()`函数调用来启动HTTP服务

### 1.3 数组、字符串和切片

1. <font color=red>字符串赋值</font>只是复制了数据地址和对应的长度，而<font color=red>不会导致底层数据的复制</font>。因为字符串结构由两个信息组成：第一个是字符串指向的底层字节数组；第二个是字符串的字节的长度。<font color=red>字符串其实是一个结构体</font>，因此字符串的赋值操作也就是reflect.StringHeader结构体的复制过程，并不会涉及底层字节数组的复制。可以将字符串数组看作一个结构体数组。
2. 切片的行为更为灵活，<font color=red>切片的结构和字符串结构类似，但是解除了只读限制</font>。
3. 切片赋值和函数传参时也是将<font color=red>切片头信息部分</font>按传值方式处理
4. 因为切片头含有底层数据的指针，所以它的赋值也不会导致底层数据的复制。
5. Go语言的赋值和函数传参规则很简单，除闭包函数以引用的方式对外部变量访问之外，其他赋值和函数传参都是以传值的方式处理。
6. 因为数组的长度是数组类型的一部分，<font color=red>不同长度或不同类型的数据组成的数组都是不同的类型</font>，所以在Go语言中很少直接使用数组（不同长度的数组因为类型不同无法直接赋值）
7. 以<font color=red>索引的方式来初始化数组</font>的元素,如定义长度为6的int型数组，元素为1,2,0,0,5,6
`var d =[...]int{1,2,4:5,6}`，这里索引4到5被赋为零值。数组的长度以出现的最大的索引为准，没有明确初始化的元素用零值初始化。
8. Go语言中数组是值语义。一个数组变量即表示整个数组，它并不是隐式地指向第一个元素的指针（例如C语言的数组），而是一个完整的值
9. 当一个数组变量被赋值或者被传递的时候，实际上会复制整个数组。
10. 若b是指向数组a的指针，通过b访问数组中元素的写法和a访问数组中元素的写法是类似的，<font color=red>指针语法糖</font>
11. 还可以通过for range来<font color=red>迭代数组指针</font>指向的数组元素。
    ```go
    var a = {1,2,3}//a是一个数组
    //b是指向数组的指针
    fmt. Println(a[0],a[1])//打印数组的前两个元素
    fmt. Println(b[0],b[1])//通过数组指针访问数组元素的方式和通过数组类似
    for i, v range b {//通过数组指针迭代数组的元素
        fmt Println(i, v)
    }
    ```

12. 对数组类型来说，len()和cap()函数返回的结果始终是一样的，都是对应数组类型的长度。
13. 用<font color=red>for range方式迭代</font>的性能可能会更好一些，因为这种迭代可以<font color=red>保证不会出现数组越界</font>的情形，每轮迭代对数组元素的访问时可以省去对下标越界的判断
    ```go
    //长度为0的数组（空数组）在内存中并不占用空间
    var times [5][0]int
    for i, v rang times{
        ...
    }
    ```

14. 一个<font color=red>[5][0]int类型的数组</font>，虽然第一维数组有长度，但是数组的元素[0]int大小是0，因此整个数组占用的<font color=red>内存大小依然是0</font>。不用付出额外的<font color=red>内存代价</font>，我们就通过for range方式实现times次<font color=red>快速迭代</font>。
15. 用空数组作为通道类型可以减少<font color=red>通道元素赋值时的开销</font>。当然，一般更倾向于用无类型的<font color=red>匿名结构体代替空数组</font>：```c2:= make(chan struct {})```
16. 数组类型是切片和字符串等结构的基础，和数组不同的是字符串的元素不可修改，是一个只读的字节数组
17. <font color=red>for range等语法并不能支持非UTF8编码的字符串的遍历</font>。
18. 字符串虽然不是切片，但是支持切片操作，不同位置的切片底层访问的是同一块内存数据
19. 字符串和数组类似，内置的len()函数返回字符串的长度。也可以通过reflect.StringHeader结构访问字符串的长度，如```fmt.Println("len(s):", (*reflect. Stringheader)(unsafe Pointer(&s)).Len) //12```
20. 如果遇到一个错误的UTF8编码输入，将生成一个特别的Unicode字符'\uFFFD'，这个字符在不同的软件中的显示效果可能不太一样，在印刷中这个符号通常是一个黑色六角形或钻石形状，里面包含一个白色的问号“�”。
21. <font color=red>错误编码不会向后扩散是UTF8编码的优秀特性</font>之一
22. 直接遍历原始的字节码，可以<font color=red>将字符串强制转为[]byte字节序列后再进行遍历</font>（这里的转换一般不会产生运行时开销）：
23. []rune其实是[]int32类型，这里的rune只是int32类型的别名
24. 字符串相关的强制类型转换主要涉及[]byte和[]rune两种类型

#### 1.6 常见的并发模式

1. 作为Go并发编程核心的CSP理论的核心概念只有一个：<font color=green>同步通信</font>
2. Go语言将其并发编程哲学化为一句口号：不要通过共享内存来通信，而应通过通信来共享内存。
3. 我们<font color=green>不能直接对一个未加锁状态的sync.Mutex进行解锁</font>，这会导致运行时异常
4. 要等待N个线程完成后再进行下一步的同步操作有一个简单的做法，就是<font color=green>使用sync.WaitGroup来等待一组事件</font>:<font color=green>wg.Add(1)用于增加等待事件的个数</font>，必须确保在后台线程启动之前执行（如果放到后台线程之中执行则不能保证被正常执行到）;调用<font color=green>wg.Done()表示完成一个事件</font>。main()函数的<font color=green>wg.Wait()是等待全部</font>的事件完成。
5. 这种靠休眠方式是无法保证稳定的输出结果的
6. 在传统生产者/消费者模型中，是将消息发送到一个队列中，而发布/订阅模型则是将消息发布给一个主题。[TODO:golang实现一个发布、订阅模型]
7. 我们不仅可以控制最大的并发数目，而且可以<font color=green>通过带缓存通道的使用量和最大容量比例来判断程序运行的并发率。当通道为空时可以认为是空闲状态，当通道满了时可以认为是繁忙状态</font>，这对于后台一些低级任务的运行是有参考价值的。
8. 当有多种方式可解决同一问题时，可以通过适当开启一些冗余的线程，尝试用不同途径（协程）去解决同样的问题，最终<font color=green>以赢者为王的方式提升了程序的相应性能</font>。
9. 并发版本的素数筛
    ```go
    package main

    import "fmt"
    //不断的生成大于2的数
    func GenerateNatural() chan int {
        ch := make(chan int)
        go func() {
            for i := 2; ; i++ {
                ch <- i
            }
        }()
        return ch

    }

    //每个传参为当前素数
    func PrimeFilter(in <-chan int, prime int) chan int {
        out := make(chan int)
        go func() {
            for {
                if i := <-in; i%prime != 0 {
                    out <- i
                }
            }
        }()
        return out
    }
    func main() {
        ch := GenerateNatural()
        for i := 0; i < 100; i++ {
            prime := <-ch
            fmt.Printf("%v: %v\n", i+1, prime)
            //由于PrimeFilter中会开启goroutine 故此处会开启100个goroutine。
            //每个传参为当前素数，GenerateNatural 发生的数字被第一个素数筛完后继续被后续筛，最后才返回到主函数打印。
            ch = PrimeFilter(ch, prime)
        }
    }
    ```

10. 要同时处理多个通道的发送或接收操作，需要使用select关键字（这个关键字和网络编程中的select()函数的行为类似）。当<font color=green>select()有多个分支时，会随机选择一个可用的通道分支，如果没有可用的通道分支，则选择default分支，否则会一直保持阻塞状态</font>。
11. 通过close()来关闭cancel通道，向多个Goroutine广播退出的指令。不过这个程序依然不够稳健：当每个Goroutine收到退出指令退出时一般会进行一定的清理工作，但是退出的清理工作并不能保证被完成，因为main线程并没有等待各个工作Goroutine退出工作完成的机制,可以结合sync.WaitGroup来改进.
12. 在前面素数筛的例子中，GenerateNatural和PrimeFilter()函数内部都启动了新的Goroutine，当main()函数不再使用通道时，后台Goroutine有泄漏的风险。我们可以通过context包来避免这个问题，当main()函数完成工作前，通过<font color=green>调用cancel()来通知后台Goroutine退出，这样就避免了Goroutine的泄漏</font>,下面是改进的素数筛实现：

    ```go
    // 返回生成自然数序列的管道: 2, 3, 4, ...
    func GenerateNatural(ctx context.Context) chan int {
        ch := make(chan int)
        go func() {
            for i := 2; ; i++ {
                select {
                case <- ctx.Done():
                    return
                case ch <- i:
                }
            }
        }()
        return ch
    }
    // 管道过滤器: 删除能被素数整除的数
    func PrimeFilter(ctx context.Context, in <-chan int, prime int) chan int {
        out := make(chan int)
        go func() {
            for {
                if i := <-in; i%prime != 0 {
                    select {
                    case <- ctx.Done():
                        return
                    case out <- i:
                    }
                }
            }
        }()
        return out
    }
    func main() {
        // 通过 Context 控制后台Goroutine状态
        ctx, cancel := context.WithCancel(context.Background())

        ch := GenerateNatural(ctx) // 自然数序列: 2, 3, 4, ...
        for i := 0; i < 100; i++ {
            prime := <-ch // 新出现的素数
            fmt.Printf("%v: %v\n", i+1, prime)
            ch = PrimeFilter(ctx, ch, prime) // 基于新素数构造的过滤器
        }

        cancel()
    }
    ```

#### 1.7 错误和异常

1. 在C语言中，默认采用一个整数类型的errno来表达错误，这样就可以根据需要定义多种错误类型。在Go语言中，<font color=orange>syscall.Errno 就是对应C语言中errno类型的错误</font>
   通过syscall包的接口来修改文件的模式时，如果遇到错误可以通过将err强制断言为syscall.Errno错误类型来处理。
2. 当返回的错误值不是nil时，我们可以通过调用error接口类型的<font color=orange>Error()方法来获得字符串类型的错误信息</font>。
3. Go语言推荐使用recover()函数将内部异常转为错误处理，这使得用户可以真正地关心业务相关的错误处理
4. defer语句可以让我们在打开文件时马上思考如何关闭文件
5. 为了提高系统的稳定性，Web框架（如gin）一般会通过recover来防御性地捕获所有处理流程中可能产生的异常，然后将异常转为普通的错误返回
6. Go语言库的实现习惯：即使在包内部使用了panic，在导出函数时也会被转化为明确的错误值
7. 为了问题定位的方便，同时也为了能记录错误发生时的函数调用状态，我们很多时候希望在出现致命错误的时候保存完整的函数调用信息。同时，为了支持RPC等跨网络的传输，可能需要<font color=orange>将错误序列化为类似JSON格式的数据</font>，然后再从这些数据中将错误解码恢复出来。
8. Go语言中大部分函数的代码结构几乎相同，首先是一系列的初始检查，用于防止错误发生，之后是函数的实际逻辑
9. Go语言作为一个强类型语言，不同类型之间必须要显式地转换（而且必须有相同的基础类型，注意类型别名还是新类型）。但是，Go语言中interface是一个例外：<font color=orange>非接口类型到接口类型，或者接口类型之间的转换都是隐式的</font>。这是为了支持鸭子类型，当然会牺牲一定的安全性。
10. 在异常发生时，如果在defer()中执行recover()调用，它可以捕获触发panic()时的参数，并且恢复到正常的执行流程。在非defer语句中执行recover()调用是初学者常犯的错误。
11. 对recover()函数的调用有着更严格的要求：我们<font color=orange>必须在defer()函数中直接调用recover()</font>，如果defer()中调用的是recover()函数的包装函数的话，异常的捕获工作将失败；同样，在嵌套的defer()函数中调用recover()，也会导致无法捕获异常。
12. 经过了两个函数帧才到达真正的recover()函数，这个时候Goroutine对应的上一级栈帧中已经没有异常信息。<font color=orange>必须要和有异常的栈帧只隔一个栈帧，recover()函数才能正常捕获异常</font>换言之，<font color=orange>recover()函数捕获的是祖父一级调用函数栈帧的异常</font>（刚好可以跨越一层defer()函数）！

## 二、 CGO编程

Go语言通过自带的一个叫CGO的工具来支持C语言函数调用，同时我们可以用Go语言导出C动态库接口给其他语言使用。

### 2.1 快速入门

1. 代码<font color=blue>通过import "C"语句启用CGO特性</font>

    ```go
    package main
    //#include <stdio.h>
    import "C"
    func main() {    
        C.puts(C.CString("Hello, World\n"))
        }
    ```
    这个版本不仅通过import "C"语句启用CGO特性，还包含C语言的<stdio.h>头文件。然后通过cgo包的C.CString()函数将Go语言字符串转换为C语言字符串，最后调用cgo包的C.puts()函数向标准输出窗口打印转换后的C字符串。没有释放使用C.CString创建的C语言字符串会导致内存泄漏。

2. 我们也可以将SayHello()函数放到当前目录下的一个C语言源文件中（扩展名必须是.c）
然后在CGO部分先声明SayHello()函数，其他部分不变：
既然SayHello()函数已经放到独立的C文件中了，我们自然可以将对应的C文件编译打包为静态库或动态库文件供使用
    ```go
    package main
    //void SayHello(const char* s)
    import "C"
    func main(){
        C.SayHello(C.CString("Hello,World!\n"))
    }
    ```
    当代码语句变多时，可以将相似的代码封装到一个个函数中；当程序中的函数变多时，将函数拆分到不同的文件或模块中。而<font color=blue>模块化编程的核心是面向程序接口编程</font>在hello.c文件的开头，实现者通过#include "hello.h"语句包含SayHello()函数的声明，这样可以保证函数的实现满足模块对外公开的接口
3. 其实CGO不仅用于Go语言中调用C语言函数，还可以用于导出Go语言函数给C语言函数调用.我们通过CGO的`//export SayHello`指令<font color=blue>将Go语言实现的函数SayHello()导出为C语言函数</font>
4. 在Go 1.10中CGO新增加了一个_GoString_预定义的C语言类型，用来表示Go语言字符串。
5. main()函数和SayHello()函数是否在同一个Goroutine里执行？

### 2.2 CGO基础

后续更新~

## 四、 RPC和Protobuf

Protobuf由于支持多种不同的语言（甚至不支持的语言也可以扩展支持），其本身特性也非常方便描述服务的接口（也就是方法列表），因此非常适合作为RPC世界的接口交流语言。

### 4.1 RPC入门

1. <font color=purple>RPC是远程过程调用</font>的简称，是分布式系统中不同节点间流行的通信方式。Go语言的RPC包的路径为net/rpc，也就是放在了net包目录下面。

2. Go语言的RPC规则：方法只能有两个可序列化的参数，其中第二个参数是指针类型，并且返回一个error类型，同时必须是公开的方法。其中rpc.RegisterName()函数调用会将对象类型中所有满足RPC规则的对象方法注册为RPC函数，所有注册的方法会放在HelloService服务的空间之下。首先是通过rpc.Dial拨号RPC服务，然后通过client.Call()调用具体的RPC方法。在调用client.Call()时，第一个参数是用点号链接的RPC服务名字和方法名字，第二个和第三个参数分别是定义RPC方法的两个参数。

---待更新~

