# test traction's sample retrieval
from traction import traction

tr = traction("num_test")
# das sample sollte es in der db geben
print(tr.smpl(psn="1367280101"))
print(tr.sample("1367280101"))