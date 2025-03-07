# dig is a dictpath wrapper for extract_dict, dis for inject_dict
# why? dictpath.get seems to return simple dicts, not dictpaths, which seems to be a bit of a shame, if you'd like to get dictpaths from them
# DictPath(deepcopy=True) doesn't seem to work
# https://pypi.org/project/dict-path/#description

from dict_path import extract_dict, inject_dict

# dig gets path from d
def dig(d, path):
    return extract_dict(d, path)

# dis sets path to value in d
def dis(d, path, val):
    inject_dict(d, path, val)
