[目录](../目录.md)

# 关于IO编程 #
IO在计算机中指Input/Output，也就是输入和输出

由于程序在运行时，数据是驻留在内存中并由CPU这个超快的计算核心来执行，涉及到数据交换的地方，通常需要磁盘读写、网络传输等，这样就需要IO接口

操作IO的能力都是由操作系统提供的，每一种编程语言(包括Python)都会把操作系统提供的低级C接口封装起来方便使用

# 流 #
IO编程中，有一个很重要的概念叫Stream(流)，可想象其是一个水管，数据就是水管里的水，但只能单向流动\
Input Stream就是数据从外面(磁盘、网络)流进内存，Output Stream就是数据从内存流到外面去\
对于浏览网页来说，浏览器和新浪服务器之间至少需要建立两根水管，才可既能发数据，又能收数据

# 同步IO和异步IO #
由于CPU和内存的速度远远高于外设的速度，因此会存在严重的速度不匹配问题\
例如，要把100M的数据写入磁盘，CPU输出100M的数据只需要0.01秒，可是磁盘要接收这100M数据可能需要10秒，对此有两种办法：
- **同步IO**\
  就是让CPU等待，即程序暂停执行后续代码，等100M的数据在10秒后写入磁盘，再接着往下执行
- **异步IO**\
  就是不让CPU等待，即程序继续执行后续代码，至于100M的数据让其慢慢往磁盘写

# 异步IO #
异步IO的性能远远高于同步IO，但是复杂程度也远远高于同步IO\
异步IO主要有以下两种模式：
- **回调模式**\
  启动类启动线程类后，线程类执行结束后会直接调用回调方法，表示线程执行结束，启动类不需要不断的确认线程是否结束
- **轮询模式**\
  启动类启动线程类后，线程类执行结束后不会调用回调方法，因此启动类需要不断监听线程类是否结束(如通过循环)
