from datetime import datetime
import json
from functools import wraps

def log_duration(func):
    def decorate(*args,**kw):
        t1 = datetime.now()
        result=func(*args, **kw)
        print(result)
        t2 = datetime.now()-t1
        print(t2.seconds)
        return result
    return decorate

def to_json(func):
    def decorate(*args, **kw):
        result = func(*args, **kw)
        if type(result) == dict :
            s = json.dumps(result, sort_keys=True)
            return s
        else :
            return result
    return decorate

def ignore_exceptions(Exception):
    def decorate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                return None
            else:
                print('It\'s OK!')
                return func(*args, **kwargs)
        return wrapped
    return decorate


@log_duration
def power():
    return 2**2**20

@to_json
def with_map():
    map1 = {True: "Marshall", 2: "Bill", -3: False, False: True}
    return map1

@to_json
def without_map():
    list1 = [1488, 'UnMarshall']
    return list1

@ignore_exceptions(ZeroDivisionError)
def div(a, b):
    return a / b

n=power()

struct1 = with_map()
print(struct1)

struct2 = without_map()
print(struct2)

result = div(10 , 2)
result_0 = div(10, 0)

print(result)
print(result_0)
