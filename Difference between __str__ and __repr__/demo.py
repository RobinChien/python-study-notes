class Test(object): pass

class Test1(object):
    def __repr__(object): return 'foo'

class Test2(object):
    def __str__(object): return 'foo'

print("Test_str:", str(Test()))
print("Test_repr:", repr(Test()))
print("Test1_str:", str(Test1()))
print("Test1_repr:", repr(Test1()))
print("Test2_str:", str(Test2()))
print("Test2_repr:", repr(Test2()))
