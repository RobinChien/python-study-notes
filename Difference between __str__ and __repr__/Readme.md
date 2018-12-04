# Difference between __str__ and __repr__

 **__str__** 與 **__repr__** 都是用於顯示，除非特別採取行動，否則在大多數Class中，兩者的效果沒有差別：

```python
class Test(object): pass
print("Test:", str(Test()))
#Test_str: <__main__.Test object at 0x0000028E699249E8>
print("Test", repr(Test()))
#Test_repr: <__main__.Test object at 0x0000028E69924A90>
```

 可以看到輸出並無不同，除了class和物件id外沒有其他信息，但如果把將__str__與__repr__覆寫的話:
```python
class Test1(object):
    def __repr__(object): return 'foo'

class Test2(object):
    def __str__(object): return 'foo'

print("Test1_str:", str(Test1()))
#Test1_str: foo
print("Test1_repr:", repr(Test1()))
#Test1_repr: foo
print("Test2_str:", str(Test2()))
#Test2_str: foo
print("Test2_repr:", repr(Test2()))
#Test2_repr: <__main__.Test2 object at 0x0000028E69924A90>
```

可以看到當覆寫了__repr__，產生與__str__一樣的效果，但反之則不然。

## 小結論
 __str__注重再提供使用者可讀性，而__repr__則是注重在檢查class是否錯誤，若要讓class顯示輸出值的話，覆寫__str__即可。

## 執行環境

* Python 3.6.4

## Reference
https://stackoverflow.com/questions/1436703/difference-between-str-and-repr