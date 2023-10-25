# traction.py gives commonly used getters (and setters?) for centraxx db

# functions:

# sample(sampleid)

from dbcon import *

# sample gets sample with sampleid
def sample(sampleid):
    query = "select * from centraxx_sample s inner join centraxx_sampleidcontainer as c on c.sample = s.oid where c.psn = ? and c.idcontainertype = 6"
    result = qfad(query, sampleid)
    if len(result) > 0:
        return result[0]

    return None

