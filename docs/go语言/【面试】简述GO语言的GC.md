# Golang三色标记、混合写屏障GC

垃圾回收(Garbage Collection，简称GC)是编程语言中提供的自动的内存管理机制，自动释放不需要的对象，让出存储器资源，无需程序员手动执行。

Golang中的垃圾回收主要应用<font color=red>三色标记法</font>，GC过程 和其他用户goroutine可并发运行，但需要一定时间的<font color=red>STW(stop the world)</font>，STW的过程中，CPU不执行用户代码，全部用于垃圾回收，这个过程的影响很大，Golang进行了多次的迭代优化来解决这个问题。

## 一、Go V1.3之前的标记-清除(mark and sweep)算法

此算法主要有两个主要的步骤：<font color=red>标记(Mark phase) 和 清除(Sweep phase)</font> ，操作非常简单，但是：mark and sweep算法在执行的时候，<font color=red>需要程序暂停</font> ！步骤为：

1. <font color=red>暂停</font>程序业务逻辑。

2. 程序<font color=red>找出它所有可达</font>的对象 ，并做上<font color=red>标记</font>。

3. 标记完成，开始<font color=red>清除未标记</font>的对象. 

4. <font color=red>停止暂停</font>，让程序继续跑。

然后循环重复这个过程，直到process程序生命周期结束。

## 二、标记-清扫(mark and sweep)的缺点

1. STW，stop the world；会让<font color=green>程序暂停，程序出现卡顿</font> (重要问题)。

2. <font color=green>标记需要扫描整个heap</font>

3. 清除数据会<font color=green>产生heap碎片</font>

Go V1.3 做了简单的优化 ,将STW提前, <font color=green>减少STW暂停的时间，即重启程序后再清除垃圾</font> 

## 三、Go V1.5的三色并发标记法

三色标记法就是通过三个阶段的标记来确定对象状态，以确定清除时机的方法。

1. 只要是<font color=orange>新创建的对象</font> ,默认的颜色都是标记为<font color=orange>“白色”</font>

2. 每次GC回收开始 , 然后从<font color=orange>根节点开始遍历</font>所有对象，把遍历到的对象从<font color=orange>白色标记为灰色</font>。

3.  <font color=orange>遍历灰色集合</font> ，将<font color=orange>灰色对象引用的对象从白色集合放入灰色集合</font>，之后将此<font color=orange>灰色对象标记为黑色</font> 

4.  <font color=orange>重复</font>第三步, 直到<font color=orange>无灰色</font>对象 .

5. 将<font color=orange>剩余所有的白色标记表的对象回收</font>，也就是回收垃圾.

## 四、没有STW的三色标记法，会有什么问题？

1. 基于<font color=blue>上述的三色并发标记法</font>要正确工作，必须<font color=blue>依赖STW</font> 的. 因为如果不暂停程序, 程序的逻辑改变对象引用关系, 如<font color=blue>在标记阶段做了修改，会影响标记结果的正确性</font>。
如此时，一个白色对象被黑色对象引用 (<font color=blue>白色被挂在黑色下</font>，但黑色对象只保证了自己的可靠，对下游无保护）。<font color=blue>同时</font>，这个白色对象，的<font color=blue>上游某灰色对象与它的可达关系遭到破坏</font>。

(即本将非法化的白色对象同时被合法化) 会导致将被合法对象被错误回收!

2. 为防止这种现象，最简单的方式就是<font color=blue>STW，直接禁止掉其他用户程序对对象引用关系的干扰</font>，但STW的过程有明显的资源浪费，对所有的用户程序都有很大影响，从而影响GC效率。

## 五、屏障机制

屏障机制的引入是为了破坏上述两个条件之一，从而保合法对象不丢失。有两种方式：

1. 强三色不变式，强制<font color=purple>禁止黑色对象引用到白色</font> 对象的指针。

2. 弱三色不变式，允许<font color=purple>黑色对象引用的白色</font>对象但要保证此<font color=purple>白色处于灰色保护</font>状态。

对应上述的两个方式,Golang团队初步得到两种屏障方式“插入屏障”, “删除屏障”：

### 1. 插入屏障

1. 在<font color=purple>A对象引用B对象的时候，先将B对象标记为灰色</font>。满足强三色不变式。
2. 由于栈空间的特点是容量小,但是要求响应速度快,函数调用时弹出频繁使用, 所以“插入屏障”机制,在栈空间的对象操作中不使用. 而<font color=purple>仅仅使用在堆空间对象</font>的操作中.
3. 因此在栈上依然存在合法对象被错误回收的风险。 所以需要<font color=purple>对栈重新进行三色标记扫描</font>, 但这次为了对象不丢失, 要对本次标记<font color=purple>扫描启动STW暂停</font>. 直到栈空间的三色标记结束.最后将栈和堆空间 扫描剩余的全部 白色节点清除. 这次STW大约的时间在10~100ms间.

### 2. 删除屏障   

1. <font color=purple>被删除的对象，如果自身为灰色或者白色，那么被标记为灰色</font>。保证其下游仍在灰色保护下 。满足:弱三色不变式。
这种方式的回收精度低，一个对象即使被删除了最后一个指向它的指针可活过这一轮，在下一轮GC中被清理掉。

## 六、Go V1.8的混合写屏障(hybrid write barrier)机制

1. 插入写屏障和删除写屏障的短板：
<font color=brown>插入写屏障：结束时需要STW来重新扫描栈</font>，标记栈上引用的白色对象的存活 ；
<font color=brown>删除写屏障：回收精度低</font>，GC开始时STW扫描堆栈来记录初始快照 ，这个过程会保护开始时刻的所有存活对象。
Go V1.8版本引入了<font color=brown>混合写屏障机制（hybrid write barrier） ，避免了对栈re-scan的过程</font>，极大的减少了STW的时间。结合了两者的优点。

2. 混合写屏障规则：
- GC开始将栈上的对象全部扫描并标记为黑色(由于栈上不高屏障，这样做可以避免重复扫描，无需STW)
- GC期间，任何在栈上创建的新对象，均为黑色。
- 被删除的对象标记为灰色 。(保证下游可达)
- 被添加的对象标记为灰色。（感觉是提前设置可达0.0）
因为要保证栈的运行效率, 屏障技术是不在栈上应用的。

## 七、总结
1. GoV1.3- 普通标记清除法，整体过程需要启动STW，效率极低。

2. GoV1.5- 三色标记法， 堆空间启动写屏障，栈空间不启动，全部扫描之后，需要重新扫描一次栈(需要STW)，效率普通

3. GoV1.8-三色标记法，混合写屏障机制， 栈空间不启动，堆空间启动。整个过程几乎不需要STW，效率较高。

---
参考 刘丹冰B站视频教程。
