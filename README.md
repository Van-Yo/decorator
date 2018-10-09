# decorator:修饰器
## 修饰器需要用到的知识：修饰器 = 高阶函数 + 嵌套函数（修饰器要不破坏原函数且正常调用原函数）
### 1.先定义两个最基本的函数并且调用函数
```
import time
# 先定义两个函数test1,test2
def test1():
    time.sleep(3)
    print("in the test1")
def test2():
    time.sleep(3)
    print("in the test2")
test1()
test2()
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result1.png)
### 2.现在需要为这两个函数分别添加一个相同的功能：计算函数运行时间,前提是不破坏原函数且正常调用test1(),test2()
尝试 1: 定义一个高阶函数
```
# 该高阶函数deco的作用就是计算函数func运行的时间
def deco(func):
    start_time = time.time()
    func()
    stop_time = time.time()
    print("the func's running time is %s" % (stop_time-start_time))
# 将前面的test1(),test2()改成deco(test1),deco(test2)调用高阶函数
deco(test1)
deco(test2)
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result2.png)
### 3.结果显示两个test函数分别都加入新功能，并且没有去修改原函数，但是，调取函数的时候并不是用的test1(),test2(),因此不符合修饰器的定义
尝试 2: 将高阶函数中的func()改成return func,表示将参数的函数地址返回
```
def deco(func):
    start_time = time.time()
    # func()改成return func
    return func
    stop_time = time.time()
    print("the func's running time is %s" % (stop_time-start_time))
# 新取一个test1,test2的名字,实现偷梁换柱的效果(将尝试1中的函数调用方式换成下面的)
test1 = deco(test1)
test1()
test2 = deco(test2)
test2()
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result3.png)
### 4.可以发现这时候return的特性就发挥出来了：一旦return，后面的语句将不再运行；到目前为止，只运用到高阶函数，嵌套函数还未使用，嵌套函数的格式：
```
def timer():
    def deco():
        pass
    return deco
```
尝试 3: 将嵌套函数运用到高阶函数中
```
# 高阶函数+嵌套函数
def timer(func):
    def deco():
        start_time = time.time()
        func()
        stop_time = time.time()
        print("the func's running time is %s" % (stop_time-start_time))
    return deco
# timer(test1)返回的是函数deco的内存地址，赋值给一个新命名的test1,偷梁换柱
# 流程是：先timer(test1),然后deco(),接着直接到return deco(表示到目前为止，只知道创建了一个deco函数的内存，由于没有调用该函数，所以函数体暂时无需运行)
# 所以timer(test1)返回的是deco函数的内存地址，然后取一个同名test1，将deco的内存地址赋值给test1
test1 = timer(test1)
# 然后test1()表示运行函数，实际上是运行deco,即deco()
test1()
test2 = timer(test2)
test2()
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result4.png)
### 5.到目前为止，已经实现了我们的需求，铺垫了这么多，就是为了引入修饰器,这样调用函数的时候就简单的多，不需要赋值地址
尝试 4：加上修饰器
```
# 加上修饰器：在每个函数前面加上@{嵌套函数名}
@timer
def test1():
    time.sleep(3)
    print("in the test1")
@timer
def test2():
    time.sleep(3)
    print("in the test2")
    
# test1 = timer(test1)
test1()
test2()
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result5.png)
### 6.这样，一个最简单的修饰器就实现了，但是，我们发现我们命名的test1,test2函数过于简单，都没有形参，一旦有参数，修饰器会出现什么问题，应该怎么修改
尝试 5：修改函数test2()，和修改调用test2()
```
# 给test2传入一个参数name
@timer
def test2(name):
    time.sleep(3)
    print(name,"in the test2")
# 调用test2,先把test1()注销
# test1()
# test2 = deco = timer(test2)
test2('vanyo')
```
输出结果（报错）：TypeError: deco() takes 0 positional arguments but 1 was given,表示deco函数需要传入一个参数

### 7.之前就已经说过timer(test1)返回的是deco的内存地址，即timer(test2)等于deco,而又test2 = timer(test2)，就相当于将deco的地址赋值给新命名的test2
### 现在我们调用test2('vanyo')就可以简单理解成deco('vanyo'),也就是说test传入的参数是和deco挂钩的
尝试 6：修改修饰器
```
def timer(func):
    # 传入name参数
    def deco(name):
        start_time = time.time()
        # 这里的func就是timer(func)里面的func，timer(test2)在这里就会运行test2(),非偷梁换柱里命名的test2
        # test2(name)传入了一个参数，因此这里对应也应改传入一个参数
        func(name)
        stop_time = time.time()
        print("the func's running time is %s" % (stop_time-start_time))
    return deco
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result6.png)
### 8.最后我们将test1()也解注了，test1()没有传入任何参数
```
test1()
```
输出结果（报错）：TypeError: deco() missing 1 required positional argument: 'name'，原因就是test1()少了一个参数，而与之挂钩的deco需要一个参数

### 9.那针对这种不确定数量参数的修饰器该怎么改呢
尝试 7：传入#args,##kwargs
```
def timer(func):
    # 传入name参数
    def deco(*args,**kwargs):
        start_time = time.time()
        # 这里的func就是timer(func)里面的func，timer(test2)在这里就会运行test2(),非偷梁换柱里命名的test2
        # test2(name)传入了一个参数，因此这里对应也应改传入一个参数,最后改成*args,**kwargs
        func(*args,**kwargs)
        stop_time = time.time()
        print("the func's running time is %s" % (stop_time-start_time))
    return deco
```
输出结果：<br>
![temple1](https://github.com/Van-Yo/decorator/blob/master/result7.png)




