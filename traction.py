# traction.py gives commonly used getters (and setters?) for centraxx db

# functions:

# smpl(?samplepsn, ?locationpath, ?like)
# patient(sampleid)

from dbcq import *

class traction:

    #def __init__(self, target):
    #    self.db = dbcq(target)

    # this doesn't work, why?
    #def __init__(self, target: str):
    #    print("init traction with string")
    #    self.db = dbcq(target)
    #def __init__(self, target: dbcq):
    #    print("init traction with dbcq")
    #    self.db = target  

    # init can be passed a string or dbcq
    def __init__(self, target):
        if type(target) is str:
            target = dbcq(target)
        self.db = target

    #get("sample", "samplelocation.locationpath = 'dresden'")
    # get pspawn samples with patients, wobei, das waer schon fast unabhaengig von centraxx db
    # a|b ist nur moeglich, wenn maximal ein fk aus b a referenziert, sonst error
    #get("sample.patientcontainer|idcontainer.psn, sample|sampleidcontainer.psn", where="idcontainer like 'pspawn' and sampleidcontainer.idcontainertype=6")
    
    

    # smpl gives sample with psn or location
    # maybe pass arguments as dicts, to be able to specify equal or like matching, e.g. locationpath = {value:'<my locationpath>',like=True}
    def smpl(self, psn = None, locationpath = None, like=False):
        # we would like to be able to return the column names prefixed by the table names, to avoid clashes when column names appear in more than one table. unfortunately there seems to be no standard sql way of doing this, see https://stackoverflow.com/a/57832920
        # so for now say: select <table short>.<column name> as '<table name>.<column name>'
        query = """
         select s.*,
        sidc.psn as 'sampleidcontainer.psn',
        samplelocation.locationid as 'samplelocation.locationid', 
        samplelocation.locationpath as 'samplelocation.locationpath',
        sampletype.code as 'sampletype.code',
        stockprocessing.code as 'stockprocessing.code',
        secondprocessing.code as 'secondprocessing.code',
        project.code as 'project.code',
        receptable.code as 'receptable.code',
        orgunit.code as 'orgunit.code',
        flexistudy.code as 'flexistudy.code'
        from centraxx_sample s
        inner join centraxx_sampleidcontainer as sidc on sidc.sample = s.oid
        left join centraxx_samplelocation samplelocation on samplelocation.oid = s.samplelocation
        left join centraxx_sampletype as sampletype on sampletype.oid = s.sampletype
        left join centraxx_stockprocessing as stockprocessing on s.stockprocessing = stockprocessing.oid
        left join centraxx_stockprocessing as secondprocessing on s.secondprocessing = secondprocessing.oid
        left join centraxx_project as project on s.project = project.oid
        left join centraxx_samplereceptable as receptable on s.receptable = receptable.oid
        left join centraxx_organisationunit as orgunit on s.orgunit = orgunit.oid
        left join centraxx_flexistudy as flexistudy on s.flexistudy = flexistudy.oid

        where sidc.idcontainertype = 6
        """
        args = []

        if psn != None:
            query = query + " and " + self._wherestring("sidc.psn", like)
            args.append(psn)
        if locationpath != None:
            query = query + " and " + self._wherestring("samplelocation.locationpath", like)
            args.append(locationpath)

        # print(query)
            
        return self.db.qfad(query, *args)

    # sample gets sample faster than smpl (from fhirproof)
    # now theres a slow method that returns much (smpl) and a faster method that returns little (sample). in future, maybe find a way to give more fine-grained options what to join in?
    def sample(self, sampleid):
        query = "select * from centraxx_sample s inner join centraxx_sampleidcontainer as sidc on sidc.sample = s.oid where sidc.psn = ? and sidc.idcontainertype = 6"
        # print(query)
        result = self.db.qfad(query, sampleid)
        if len(result) > 0:
            return result[0]

        return None

    # _wherestring gives a ?-parameterized sql where expression for name equal or like parameter for use in queries
    def _wherestring(self, name, like):
        if not like:
            return name + " = ?"
        else:
            return name + " like '%' + ? + '%'"
        
    # patient gives the patient of sample
    def patient(self, sampleid):
        # get from sample to patient: sample to patientcontainer, patientcontainer to idcontainer.
        query = """
        select idc.*, pc.* from centraxx_idcontainer idc
        inner join centraxx_patientcontainer pc on idc.patientcontainer = pc.oid
        inner join centraxx_sample s on s.patientcontainer = pc.oid
        where idc.idcontainertype = 8 and s.oid = ?
        """
        result = self.db.qfad(query, sampleid)
        if len(result) == 0:
            return None
        return result[0]

