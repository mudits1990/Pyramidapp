from simple_salesforce import Salesforce, SalesforceLogin, SFType
import mongoadapter

class sfdcdatafetch():

    def __init__(self, session_id, instance_url):
        self.session_id = session_id
        self.instance_url = instance_url

    def returnsObject(self):
        sf = Salesforce(instance_url=self.instance_url, session_id=self.session_id)
        object_list = []
        for x in sf.describe()['sobjects']:
            l1 = {}
            l1['name']=x['name']
            l1['custom']=x['custom']
            l1['label']=x['label']
            object_list.append(l1)
        return object_list

    def getTableData(self,*args):
        sf = Salesforce(instance_url=self.instance_url, session_id=self.session_id)
        session_id = sf.session_id
        instance = sf.sf_instance
        query = "Select "
        for sObject in args:
            sObjectName = SFType(sObject,session_id,instance)
            for x in sObjectName.describe()['fields']:
                query = query + x['name'] + ","
            query = query[:-1] + " from " + sObjectName.name
            #print query
            res = sf.query_all(query)
            records = res['records']
            ls = []
            adapter = mongoadapter.adapter()
            collection = adapter.createColletion(sObject)
            for x in records:
                data = {}
                for y in sObjectName.describe()['fields']:
                    data[y['name']] = x[y['name']]
                    #print data
                #print data
                ls.append(adapter.insert_posts(collection, data))
        return ls

    def getFieldType(self,*args):
        sf = Salesforce(instance_url=self.instance_url, session_id=self.session_id)
        session_id = sf.session_id
        instance = sf.sf_instance
        type = {}
        ls=[]
        for sObject in args:
            adapter = mongoadapter.adapter()
            sObject_type = sObject + "_type"
            collection = adapter.createColletion(sObject_type)
            print sObject_type
            sObjectName = SFType(sObject,session_id,instance)
            for y in sObjectName.describe()['fields']:
                type[y['name']] = y['type']
            ls.append(adapter.insert_posts(collection, type))
        return ls

#sfdc = sfdcdatafetch('mudit@mammoth.io','mammoth1234$','N0OF2max8RxHHoZkY4AB96uih')
#sfdc = sfdcdatafetch('mudit@mammoth.io','mammoth1234$','oy4po3ssdQ8UJieOpxL4sYjN')
#print sfdc.returnsObject()
#sfdc.getFieldType('Campaign__c', 'Account')
#sfdc.getTableData('Campaign__c')