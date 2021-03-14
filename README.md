# AutoGrader

- 0.2.0更新：加入资源分配溢出检测，如果发生资源溢出会输出溢出发生的位置。

  - 如果通过检测，会显示通过符号![image-20210312210156727](./ScreenShot/3.png)

    

  - 如果没有通过检测，会显示警告，并输出溢出发生的位置和操作，比如：![image-20210312210310933](./ScreenShot/4.png)
  
- 0.2.1更新：溢出信息更详细

  - ![image-20210313114711826](./ScreenShot/5.png)
  
- 0.2.2更新：可以对java程序输出分析了，详见下述食用方法。

**网页不再使用index.html的统一名称，改为当前时间戳，方便保存对比。**

## 1.说明

本程序仅用以分析2021华为软件精英挑战赛的个人程序输出结果，不得用于商业用途，仅做学习交流。

## 2.食用方法

1. Clone本项目到本地

2. 使用你的文本编辑器（记事本、NotePad++、VSCode等）打开目录中的`config.json`文件，你将看到以下内容：

   ![image-20210314200207973](./ScreenShot/1.png)

   字段意义：

   - **language**：你所使用的语言，请从[c,c++,python,java]中选择一个填入。
   - **pythonInterpreter**：如果language为python，请指定python解释器路径，留空则为默认python解释器，建议使用pypy并指定路径而不是Cpython。
   - **executable**：如果language为c或c++，请给出编译后的可执行文件(exe)的路径。
   - **sourceCode**：如果language为python，请给出python脚本所在的路径。
   - **javaPath**：如果language为java，请给出java路径，如果留空则为默认java。请在cmd中键入“java -version”来检查是否存在默认java解释器。
   - **javaClass**：如果language为java，请给出javaClass文件，也就是你已经用javac编译过的文件，如果不会编译请百度。
   - **ioData**：输入文件，以列表形式存在，其中每一个字符串为一个输入文件。

3. 

   如果你是C/C++选手，请在language中填入c++，然后在executable字段中给出编译后的可执行文件所在路径，并修改你的程序接受的输入文件所在的位置，填入到ioData字段中。

   如果你是Python选手，请在language中填入python，然后在PythonInterpreter中指定解释器，留空则为默认python解释器。在sourceCode字段填入你的python脚本所在路径，并给出程序接收的输入文件。

   如果你是Java选手，请在language中填入java，然后在javaPath中指定java路径，留空则使用默认java解释器。在javaClass字段中填入你已经使用javac编译好的.class文件或者可执行文件，并给出程序接受的输入文件。

   **注意：**

   **所有路径应当使用一个/或者\\\来避免转义，并遵循JSON格式。**

   **如果使用相对路径，请使用./开头**

   **程序从标准输入输出获取信息，请不要重定向输入输出，仅在ioData字段中给出你想要输入到程序的文件路径即可**

   **程序从标准输入输出获取信息，请不要重定向输入输出，仅在ioData字段中给出你想要输入到程序的文件路径即可**

   **程序从标准输入输出获取信息，请不要重定向输入输出，仅在ioData字段中给出你想要输入到程序的文件路径即可**

4. config编辑完成后，在你clone下来的本文件夹中打开cmd并运行`pip install -r requirements.txt`来安装autoGrader需要的依赖。

5. 运行`autograder.py`，你可以选择使用IDE来运行或者直接在命令行中键入`python autograder.py`来运行

### 结果实例

`autograder`运行结束后将在当前路径生成index.html并**自动使用Chrome**打开，你将看到类似的页面

![image-20210312183146233](./ScreenShot/2.png)

**如果你没有安装Chrome，请手动打开index.html**