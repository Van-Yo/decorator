# Author:vanyo
import time
# 高阶函数+嵌套函数
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

# 加上修饰器
@timer
def test1():
    time.sleep(3)
    print("in the test1")
@timer
def test2(name):
    time.sleep(3)
    print(name,"in the test2")

# test2 = deco = timer(test2)
test1()
test2('vanyo')