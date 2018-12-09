# Speed of 'while True' and 'while 1'

 Python做為interpreted language，其內部運作會先把Python程式語言轉換為Byte Code，再將Byte Code編譯成0/1的Machine Code，最後由CPU處理Machine Code。

 那該如何觀察Python轉換為Byte Code的過程呢?

## 例子
 在CPython中自帶dis函式庫，可以透過呼叫dis來觀察轉換過程。
 今天有一段程式碼如下:
 先建立一個add function，呼叫function帶入變數c裡面，最後將答案印出來。
```Python
#demo.py
def add(a, b):
    return a+b

c = add(1, 2)
print("Result of add:", c)
```
利用以下代碼執行此程式:
```
python -m dis demo.py
```

產生的結果如下:
```
  1           0 LOAD_CONST               0 (<code object add at 0x000001758FF31150, file "demo.py", line 1>)
              2 LOAD_CONST               1 ('add')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (add)

  4           8 LOAD_NAME                0 (add)
             10 LOAD_CONST               2 (1)
             12 LOAD_CONST               3 (2)
             14 CALL_FUNCTION            2
             16 STORE_NAME               1 (c)

  5          18 LOAD_NAME                2 (print)
             20 LOAD_CONST               4 ('Result of add:')
             22 LOAD_NAME                1 (c)
             24 CALL_FUNCTION            2
             26 POP_TOP
             28 LOAD_CONST               5 (None)
             30 RETURN_VALUE
```

解釋一下這段結果
**def add(a, b)** 對應 **2 LOAD_CONST 1('add')**、**4 MAKE_FUNCTION 0**以及 **6 STORE_NAME 0(add)**
**c = add(1, 2)** 對應到 **8 LOAD_NAME 0 (add)**、 **10 LOAD_CONST 2(1)**、 **12 LOAD_CONST 3(2)**
**14 CALL_FUNCTION 2** 呼叫上面的add function
**16 STORE_NAME 1 (c)**將值帶回變數c中
**18 LOAD_NAME 2 (print)**呼叫print函式，**20 LOAD_CONST 4 ('Result of add:')**和**22 LOAD_NAME 1 (c)**對應到print中的值
**26 POP_TOP**把c的值pop出來
最後的 LOAD_CONST (None) 以及 RETURN_VALUE 是附加上去的，跟三行程式碼沒有關係

##分析

分析dis源碼:
```python
def dis(x=None, *, file=None, depth=None):
    """Disassemble classes, methods, functions, and other compiled objects.
    With no argument, disassemble the last traceback.
    Compiled objects currently include generator objects, async generator
    objects, and coroutine objects, all of which store their code object
    in a special attribute.
    """
    if x is None:
        distb(file=file)
        return
    # Extract functions from methods.
    if hasattr(x, '__func__'):
        x = x.__func__
    # Extract compiled code objects from...
    if hasattr(x, '__code__'):  # ...a function, or
        x = x.__code__
    elif hasattr(x, 'gi_code'):  #...a generator object, or
        x = x.gi_code
    elif hasattr(x, 'ag_code'):  #...an asynchronous generator object, or
        x = x.ag_code
    elif hasattr(x, 'cr_code'):  #...a coroutine.
        x = x.cr_code
    # Perform the disassembly.
    if hasattr(x, '__dict__'):  # Class or module
        items = sorted(x.__dict__.items())
        for name, x1 in items:
            if isinstance(x1, _have_code):
                print("Disassembly of %s:" % name, file=file)
                try:
                    dis(x1, file=file, depth=depth)
                except TypeError as msg:
                    print("Sorry:", msg, file=file)
                print(file=file)
    elif hasattr(x, 'co_code'): # Code object
        _disassemble_recursive(x, file=file, depth=depth)
    elif isinstance(x, (bytes, bytearray)): # Raw bytecode
        _disassemble_bytes(x, file=file)
    elif isinstance(x, str):    # Source code
        _disassemble_str(x, file=file, depth=depth)
    else:
        raise TypeError("don't know how to disassemble %s objects" %
type(x).__name__)
```
 * x參數可以是None、Method、Function、Generator Object、Asynchronous Generator Object、Coroutine、Class、Module、Code Object、Raw Bytecode、Source Code
 * 如果x是Method、Function、Generator Object、Asynchronous Generator Object、Coroutine的話，就回傳對應字節碼。
 * 如果x是Class或Module，會排序x所有元素並且返回
 * 如果x是Code Object、Raw Bytecode或Source Code，那麼會調用_disassemble函數，透過此函數輸出字節碼。

## 執行環境

* Python 3.7

## Reference
https://docs.python.org/3/library/dis.html
https://github.com/python/cpython/blob/3.7/Lib/dis.py