from dictpath import *

d = {"a": "hello", "b": [1, 2, 3], "c": " world", "d": {"hello": "hi"}}

dp = DictPath(d)

print(dp / "d" / "hello")
