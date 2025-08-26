# 读写文件

2024-10-23 ⭐
@author Jiawei Mao
***
## 简介

`open()` 返回一个文件对象，通常使用 2 个位置参数和 1 个关键字参数：`open(filename, mode, encoding=None)`

```python
>>> f = open('workfile', 'w', encoding="utf-8")
```

参数：

- 第一个参数是包含文件名的字符串；
- 第二个参数也是字符串，包含的字符用于描述使用文件的方式：
  - `'r'` 表示只读，默认
  - `'w'` 表示写入（同名文件被删除）
  - `'a'` 表示追加，写入数据添加到文件末尾
  - `'r+'` 表示读写

通常以文本模式打开文件，即以指定 encoding 从文件读写字符串。`encoding` 默认值取决于平台。UTF-8 是现代文件编码事实标准，除非你知道需要使用其它编码，否则建议使用 `encoding="utf-8"`。

在 `mode` 中附加 `'b'` 表示以 binary 模式打开文件，binary 模式以 `bytes` 对象的形式读写数据。以 binary 模式打开无法指定 `encoding` (也没必要)。

在 text 模式，默认换行符取决于平台，Unix 为 `\n`，Windows 为 `\r\n`。在 text 模式写入，会自动将 `\n` 转换为平台的换行符。这种后台修饰文件数据对文本文件没问题，但会损坏 JPEG 或 EXE 等 binary 文件格式。在读写此类文件时要小心使用 binary 模式。

处理文件对象时建议使用 `with` 关键字。该语法能保证正确关闭文件。使用 `with` 也比等效的 `try-finally` 更短：

```python
>>> with open('workfile', encoding="utf-8") as f:
...     read_data = f.read()

>>> # We can check that the file has been automatically closed.
>>> f.closed
True
```

如果不使用 `with` 关键字，就需要调用 `f.close()` 来关闭文件并释放资源。

> [!WARNING]
>
> 不使用 `with` 关键字也不使用 `f.close()`，调用 `f.write()` 可能会导致 `f.write()` 的参数无法完全写入磁盘，即使程序成功退出。

使用 `with` 语句或 `f.close()` 关闭文件对象后，使用该文件对象将报错：

```python
>>> f.close()
>>> f.read()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
```

## 文件对象的方法

假设已经创建了名为 `f` 的文件对象。

**f.read(size)**

使用 `f.read(size)` 读取一定量的数据，在 text 模式返回字符串，在 binary 模式返回字节。`size` 为可选参数：

- 当忽略 `size` 或为负数时，读取并返回整个文件的内容，如果文件大小远大于内存，那就是你的问题了
- 否则读取 `size` 个字符（text 模式）或 `size` 个字节（binary 模式）

如果到达文件末尾，`f.read()` 返回一个空字符串 `''`。

```python
>>> f.read()
'This is the entire file.\n'
>>> f.read()
''
```

**f.readline()**

`f.readline()` 从文件读取一行；字符串末尾会留下一个换行符 `\n`，除非是最后一行，且最后一个不是换行符。如果 `f.readline()` 返回空字符串，表示到达文件末尾，空行以 `'\n'` 表示，即只包含换行符的字符串。

```python
>>> f.readline()
'This is the first line of the file.\n'
>>> f.readline()
'Second line of the file\n'
>>> f.readline()
''
```

可以循环遍历文件逐行读取。这节省内存、速度快，代码简单：

```python
>>> for line in f:
...     print(line, end='')
...
This is the first line of the file.
Second line of the file
```

读取文件中的所有 lines，使用：

- `list(f)`
- 或 `f.readlines()`

`f.write(string)` 将 `string` 内存写入文件，返回写入的字符数。

```python
>>> f.write('This is a test\n')
15
```

其它类型的对象在写入前需要先转换为字符串（text 模式）或字节（binary 模式）：

```python
>>> value = ('the answer', 42)
>>> s = str(value)  # convert the tuple to string
>>> f.write(s)
18
```

`f.tell()` 返回一个整数，指示指针在文件中的当前位置，在 binary 模式，表示距离开头的字节数；在 text 模式，则为当前位置。

使用 `f.seek(offset, whence)` 修改指针位置，该位置通过将 `offset` 与参考点相加计算，`whence` 为参考点：0 表示文件开头，1 表达当前位置，2 表示文件末尾。`whence` 默认为 0.

```python
>>> f = open('workfile', 'rb+')
>>> f.write(b'0123456789abcdef')
16
>>> f.seek(5)      # Go to the 6th byte in the file
5
>>> f.read(1)
b'5'
>>> f.seek(-3, 2)  # Go to the 3rd byte before the end
13
>>> f.read(1)
b'd'
```

在 text 文件中，只允许相对文件开头进行搜索，并且唯一有效的 `offset` 为 `f.tell()` 返回值或 0，使用其它 `offset` 的结果未知。

文件对象还有其他方法，如 `isatty()` 和 `truncate()` 等，这些方法使用较小。

## 使用 json 保存结构化数据

字符串的读写很容易。数字则稍微麻烦一点，因为 `read()` 只返回字符串，必须将字符串传递给 `int()` 之类的函数转换类型。对更复杂的数据类型，如嵌套 list 和 dict，手动解析和序列化会很复杂。

Python 支持将复杂的数据类型保存为 JSON 格式。标准模块 `json` 可以将 Python 数据结构转换为字符串形式，该过程称为序列化（serializing）。从字符串表示形式重建数据结构称为反序列化（deserializing）。在序列化和反序列化之间，表示对象的字符串可能存储在文件或数据中，或通过网络发送到某个远程机器。

> [!NOTE]
>
> JSON 格式是现代应用常用的数据交换格式。

如果你有一个对象 `x`，可以用一行代码转换为 JSON 字符串：

```python
>>> import json
>>> x = [1, 'simple', 'list']
>>> json.dumps(x)
'[1, "simple", "list"]'
```

除了 `dumps()` 函数，`dump()` 可以将对象序列化为文本文件。因此，如果 `f` 是以写入模式打开的文本文件对象：

```python
json.dump(x, f)
```

解码：假设 `f` 是以读取模式打开的 binary 或 text 文件：

```python
x = json.load(f)
```

> [!NOTE]
>
> JSON 文件必须使用 UTF-8 编码。将 JSON 文件以 text 模式打开时，使用 `encoding="utf-8"`。

这个简单的序列化技术可以处理 dict 和 list，序列化其它类则需要额外工作，具体可以参考 json 模块。

## 参考

- https://docs.python.org/3.9/tutorial/inputoutput.html#reading-and-writing-files
