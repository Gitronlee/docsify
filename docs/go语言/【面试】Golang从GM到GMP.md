# Golang从GM到GMP


## 一、GM模型
1. GM概述
在12年的go1.1版本之前用的都是GM模型，但是由于GM模型性能不好，饱受诟病。之后对调度器改进变成了现在的GMP模型。
GM模型中的G全称为Goroutine协程，M全称为Machine内核级线程，调度过程如下
<font color=red>M(内核线程)从加锁的Goroutine队列中获取G(协程)执行，如果G在运行过程中创建了新的G，那么新的G也会被放入全局队列中</font>。
2. GM缺点
缺点:一是调度，返回G都需要获取队列锁，形成了<font color=red>激烈的锁竞争</font>。二是M转移G没有把资源最大化利用，<font color=red>局部性较差</font>。比如当M1在执行G1时，M1创建了G2，为了继续执行G1，需要把G2交给M2执行，因为G1和G2是相关的，而寄存器中会保存G1的信息，因此G2最好放在M1上执行，而不是其他的M。

## 二、GMP
1. GMP概述
G全称为Goroutine协程，M全称为Machine内核级线程，P全称为Processor协程运行所需的资源，即在原GM的基础上增加了一个P层（处理器）。
<font color=green>全局队列</font>：当P中的本地队列中有协程G溢出时，会被放到全局队列中。
<font color=green>P的本地队列</font>：P内置的G队列，存的数量有限，不超过256个。这里有俩种特殊情况。一是当队列P1中的G1在运行过程中新建G2时，G2优先存放到P1的本地队列中，如果队列满了，则会把P1队列中一半的G移动到全局队列。二是如果<font color=green>P的本地队列为空，那么他会先到全局队列中获取G</font>，如果全局队列中也没有G，则会尝试从其他线程绑定的P中<font color=green>偷取</font>一半的G。
<font color=green>P的数量</font>：由启动时环境变量$GOMAXPROCS或者是由runtime的方法GOMAXPROCS()决定。在确定了P的最大数量n后，运行时系统会根据这个数量创建n个P。
<font color=green>M的数量</font>：go程序启动时，会设置M的最大数量，默认10000。但是内核很难创建出如此多的线程，因此默认情况下M的最大数量取决于内核。也可以调用runtime/debug中的SetMaxThreads函数，手动设置M的最大数量。内核级线程的初始化是由内核管理的，当没有足够的M（如休眠中的M）来关联P并运行其中的可运行的G时会请求创建新的M。

2. G在GMP模型中流动过程:
- 调用 go func()创建一个goroutine；
- 新创建的G优先保存在P的本地队列中，如果P的本地队列已经满了就会保存在全局的队列中；
- M需要在P的本地队列弹出一个可执行的G，如果P的本地队列为空，则先会去全局队列中获取G，如果全局队列也为空则去其他P中偷取G放到自己的P中
- G将相关参数传输给M，为M执行G做准备
- 当M执行某一个G时候如果发生了系统调用产生导致<font color=orange>M会阻塞，如果当前P队列中有一些G，runtime会将线程M和P分离</font>，然后再获取空闲的线程或创建一个新的内核级的线程来服务于这个P，阻塞调用完成后G被销毁将值返回；
- 销毁G，将执行结果返回. 当M系统调用结束时候，这个M会尝试获取一个空闲的P执行，如果获取不到P，那么这个线程<font color=orange>M变成休眠状态， 加入到空闲线程</font>中。

## 三、GM与GMP

1. GM与GMP区别
GMP相交于前辈<font color=blue>优化点有三个</font>
- 每个 P 有自己的本地队列，而不是所有的G操作都要经过全局的G队列，这样<font color=blue>大大降低了锁的竞争</font>。而 GM 模型的性能开销大头就是锁竞争。
- P的本地队列平衡上，在 GMP 模型中也实现了 <font color=blue>Work Stealing 算法</font>，如果 P 的本地队列为空，则会从全局队列或其他 P 的本地队列中窃取可运行的 G 来运行（通常是偷一半），<font color=blue>减少空转，提高了资源利用率</font>。
- hand off机制<font color=blue>当M因为G进行系统调用阻塞时，线程释放绑定的P</font>，把P转移给其他空闲的线程M执行，同样也是提高了资源利用率。
2. 队列和线程的优化可以做在G层和M层，<font color=blue>为何还要加一个P层</font>呢？
如果将队列和M绑定，由于hand off机制M会一直扩增，因此队列也需要一直扩增，那么为了使Work Stealing 能够正常进行，队列管理将会变的复杂。因此<font color=blue>设定了P层作为中间层，进行队列管理，控制GMP数量</font>（最大个数为P的数量）。

---
参考 刘丹冰B站视频
