# 一文读完GobyExample

1. for是golang中唯一的循环结构。
1. if else 需要注意else的代码格式：`}else{...`
1. switch case ,在一个case中可以用逗号分隔多个条件，不带表达式的switch是实现if/else的另一种方式
1. len(a)获取数组的长度
1. <font color=red>slice</font>支持比数组更多的操作，<font color=red>内建的append方法，返回新的slice</font>。copy方法复制。slice可以组成多维数据结构，内部的维数可以不同。用make初始化一个slice。
1. map， make初始化一个map，内建的<font color=red>delete方法删除一个kv对</font>，当从map中取值时，可选的第二个参数指示这个键是否存在。
1. range用于迭代各种数据结构。<font color=red>range在字符串中迭代unicode编码，第一个返回值是rune的起始字节位置，然后是rune自己</font>。
    ```go
    for i, v := range "go"{
    //0 103
    //1 111
    fmt.println(i, c)
    }
   ```   
1. 函数是一等公民，支持多返回值，变参函数：当slice有多个值时，想把它们作<font color=red>变参使用，需要`fun(slice...)`的方式展开</font>。
1. 支持通过闭包来使用匿名函数。<font color=red>所谓闭包，就是返回值是一个函数，但是这个函数会带上自己的变量值</font>。
1. 指针，解引用*后赋值操作，&取地址。
1. 结构体指针与结构体访问成员的方式一致都是 . 。可以定义结构体的方法，可以根据值类型或指针类型的结构器定义方法。
1. <font color=red>接口是方法特征的命名集合</font>。结构体类型完全实现了接口的所有方法时，可以使用其实例为接口类型赋值。
1. errors.New()构造一个使用给定的错误信息的基本error值。<font color=red>实现了Error方法，即实现了error接口类型</font>。注意在 if行内的错误检查代码，在 Go 中是一个普遍的用法。
1. 结构体有多个成员，并实现了Error方法，即<font color=red>实现了error接口类型，函数以error返回，通过对返回值的断言为结构体类型，可访问其成员</font>。

1. 这里的 Scanln 代码需要我们在程序退出前按下任意键结束。
    ```go
    var input string
    fmt.Scanln(&input)
   ```   
1. 默认通道是 无缓冲 的，这意味着只有在对应的<font color=red>接收（<- chan）通道准备好接收时，才允许进行发送</font>（chan <-）。可缓存通道允许在没有对应接收方的情况下，缓存限定数量的值。
1. Go 的通道选择器 让你可以同时等待多个通道操作，<font color=red>常规的通过通道发送和接收数据是阻塞的</font>。然而，我们可以使用带一个 <font color=red>default 子句的 select 来实现非阻塞 的发送、接收</font>，甚至是非阻塞的多路 select。
1. 关闭 一个通道意味着不能再向这个通道发送值了。这个特性可以用来给这个通道的接收方传达工作已经完成的信息。使用 j, more := <- jobs 循环的从jobs 接收数据。在接收的这个特殊的二值形式的值中，<font color=red>如果 jobs 已经关闭了，并且通道中所有的值都已经接收完毕，那么 more 的值将是 false</font>。
    ```go
    jobs := make(chan int, 5)
    j, more := <-jobs
    if more {
    }
    ```
1. 这个 range 迭代从 queue 中得到的每个值。因为我们在前面 close 了这个通道，这个迭代会在接收完 2 个值之后结束。如果我们没有 close 它，我们将在这个循环中继续阻塞执行，等待接收第三个值.
    ```go
    for elem := range queue {
        fmt.Println(elem)
    }
    ```
1. 直到这个<font color=red>定时器的通道 C 明确的发送了定时器失效的值之前，将一直阻塞</font>。
    ```go
    timer1 := time.NewTimer(time.Second * 2)
    <-timer1.C 
    stop2 := timer2.Stop() //可提前关闭这个定时器。
    ```
1. 定时器 是当你想要在未来某一刻执行一次时使用的 - 打点器 则是当你想要在固定的时间间隔重复执行准备的。
    ```go
    //新建打点器，每500ms，给t一个信号、1600ms后关闭。
    ticker := time.NewTicker(time.Millisecond * 500)
    go func() {
        for t := range ticker.C {
            fmt.Println("Tick at", t)
        }
    }()
    time.Sleep(time.Millisecond * 1600)
    ticker.Stop()
    ```

1. 在这个例子中，我们将看到如何使用 Go 协程和通道实现一个工作池 。<font color=red>9个任务由3个协程去完成</font>。

    ```go
    package main
    import "fmt"
    import "time"
    //模拟一个工作协程，会遍历jobs的值并取平方
    func worker(id int, jobs <-chan int, results chan<- int) {
        for j := range jobs {
            fmt.Println("worker", id, "processing job", j)
            time.Sleep(time.Second)
            results <- j * 2
        }
    }
    func main() {
    //为了使用 worker 工作池并且收集他们的结果，我们需要2 个通道。
        jobs := make(chan int, 100)
        results := make(chan int, 100)
    //这里启动3个协程去工作，初始是阻塞的，因为还没有传递任务。
        for w := 1; w <= 3; w++ {
            go worker(w, jobs, results)
        }
    //这里我们发送 9 个 jobs，然后 close 这些通道来表示这些就是所有的任务了。
        for j := 1; j <= 9; j++ {
            jobs <- j
        }
        close(jobs)
    //最后，我们收集所有这些任务的返回值。
        for a := 1; a <= 9; a++ {
            <-results
        }
    }
    ```
1. 速率限制是一个重要的控制服务资源利用和质量的途径。Go 通过 Go 协程、通道和打点器优美的支持了速率限制（阻塞一定时间）。
    ```go
    package main
    import "time"
    import "fmt"
    func main() {
        //接收5个请求
        requests := make(chan int, 5)
        for i := 1; i <= 5; i++ {
            requests <- i
        }
        close(requests)
        //设置一个200ms的打点器
        limiter := time.Tick(time.Millisecond * 200)
    //每个任务会被打点器阻塞
        for req := range requests {
            <-limiter
            fmt.Println("request", req, time.Now())
        }
    //若先给3个同时时间
        burstyLimiter := make(chan time.Time, 3)
        for i := 0; i < 3; i++ {
            burstyLimiter <- time.Now()
        }
    //然后继续给200ms打点时间
        go func() {
            for t := range time.Tick(time.Millisecond * 200) {
                burstyLimiter <- t
            }
        }()
    //那么5个任务的阻塞变成了，3个立即，与2个200ms阻塞
        burstyRequests := make(chan int, 5)
        for i := 1; i <= 5; i++ {
            burstyRequests <- i
        }
        close(burstyRequests)
        for req := range burstyRequests {
            <-burstyLimiter
            fmt.Println("request", req, time.Now())
        }
    }
    ```
1. runtime.Gosched()，<font color=red>让当前goroutine让出CPU</font>，好让其它的goroutine获得执行的机会(在自己控制的cpu范围之内让出cpu执行权限，而不是无限制让出)
    ```go
    //原子操作
    atomic.AddUint64(&ops, 1)
    //允许其它 Go 协程的执行
    runtime.Gosched()
    ```
1. 可以使用一个互斥锁来在 Go 协程间安全的访问数据。
    ```go  
    var mutex = &sync.Mutex{} 
    mutex.Lock()
    //xxxx
    mutex.Unlock()
    ```
1. 于 Go <font color=red>协程的实现比基于互斥锁的稍复杂但效率更高</font>。在这个例子中，state 将被一个单独的 Go 协程拥有。select能够保证数据在并行读取时不会混乱。
    ```go
    package main
    import (
        "fmt"
        "math/rand"
        "sync/atomic"
        "time"
    )
    type readOp struct {
        key  int
        resp chan int
    }
    type writeOp struct {
        key  int
        val  int
        resp chan bool
    }
    func main() {
        var ops int64
    //reads 和 writes 通道分别将被其他 Go 协程用来发布读和写请求。
        reads := make(chan *readOp)
        writes := make(chan *writeOp)
    //这个 Go 协程反复响应到达的请求。先响应到达的请求，然后返回一个值到响应通道 resp 来表示操作成功（或者是 reads 中请求的值）
        go func() {
            var state = make(map[int]int)
            for {
                select {
                case read := <-reads:
                    read.resp <- state[read.key]
                case write := <-writes:
                    state[write.key] = write.val
                    write.resp <- true
                }
            }
        }()
    //100读操作
        for r := 0; r < 100; r++ {
            go func() {
                for {
                    read := &readOp{
                        key:  rand.Intn(5),
                        resp: make(chan int)}
                    reads <- read
                    <-read.resp
                    atomic.AddInt64(&ops, 1)
                }
            }()
        }
    // 10 个写操作。
        for w := 0; w < 10; w++ {
            go func() {
                for {
                    write := &writeOp{
                        key:  rand.Intn(5),
                        val:  rand.Intn(100),
                        resp: make(chan bool)}
                    writes <- write
                    <-write.resp
                    atomic.AddInt64(&ops, 1)
                }
            }()
        }
        time.Sleep(time.Second)
        opsFinal := atomic.LoadInt64(&ops)
        fmt.Println("ops:", opsFinal)
    }
    ```
1. 注意排序是原地更新的，所以他会<font color=red>改变给定的序列并且不返回一个新值</font>。
    ```go
        strs := []string{"c", "a", "b"}
        sort.Strings(strs)
        fmt.Println("Strings:", strs)
        ints := []int{7, 2, 4}
        sort.Ints(ints)
        //可以使用 sort 来检查一个序列是不是已经是排好序的。
        s := sort.IntsAreSorted(ints)
    ```
1. 在xxxx类型中<font color=red>实现了 sort.Interface 的 Len，Less和 Swap 方法</font>，这样我们就可以使用 sort 包的通用Sort 方法,```sort.Sort(xxxx)```
1. panic 意味着有些出乎意料的错误发生。
1. Defer 被用来确保一个函数调用在程序执行结束前执行。同样用来执行一些清理工作。 defer 用在像其他语言中的ensure 和 finally用到的地方。
1. 标准库的strings包提供了很多字符串相关的函数：
    ```go
    package main
    import s "strings"
    import "fmt"
    //我们给 fmt.Println 一个短名字的别名，我们随后将会经常用到。
    var p = fmt.Println
    func main() {
    //注意在调用时传递字符作为第一个参数进行传递。
        p("Contains:  ", s.Contains("test", "es"))//是否包含
        p("Count:     ", s.Count("test", "t"))//统计个数
        p("HasPrefix: ", s.HasPrefix("test", "te"))//是否为前缀
        p("HasSuffix: ", s.HasSuffix("test", "st"))//是否后缀
        p("Index:     ", s.Index("test", "e"))//获取下标
        p("Join:      ", s.Join([]string{"a", "b"}, "-"))//连接字符串
        p("Repeat:    ", s.Repeat("a", 5))//重复
        p("Replace:   ", s.Replace("foo", "o", "0", -1))//替换，所有
        p("Replace:   ", s.Replace("foo", "o", "0", 1))//替换，一个
        p("Split:     ", s.Split("a-b-c-d-e", "-"))//分割，以-
        p("ToLower:   ", s.ToLower("TEST"))//全转小写
        p("ToUpper:   ", s.ToUpper("test"))//全转大写
        p()
        p("Len: ", len("hello"))//长度获取
        p("Char:", "hello"[1])//获取坐标的字符
    }
    ```
1. 字符串格式化：
    ```go
    package main
    import "fmt"
    import "os"
    type point struct {
        x, y int
    }
    func main() {
    //这里打印了 point 结构体的一个实例:{1 2}。
        p := point{1, 2}
        fmt.Printf("%v\n", p)
    //%+v 的格式化输出内容将包括结构体的字段名:{x:1 y:2}。
        fmt.Printf("%+v\n", p)

    // %#v 形式则输出这个值的 Go 语法表示: main.point{x:1, y:2}。
        fmt.Printf("%#v\n", p)
    //需要打印值的类型，使用 %T:main.point。
        fmt.Printf("%T\n", p)
    //格式化布尔值是简单的:true。
        fmt.Printf("%t\n", true)
    //格式化整形数有多种方式，使用 %d进行标准的十进制格式化。
        fmt.Printf("%d\n", 123)
    //这个输出二进制表示形式。
        fmt.Printf("%b\n", 14)
    //这个输出给定整数的对应字符。
        fmt.Printf("%c\n", 33)
    //%x 提供十六进制编码。
        fmt.Printf("%x\n", 456)
    //对于浮点型同样有很多的格式化选项。使用 %f 进行最基本的十进制格式化。
        fmt.Printf("%f\n", 78.9)
    // %e 和 %E 将浮点型格式化为（稍微有一点不同的）科学技科学记数法表示形式。
        fmt.Printf("%e\n", 123400000.0)
        fmt.Printf("%E\n", 123400000.0)
    //使用 %s 进行基本的字符串输出。
        fmt.Printf("%s\n", "\"string\"")
    //像 Go 源代码中那样带有双引号的输出，使用 %q。
        fmt.Printf("%q\n", "\"string\"")
    //和上面的整形数一样，%x 输出使用 base-16 编码的字符串，每个字节使用 2 个字符表示。
        fmt.Printf("%x\n", "hex this")
    //要输出一个指针的值，使用 %p。
        fmt.Printf("%p\n", &p)
    //当输出数字的时候，你将经常想要控制输出结果的宽度和精度，可以使用在 % 后面使用数字来控制输出宽度。默认结果使用右对齐并且通过空格来填充空白部分。
        fmt.Printf("|%6d|%6d|\n", 12, 345)
    //你也可以指定浮点型的输出宽度，同时也可以通过 宽度.精度 的语法来指定输出的精度。
        fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45)
    //要左对齐，使用 - 标志。
        fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45)
    //你也许也想控制字符串输出时的宽度，特别是要确保他们在类表格输出时的对齐。这是基本的右对齐宽度表示。
        fmt.Printf("|%6s|%6s|\n", "foo", "b")
    //要左对齐，和数字一样，使用 - 标志。
        fmt.Printf("|%-6s|%-6s|\n", "foo", "b")
    //Sprintf 则格式化并返回一个字符串而不带任何输出。
        s := fmt.Sprintf("a %s", "string")
        fmt.Println(s)
    //你可以使用 Fprintf 来格式化并输出到 io.Writers而不是 os.Stdout。
        fmt.Fprintf(os.Stderr, "an %s\n", "error")
    }
    ```
1. <font color=red>正则表达式</font>：
    ```go
    package main
    import "bytes"
    import "fmt"
    import "regexp"
    func main() {
    //这个测试一个字符串是否符合一个表达式。
        match, _ := regexp.MatchString("p([a-z]+)ch", "peach")
        fmt.Println(match)
    //上面我们是直接使用字符串，但是对于一些其他的正则任务，你需要 Compile 一个优化的 Regexp 结构体。

        r, _ := regexp.Compile("p([a-z]+)ch")
    //这个结构体有很多方法。这里是类似我们前面看到的一个匹配测试。
        fmt.Println(r.MatchString("peach"))
    //这是查找匹配字符串的。
        fmt.Println(r.FindString("peach punch"))//peach
    //这个也是查找第一次匹配的字符串的，但是返回的匹配开始和结束位置索引，而不是匹配的内容。
        fmt.Println(r.FindStringIndex("peach punch"))//[0 5]
    //Submatch 返回完全匹配和局部匹配的字符串。例如，这里会返回 p([a-z]+)ch 和 `([a-z]+) 的信息。
        fmt.Println(r.FindStringSubmatch("peach punch"))
    //类似的，这个会返回完全匹配和局部匹配的索引位置。[0 5 1 3]
        fmt.Println(r.FindStringSubmatchIndex("peach punch"))
    //带 All 的这个函数返回所有的匹配项，而不仅仅是首次匹配项。例如查找匹配表达式的所有项。
        fmt.Println(r.FindAllString("peach punch pinch", -1))
    //All 同样可以对应到上面的所有函数。[[0 5 1 3] [6 11 7 9] [12 17 13 15]]
        fmt.Println(r.FindAllStringSubmatchIndex(
            "peach punch pinch", -1))
    //这个函数提供一个正整数来限制匹配次数。
        fmt.Println(r.FindAllString("peach punch pinch", 2))
    //我们也可以提供 []byte参数并将 String 从函数命中去掉。
        fmt.Println(r.Match([]byte("peach")))
    //创建正则表示式常量时，可以使用 Compile 的变体MustCompile 。因为 Compile 返回两个值，不能用于常量。
        r = regexp.MustCompile("p([a-z]+)ch")
        fmt.Println(r)
    //regexp 包也可以用来替换部分字符串为其他值。
        fmt.Println(r.ReplaceAllString("a peach", "<fruit>"))
    //Func 变量允许传递匹配内容到一个给定的函数中，

        in := []byte("a peach")
        out := r.ReplaceAllFunc(in, bytes.ToUpper)
        fmt.Println(string(out))
    }
    ```
1. 可以解码 JSON 值到自定义类型。这个功能的好处就是可以为我们的程序带来额外的类型安全加强，并且消除在访问数据时的类型断言。
    ```go
        str := `{"page": 1, "fruits": ["apple", "peach"]}`
        res := &Response2{}
        json.Unmarshal([]byte(str), &res)
        fmt.Println(res)
        fmt.Println(res.Fruits[0])
    //在上面的例子中，我们经常使用 byte 和 string 作为使用标准输出时数据和 JSON 表示之间的中间值。我们也可以和os.Stdout 一样，直接将 JSON 编码直接输出至 os.Writer流中，或者作为 HTTP 响应体。
        enc := json.NewEncoder(os.Stdout)
        d := map[string]int{"apple": 5, "lettuce": 7}
        enc.Encode(d)
    ```
1. go的时间支持
    ```go
    package main
    import "fmt"
    import "time"
    func main() {
        p := fmt.Println
    //得到当前时间。
        now := time.Now()
        p(now)//2012-10-31 15:50:13.793654 +0000 UTC
    //通过提供年月日等信息，你可以构建一个 time。时间总是关联着位置信息，例如时区。

        then := time.Date(
            2009, 11, 17, 20, 34, 58, 651387237, time.UTC)
        p(then)//2009-11-17 20:34:58.651387237 +0000 UTC
    //你可以提取出时间的各个组成部分。
        p(then.Year())
        p(then.Month())
        p(then.Day())
        p(then.Hour())
        p(then.Minute())
        p(then.Second())
        p(then.Nanosecond())//毫微秒651387237
        p(then.Location())
    //输出是星期一到日的 Weekday 也是支持的。
        p(then.Weekday())
    //这些方法来比较两个时间，分别测试一下是否是之前，之后或者是同一时刻，精确到秒。
        p(then.Before(now))
        p(then.After(now))
        p(then.Equal(now))
    //方法 Sub 返回一个 Duration 来表示两个时间点的间隔时间。
        diff := now.Sub(then)
        p(diff)
    //我们计算出不同单位下的时间长度值。
        p(diff.Hours())
        p(diff.Minutes())
        p(diff.Seconds())
        p(diff.Nanoseconds())
    //你可以使用 Add 将时间后移一个时间间隔，或者使用一个 - 来将时间前移一个时间间隔。
        p(then.Add(diff))
        p(then.Add(-diff))
    }
    ```
1. 分别使用带 Unix 或者 UnixNano 的 time.Now来获取从自协调世界时起到现在的秒数或者纳秒数。
    ```go
        now := time.Now()
        secs := now.Unix()
        nanos := now.UnixNano()
        //你也可以将协调世界时起的整数秒或者纳秒转化到相应的时间。
        fmt.Println(time.Unix(secs, 0))
        fmt.Println(time.Unix(0, nanos))
    ```
1. 时间的格式化和解析,注意这个特殊时间2006年1月2日下午3时4分5秒
    ```go
    //这里是一个基本的按照 RFC3339 进行格式化的例子，使用对应模式常量。
        t := time.Now()
        p(t.Format(time.RFC3339))//2014-04-15T18:00:15-07:00
        //解析
        t1, e := time.Parse(
            time.RFC3339,
            "2012-11-01T22:08:41+00:00")
        p(t1)//2012-11-01 22:08:41 +0000 +0000
        //Format 和 Parse 使用基于例子的形式来决定日期格式，一般你只要使用 time 包中提供的模式常量就行了，但是你也可以实现自定义模式。模式必须使用时间 Mon Jan 2 15:04:05 MST 2006来指定给定时间/字符串的格式化/解析方式。时间一定要按照如下所示：2006为年，15 为小时，Monday 代表星期几，等等。

        p(t.Format("3:04PM"))
        p(t.Format("Mon Jan _2 15:04:05 2006"))
        p(t.Format("2006-01-02T15:04:05.999999-07:00"))
        form := "3 04 PM"
        t2, e := time.Parse(form, "8 41 PM")
        p(t2)
    ```
1. 随机数
    ```go
    //rand.Float64 返回一个64位浮点数 f，0.0 <= f <= 1.0。
        fmt.Println(rand.Float64())
    //这个技巧可以用来生成其他范围的随机浮点数，例如5.0 <= f <= 10.0
        fmt.Print((rand.Float64()*5)+5, ",")
        fmt.Print((rand.Float64() * 5) + 5)
        fmt.Println()
    //默认情况下，给定的种子是确定的，每次都会产生相同的随机数数字序列。要产生变化的序列，需要给定一个变化的种子。需要注意的是，如果你出于加密目的，需要使用随机数的话，请使用 crypto/rand 包，此方法不够安全。
        s1 := rand.NewSource(time.Now().UnixNano())
        r1 := rand.New(s1)
    ```
1. 数字解析,内置的 <font color=red>strconv 包提供了数字解析功能</font>。
    ```go
    package main
    import "strconv"
    import "fmt"
    func main() {
    //使用 ParseFloat 解析浮点数，这里的 64 表示表示解析的数的位数。
        f, _ := strconv.ParseFloat("1.234", 64)
        fmt.Println(f)
    //在使用 ParseInt 解析整形数时，例子中的参数 0 表示自动推断字符串所表示的数字的进制。64 表示返回的整形数是以 64 位存储的。
        i, _ := strconv.ParseInt("123", 0, 64)
        fmt.Println(i)
    //ParseInt 会自动识别出十六进制数。
        d, _ := strconv.ParseInt("0x1c8", 0, 64)
        fmt.Println(d)
    //ParseUint 也是可用的。
        u, _ := strconv.ParseUint("789", 0, 64)
        fmt.Println(u)
    //Atoi 是一个基础的 10 进制整型数转换函数。

        k, _ := strconv.Atoi("135")
        fmt.Println(k)
    //在输入错误时，解析函数会返回一个错误。
        _, e := strconv.Atoi("wat")
        fmt.Println(e)//strconv.ParseInt: parsing "wat": invalid syntax
    }
    ```
1. URL解析
    ```go
    package main
    import "fmt"
    import "net/url"
    import "strings"
    func main() {
        s := "postgres://user:pass@host.com:5432/path?k=v#f"
    //解析这个 URL 并确保解析没有出错。
        u, err := url.Parse(s)
        if err != nil {
            panic(err)
        }
    //直接访问 scheme。
        fmt.Println(u.Scheme)//postgres
    //User 包含了所有的认证信息，这里调用 Username和 Password 来获取独立值。
        fmt.Println(u.User)//user:pass
        fmt.Println(u.User.Username())
        p, _ := u.User.Password()
        fmt.Println(p)
    //Host 同时包括主机名和端口信息，如过端口存在的话，使用 strings.Split() 从 Host 中手动提取端口。
        fmt.Println(u.Host)//host.com:5432
        h := strings.Split(u.Host, ":")
        fmt.Println(h[0])
        fmt.Println(h[1])
    //这里我们提出路径和查询片段信息。
        fmt.Println(u.Path)
        fmt.Println(u.Fragment)//f
    //要得到字符串中的 k=v 这种格式的查询参数，可以使用 RawQuery 函数。
        fmt.Println(u.RawQuery)//k=v
        m, _ := url.ParseQuery(u.RawQuery)
        fmt.Println(m)//map[k:[v]]
        fmt.Println(m["k"][0])//v
    }
    ```
1. 产生一个散列值得方式是 sha1.New()，sha1.Write(bytes)，然后 sha1.Sum([]byte{})。
1. Base64编码, Go 同时支持标准的和 URL 兼容的 base64 格式。
    ```go
    //编码需要使用 []byte 类型的参数，所以要将字符串转成此类型。
        sEnc := b64.StdEncoding.EncodeToString([]byte(data))
        fmt.Println(sEnc)
    //解码可能会返回错误，如果不确定输入信息格式是否正确，那么，你就需要进行错误检查了。
        sDec, _ := b64.StdEncoding.DecodeString(sEnc)
        fmt.Println(string(sDec))
        fmt.Println()
    //使用 URL 兼容的 base64 格式进行编解码。
        uEnc := b64.URLEncoding.EncodeToString([]byte(data))
        fmt.Println(uEnc)
        uDec, _ := b64.URLEncoding.DecodeString(uEnc)
        fmt.Println(string(uDec))
    ```
1. <font color=red>读文件,ioutil,os,io,bufio等包支持</font>
    ```go
    func main() {
    //大部分基本的文件读取任务是将文件内容读取到内存中。ioutil包
        dat, err := ioutil.ReadFile("/tmp/dat")
        check(err)
        fmt.Print(string(dat))//hello\ngo
    //进行更多的控制。对于这个任务，从使用 os.Open打开一个文件获取一个 os.File 值开始。
        f, err := os.Open("/tmp/dat")
        check(err)
    //从文件开始位置读取一些字节。这里最多读取 5 个字节，并且这也是我们实际读取的字节数。
        b1 := make([]byte, 5)
        n1, err := f.Read(b1)
        check(err)
        fmt.Printf("%d bytes: %s\n", n1, string(b1))
    //你也可以 Seek 到一个文件中已知的位置并从这个位置开始进行读取。
        o2, err := f.Seek(6, 0)
        check(err)
        b2 := make([]byte, 2)
        n2, err := f.Read(b2)
        check(err)
        fmt.Printf("%d bytes @ %d: %s\n", n2, o2, string(b2))//2 bytes @ 6: go
    //io 包提供了一些可以帮助我们进行文件读取的函数。例如，上面的读取可以使用 ReadAtLeast 得到一个更健壮的实现。
        o3, err := f.Seek(6, 0)
        check(err)
        b3 := make([]byte, 2)
        n3, err := io.ReadAtLeast(f, b3, 2)
        check(err)
        fmt.Printf("%d bytes @ %d: %s\n", n3, o3, string(b3))
    //没有内置的回转支持，但是使用 Seek(0, 0) 实现。
        _, err = f.Seek(0, 0)
        check(err)
    //bufio 包实现了带缓冲的读取，这不仅对有很多小的读取操作的能提升性能，也提供了很多附加的读取函数。
        r4 := bufio.NewReader(f)
        b4, err := r4.Peek(5)
        check(err)
        fmt.Printf("5 bytes: %s\n", string(b4))
    //任务结束后要关闭这个文件（通常这个操作应该在 Open操作后立即使用 defer 来完成）。
        f.Close()
    ```
1. <font color=red>写文件，ioutil，os,bufio等包</font>。
    ```go
    func main() {
    //如写入一个字符串（或者只是一些字节）到一个文件。ioutil包
        d1 := []byte("hello\ngo\n")
        err := ioutil.WriteFile("/tmp/dat1", d1, 0644)
        check(err)
    //对于更细粒度的写入，先打开一个文件。os包
        f, err := os.Create("/tmp/dat2")
        check(err)
    //打开文件后，习惯立即使用 defer 调用文件的 Close操作。
        defer f.Close()
    //你可以写入你想写入的字节切片
        d2 := []byte{115, 111, 109, 101, 10}
        n2, err := f.Write(d2)
        check(err)
        fmt.Printf("wrote %d bytes\n", n2)
    //WriteString 也是可用的。
        n3, err := f.WriteString("writes\n")
        fmt.Printf("wrote %d bytes\n", n3)
    //调用 Sync 来将缓冲区的信息写入磁盘。
        f.Sync()
    //bufio 提供了和我们前面看到的带缓冲的读取器一样的带缓冲的写入器。
        w := bufio.NewWriter(f)
        n4, err := w.WriteString("buffered\n")
        fmt.Printf("wrote %d bytes\n", n4)
    //使用 Flush 来确保所有缓存的操作已写入底层写入器。
        w.Flush()
    }
    ```
1. grep 和 sed 是常见的行过滤器。处理标志输入流的输入，将结果输出到标准输出的功能。
    ```go
    func main() {
    //对 os.Stdin 使用一个带缓冲的 scanner，让我们可以直接使用方便的 Scan 方法来直接读取一行，每次调用该方法可以让 scanner 读取下一行。
        scanner := bufio.NewScanner(os.Stdin)
    //Text 返回当前的 token，现在是输入的下一行。
        for scanner.Scan() {
            ucl := strings.ToUpper(scanner.Text())
    //写出大写的行。
            fmt.Println(ucl)
        }
    //检查 Scan 的错误。文件结束符是可以接受的，并且不会被 Scan 当作一个错误。

        if err := scanner.Err(); err != nil {
            fmt.Fprintln(os.Stderr, "error:", err)
            os.Exit(1)
        }
    }
    ```
1. 命令行参数
    ```go
    //os.Args 提供原始命令行参数访问功能。注意，切片中的第一个参数是该程序的路径，并且 os.Args[1:]保存所有程序的的参数。
        argsWithProg := os.Args
        argsWithoutProg := os.Args[1:]
    ```
1. 命令行标志是命令行程序指定选项的常用方式。例如，在 wc -l 中，这个 -l 就是一个命令行标志。
    ```go
    package main
    //Go 提供了一个 flag 包，支持基本的命令行标志解析。我们将用这个包来实现我们的命令行程序示例。
    import "flag"
    import "fmt"
    func main() {
    //基本的标记声明仅支持字符串、整数和布尔值选项。这里我们声明一个默认值为 "foo" 的字符串标志 word并带有一个简短的描述。这里的 flag.String 函数返回一个字符串指针（不是一个字符串值），在下面我们会看到是如何使用这个指针的。
        wordPtr := flag.String("word", "foo", "a string")
    //相同的方法来声明 numb 和 fork 标志。
        numbPtr := flag.Int("numb", 42, "an int")
        boolPtr := flag.Bool("fork", false, "a bool")
    //用程序中已有的参数来声明一个标志也是可以的。注意在标志声明函数中需要使用该参数的指针。
        var svar string
        flag.StringVar(&svar, "svar", "bar", "a string var")
    //所有标志都声明完成以后，调用 flag.Parse() 来执行命令行解析。
        flag.Parse()
    ///这里我们将仅输出解析的选项以及后面的位置参数。注意，我们需要使用类似 *wordPtr 这样的语法来对指针解引用，从而得到选项的实际值。

        fmt.Println("word:", *wordPtr)
        fmt.Println("numb:", *numbPtr)
        fmt.Println("fork:", *boolPtr)
        fmt.Println("svar:", svar)
        fmt.Println("tail:", flag.Args())
    }
    ```
1. 设置，<font color=red>获取并列举环境变量</font>
    ```go
    //使用 os.Setenv 来设置一个键值队。使用 os.Getenv获取一个键对应的值。如果键不存在，将会返回一个空字符串。
        os.Setenv("FOO", "1")
        fmt.Println("FOO:", os.Getenv("FOO"))
        fmt.Println("BAR:", os.Getenv("BAR"))
    //使用 os.Environ 来列出所有环境变量键值队。这个函数会返回一个 KEY=value 形式的字符串切片。你可以使用strings.Split 来得到键和值。这里我们打印所有的键。
        fmt.Println()
        for _, e := range os.Environ() {
            pair := strings.Split(e, "=")
            fmt.Println(pair[0])
        }
    }
    ```
1. 生成进程
    ```go
    package main
    import "fmt"
    import "io/ioutil"
    import "os/exec"
    func main() {
    //exec.Command 函数帮助我们创建一个表示这个外部进程的对象。
        dateCmd := exec.Command("date")
    //.Output 等待命令运行完成，并收集命令的输出。
        dateOut, err := dateCmd.Output()
        if err != nil {
            panic(err)
        }
        fmt.Println("> date")
        fmt.Println(string(dateOut))
    //从外部进程的stdin 输入数据并从 stdout 收集结果。
        grepCmd := exec.Command("grep", "hello")
    //这里我们明确的获取输入/输出管道，运行这个进程，写入一些输入信息，读取输出的结果，最后等待程序运行结束。
        grepIn, _ := grepCmd.StdinPipe()
        grepOut, _ := grepCmd.StdoutPipe()
        grepCmd.Start()
        grepIn.Write([]byte("hello grep\ngoodbye grep"))
        grepIn.Close()
        grepBytes, _ := ioutil.ReadAll(grepOut)
        grepCmd.Wait()
        fmt.Println("> grep hello")
        fmt.Println(string(grepBytes))
    //使用通过一个字符串生成一个完整的命令，那么你可以使用 bash命令的 -c 选项：
        lsCmd := exec.Command("bash", "-c", "ls -a -l -h")
        lsOut, err := lsCmd.Output()
        if err != nil {
            panic(err)
        }
        fmt.Println("> ls -a -l -h")
        fmt.Println(string(lsOut))
    }
    ```
1. 想用其他的（也许是非 Go 程序）来完全替代当前的 Go 进程。这时候，我们可以使用经典的 exec方法的 Go 实现。
    ```go
        binary, lookErr := exec.LookPath("ls")
        if lookErr != nil {
            panic(lookErr)
        }
        args := []string{"ls", "-a", "-l", "-h"}
        env := os.Environ()
        execErr := syscall.Exec(binary, args, env)
    ```
1. 用<font color=red>通道处理信号实现优雅退出</font>。<font color=red>signal.Notify</font> 注册这个给定的通道用于<font color=red>只接收特定信号</font>。
    ```go
    package main
    import "fmt"
    import "os"
    import "os/signal"
    import "syscall"
    func main() {
        sigs := make(chan os.Signal, 1)
        done := make(chan bool, 1)
    //signal.Notify 注册这个给定的通道用于接收特定信号。
        signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
    //这个 Go 协程执行一个阻塞的信号接收操作。当它得到一个值时，它将打印这个值，然后通知程序可以退出。
        go func() {
            sig := <-sigs
            fmt.Println()
            fmt.Println(sig)
            done <- true
        }()
    //程序将在这里进行等待，直到它得到了期望的信号（也就是上面的 Go 协程发送的 done 值）然后退出。

        fmt.Println("awaiting signal")
        <-done
        fmt.Println("exiting")
    }
    ```
1. 当<font color=red>使用 os.Exit(3) 时 defer 将不会 执行</font>.