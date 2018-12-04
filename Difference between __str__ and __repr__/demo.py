class Test(object): pass

class Test_repr(object):
    def __repr__(object): return 'foo'

class Test_str(object):
    def __str__(object): return 'foo'

print("Test:", str(Test()))
print("Test", repr(Test()))
print("Test_repr", str(Test_repr()))
print("Test_repr", repr(Test_repr()))
print("Test_str", str(Test_str()))
print("Test_str", repr(Test_str()))
