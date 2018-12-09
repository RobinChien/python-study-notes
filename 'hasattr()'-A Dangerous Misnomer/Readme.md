# 'hasattr()'-A Dangerous Misnomer

這是在研究 dis.py 開源碼的時候看到dis大量使用到 **hasattr()**，因此查詢了一下 **hasattr()** 這個函式，就發現了Hynek Schlawack所撰寫的hasattr()問題，此篇是翻譯他的文章。

## 全文

不要在Python 3以下的版本或是不了解的狀況下使用 **hasattr()**。
**hasattr()**是在Python code reviews中常見的主題，所以這邊提供較安全的寫法。

Do not:
```Python
if hasattr(x, "y"):
    print(x.y)
else:
    print("no y!")
```

Do instead:
```Python
try:
    print(x.y)
except AttributeError:
    print("no y!")
```

or:
```Python
y = getattr(x, "y", None)
if y is not None:
    print(y)
else:
    print("no y!")
```
如果處理的是自己寫的class，更應該採用此寫法。
hasattr()在速度上也沒有比getattr()快，因為兩者查找過程完全相同，而前者不會保留結果。

## 為什麼不建議使用hasattr()?

在python2下使用hasattr()和下面的代碼幾乎相同:
```Python
try:
    print(x.y)
except:
    print("no y!")
```

這幾乎不是你想要的，因為它會影響屬性中的錯誤：

```Pyhton
>>> class C(object):
...     @property
...     def y(self):
...         0/0
...

#python 2
>>> hasattr(C(), "y")
False

#python 3
>>> hasattr(C(), "y")
Traceback (most recent call last):
  File "demo.py", line 6, in <module>
    print(hasattr(C(), "y"))
  File "demo.py", line 4, in y
    0/0
ZeroDivisionError: division by zero
```
因為在third party classs中，我們無法確定某個屬性(attribute)是否為特性(@property)，或是在之後的更新將其變成特性，因此這樣使用**hasattr()**是危險的，**不過在Python 3中，hasattr()不存在這個問題**，因此在寫python2與3的混合程式碼時，要特別注意這個函數。

另外，我們在調用hasattr()是要驗證屬性或特性是否存在，如果引發AttributeError，我們就無法區別到底是缺失該屬性，還是特性存在問題，**文章中的寫法可以將可能的錯誤減少到只有一個，避免出現Python2和3之間的行為混淆**。

## 結語
當然你還是可以繼續使用hasattr()，**但記得在class修改的時候去修復對應的hasattr()**，不過這也會造成開發時增加了不必要的精神負擔。

## Reference
https://hynek.me/articles/hasattr/
