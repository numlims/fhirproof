from dict-path import DictPath
d = {"a": "hello", "b": [1, 2, 3], "c": " world"}
pd = DictPath(d)
print(pd.get("b/1"))

