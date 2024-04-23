from dict_path import DictPath
d = {"a": "hello", "b": [1, 2, 3], "c": " world"}
# does the 'in' keyword work for dict-path?
# seems so
print(f"a in dict: {'a' in d}")
pd = DictPath(d)
print(pd.get("b/1"))



