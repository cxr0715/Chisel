# 从断点到LLDB再到Chisel



## 1.断点

Xcode断点有很多种类型，这里主要介绍一下以下的几种



### 1.普通断点

既在代码中点击某一行，程序运行到改行既中止

其实每下一个断点是在xcdebugger的Breakpoints_v2.xcbkptlist文件中添加了一些配置项，如下表示一个全局的异常断点

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Bucket
   type = "0"
   version = "2.0">
   <Breakpoints>
      <BreakpointProxy
         BreakpointExtensionID = "Xcode.Breakpoint.ExceptionBreakpoint">
         <BreakpointContent
            shouldBeEnabled = "Yes"
            ignoreCount = "0"
            continueAfterRunningActions = "No"
            scope = "0"
            stopOnStyle = "0">
         </BreakpointContent>
      </BreakpointProxy>
   </Breakpoints>
</Bucket>
```



### 2.全局断点

可以点击Xcode左下角的加号添加一个"Exception Breakpoint"全局断点，值得注意的是，在手Y中添加全局断点每次程序启动的时候都会断到main函数中，这里我们只要下一个oc类型的全局断点就可以避免这个问题

![](http://zonemin.bs2cdn.yy.com/DebugPhoto_2.png)



### 3.条件断点

在下的断点处右键（双击）点击Edit Breakpoint弹出断点编辑窗口，填写具体条件，只有当程序运行到断点处并且满足条件的时候才会触发。

![](http://zonemin.bs2cdn.yy.com/DebugPhoto_3.png)



#### 1.Edit Breakpoint：



##### 1.Condition：

满足表达式的情况就会触发断点



##### 2.Ignore：

忽然多少次后触发



##### 3.Action：

可以在触发断点后执行一些操作，主要有包括几种操作：

AppleScript（执行一些苹果脚本）、Capture GPU Frame（断点后捕获GPU当前帧）、Debug Commond（执行一些LLDB命令）、Log Message（打印一些信息到控制台，也可以输出语音）、Shell Commond（异步执行一些shell脚本）、Sound（发出提示音）

```shell
display dialog "Hello World"
```



##### 4.Options：

勾选后断点不会触发程序中断



### 4.符号断点

可以在当程序执行指定方法时候下断点，介绍一个UIButton点击的符号断点的例子：

```lldb
po [button allTargets]
po [button actionsForTarget:(id)targets地址 forControlEvent:0]
```

拿到button相关信息之后去下button的点击符号断点



### 5.共享断点

可以在小组内分享你的本地断点，会把之前介绍的在xcdebugger中生成的xml配置文件加入到版本记录中，从而分享出去你的本地断点，值得注意的一点是现在的断点都是下在xcworkspace中，但是xcworkspace是没有加入版本追踪的，所以手Y的共享断点需要先move breakpoint to 相应的project中，才可以共享出去。

![](http://zonemin.bs2cdn.yy.com/DebugPhoto_4.png)

## 2.LLDB

Xcode在4.3版本之后接入了LLDB（之前使用的是GDB），包括了很多种内置的调试指令，主要介绍以下几种：



### 1.help

help <expr>

会列举出所有的相关指令，例如help thread会列举出所有thread相关的指令，可以使用help查看一些具体的指令。



### 2.print po

print <expr>

用于打印基本类型，例如：可以使用以下指令打印当前vc的view的子view个数

print也可以缩写为p，p指令会返回命令结果的引用名

```
print (int)((NSArray *)self.view.subviews).count
(int) $1 = 2
```

po <expr>

用于打印对象，例如：可以使用如下指令打印当前vc的view的子view的个数

po只会输出指令的结果

```
po ((NSArray *)self.view.subviews).count
2
```



### 3.expression

expression [-O] -- <expr>

expression <expr>

可以在调试的时候动态执行表达式，并且显示执行结果。缩写为e，expr

使用该指令可以动态的修改一些程序中的数值，执行一些语句，动态的修改一些UI等。和之前介绍的编辑断点action结合起来使用可以做到修改一些数值，修改一些UI而不需要重新build整个项目，例如：执行以下指令就可以在不重新build项目的情况下动态修改右下角的button为“支持我”

```
e self.isArenaRedOrBlueRoom = YES
e self.notifyInfo.state = 1
e self.notifyInfo.type = 5
```

修改giftBtn的背景色：
```
e self.giftBtn.backgroundColor = [UIColor redColor]
e [CATransaction flush] #刷新操作
```

也可以自己在lldb中通过e指令new一些临时变量

```
e int $a = 2
e NSString *$aa = @"aaa"
# “$”表示变量
```



### 4.thread

thread <expr>

用于操作一个或多个线程的命令

```
thread return xxx 
#退出当前的栈帧，返回xxx，可以用来短路函数，但是在使用的过程要注意可能#会造成ARC内存计数错误，所以一般在函数开头使用，短路改函数
```

可以使用thread return加共享断点实现模拟器开播

短路YYMobileLivePreViewController中的isAllPermissionsGranted方法即可

不过Xcode10的iOS12模拟器已经可以获取到麦克风权限了，可以直接模拟器开播了，Xcode9、iOS11及以下的模拟器可以使用这个方法使模拟器可以开播

```
thread list #显示当前APP中每个线程的摘要
thread continue 线程号 #可以继续执行指定的线程
```



### 5.watchpoint内存断点

watchpoint <expr>

watchpoint set exprssion 地址 #对该地址下断点，修改到该地址即程序会产生中断

watchpoint set variable 变量 #对改变量下断点，修改到该变量即程序会产生中断

watchpoint set expression -w read -- 地址 #访问到该地址即会产生中断

watchpoint set variable -w read 变量 #访问到该变量即会产生中断



## 3.Chisel

[Chisel介绍](https://github.com/facebook/chisel)

Chisel是facebook的一款开源lldb插件，主要使用Python实现，集成了多种功能，可以使调试更加便捷。

### 1.安装Chisel

通过[homebrew](https://brew.sh/)快速安装

```shell
brew install chisel
```

安装之后按照提示在~/.lldbinit中添加，重启xcode即可

```
command script import /usr/local/opt/chisel/libexec/fblldb.py
```

### 2.chisel指令

#### 1.pviews/pvc

递归打印view/viewcontroller，相当于私有方法[view recursiveDescription]/[UIViewController _printHierarchy]

#### 2.visualize

visulize可以在mac的预览中打开指定view

#### 3.fv/fvc

搜索查找当前内存中的view和viewcontroller

### 3.自定义命令

我们也可以自定义一些脚本命令，来实现一些简单的调试输入输出

需要在lldbinit中添加一行脚本加载路径

```
script fblldb.loadCommandsInDirectory('/Users/yyinc/Desktop/example')
```

#### 1.打印指定view的在subview中的序号

pviewlevel view view

```python
#!/usr/bin/python
# Example file with custom commands, located at /magical/commands/example.py

import lldb
import fblldbbase as fb
import pdb


def lldbcommands():
    return [PrintViewLevel()]


class PrintViewLevel(fb.FBCommand):
    def name(self):
        return 'pviewlevel'

    def description(self):
        return 'View in subviews level.'

    def args(self):
        return [
            fb.FBCommandArgument(arg='subviews', type='UIView *', help='This is subviews.'),
            fb.FBCommandArgument(arg='view', type='UIView *', help='This is view')
        ]


#   def options(self):
#     return [
#       fb.FBCommandArgument(short='-s', long='--subviews', arg='color', type='string', default='red', help='A color name such as \'red\', \'green\', \'magenta\', etc.'),
#       fb.FBCommandArgument(short='-w', long='--width', arg='width', type='CGFloat', default=2.0, help='Desired width of border.')
#     ]

    def run(self, arguments, options):
        # It's a good habit to explicitly cast the type of all return
        # values and arguments. LLDB can't always find them on its own.
        subviews = fb.evaluateInputExpression(arguments[0])
        # subviews = subviewsOfView(selfView)
        view = fb.evaluateInputExpression(arguments[1])

        index = fb.evaluateIntegerExpression('[[' + subviews + ' subviews] indexOfObject:' + view + ']')
        # index = fb.evaluateIntegerExpression('[(id)' + subviews + '.subviews indexOfObject:' + view + ']')

        # index = fb.evaluateExpression('[(UIView *)%s.subviews indexOfObject:(UIView *)%s]' % (subviews, view))

        # pdb.set_trace()
        print ('index: %d' % index)
        # lldb.debugger.HandleCommand('po [((UIView *)%s).subviews indexOfObject:((UIView *)%s)]' % (arguments[0], arguments[1]))

    def subviewsOfView(view):
        return fb.evaluateObjectExpression('[' + view + ' subviews]')

```

#### 2.GetCore等宏输出

因为宏定义在预编译的时候会进行宏展开，所以在运行时使用宏是无效的，所以使用自定义脚本实现了一些宏在运行时可以使用查看

GetCore CoreName 方法/属性名，

GetCoreI ICoreName 方法/属性名，

BRIDGE BRIDGEName 方法/属性名

```python
#!/usr/bin/python
# Example file with custom commands, located at /magical/commands/example.py

import lldb
import fblldbbase as fb
import pdb


def lldbcommands():
    return [
        GetCoreMacro(),
        GetCoreIMacro(),
        BRIDGEMacro(),
        ]


class GetCoreMacro(fb.FBCommand):
    def name(self):
        return 'GetCore'

    def description(self):
        return 'GetCore Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='GetCore', type='string', help='This is Core Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is Core Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        coreName = fb.evaluateExpression('((' + arguments[0] + ' *)[CoreManager getCore:[' + arguments[0] + ' class]])')
        result = fb.evaluateObjectExpression('(id)[' + coreName + ' %s]' % arguments[1])
        print ('result: {}'.format(result))
        print ('<{}: {}>'.format(arguments[0], coreName))
        lldb.debugger.HandleCommand('po [(%s *)%s %s]' % (arguments[0], coreName, arguments[1]))


class GetCoreIMacro(fb.FBCommand):
    def name(self):
        return 'GetCoreI'

    def description(self):
        return 'GetCoreI Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='GetCoreI', type='string', help='This is CoreI Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is CoreI Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        coreName = fb.evaluateExpression('[CoreManager getCoreFromProtocol:(Protocol *)objc_getProtocol("'+ arguments[0] +'")]')
        print ('<{}: {}>'.format(arguments[0], coreName))
        lldb.debugger.HandleCommand('po [%s %s]' % (coreName, arguments[1]))

        
class BRIDGEMacro(fb.FBCommand):
    def name(self):
        return 'BRIDGE'

    def description(self):
        return 'BRIDGE Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='BRIDGE', type='string', help='This is BRIDGE Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is BRIDGE Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        bridgeName = fb.evaluateExpression('[[YYBridgeSet shareInstance] getBridgeWithProtocol:(Protocol *)objc_getProtocol("' + arguments[0] + '")]')
        print ('<{}: {}>'.format(arguments[0], bridgeName))
        lldb.debugger.HandleCommand('po [%s %s]' % (bridgeName, arguments[1]))

```

#### 3.Chisel原理

Chisel是使用了lldb提供的[PythonAPI](https://lldb.llvm.org/python_reference/index.html)来实现各个脚本方法的。


PS:xcode11的lldb使用的是Python3，导致会有问题，可以先在终端中输入defaults write com.apple.dt.lldb DefaultPythonVersion 2，让lldb使用Python2





