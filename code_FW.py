import os
import json
import time
import sys
from filelock import FileLock
class path1():
    ''' This class maintains the path and loading and dumping activities on the file path
        If Data Store path isn't provided a default Data Store is Created'''
    def __init__(self,pa="Freshworks_Datastore_FW.txt"):
        if(pa=="Freshworks_Datastore_FW.txt"):
            self.path=os.path.join(os.path.dirname(os.path.abspath(__file__)),pa)#default data store path if one isn't provided
            if(not os.path.isfile(self.path)):#if Data store is to be created for the first time
                f=open(self.path,'w')
                f.write("{}")#adding {} to the file to make it json loadable
                f.close()
        else:
            try:
                if(os.stat(pa).st_size == 0):
                    f=open(pa,'w')
                    f.write("{}")#if the specified path file is empty adding {} to make it json loadable 
                    f.close()
                    self.path=pa
                else:
                    f=open(pa,'r')
                    data=json.load(f)#if given path file is not empty and if it is not json loadable
                    f.close()       #exception occurs and prompts that file is not json loadable
                    self.path=pa
            except:
                print("Make sure the file specified exists and is a json loadable!!")
                sys.exit()
    def getpath(self):
        return self.path
    def dumpdata(self,data):
        with FileLock(self.getpath()+".lock"):#Ensuring Thread Safe
            with open(self.getpath(),'w') as f:
                json.dump(data,f)
    def loaddata(self):
        with FileLock(self.getpath()+".lock"):#Ensuring Thread safe
            with open(self.getpath(),'r') as f:
                data=json.load(f)
               
        return data
class DataStore(path1):
    ''' This class defines the Create ,Read and Delete Operations on Data Store to be performed
        It inherits path1 class'''
    def Create(self,k,va,ttl=0):
        '''-> Create method takes key,value and an optional value time to live if provided as parameters
           -> it loads the old data and checks if key already exists and adds key:value pair to data if key doesn,t already exists
           ->This new data is only inserted into file if the data size is not morethan 1GB'''
        data=super().loaddata()#load old data
        v=json.loads(va)#Value which is mentioned as json object is converted to python dictionary object
        if(k not in data):#check if key already exists
            if(ttl):#if time to live is mentioned
                v["ttl"]=time.time()+ttl
                data[k]=v
            else:
                data[k]=v
            if(len(str(data))<=1024*1024*1024):#constraints for file size not exceeding 1GB
                super().dumpdata(data)
                print("{}:{} stored".format(k,v))
            else:
                print("File size exceeding 1GB cannot insert data")
        else:
            print("key already exists")
            
    def Read(self,k):
        '''->Read method takes key as parameter
           ->first old data is loaded and check the data for key
           ->if key is avalilable and still has some time to live(optional) then value is displayed
           ->if key is expired or key is unavailable value is not printed'''
        data=super().loaddata()#load old data
        if(k in data):#check if key is available
            try:#if key has time to live property
                if(time.time()<data[k]["ttl"]):#check if key expired
                    ttl=data[k]["ttl"]
                    data[k].pop("ttl",None)
                    print(k,":",json.dumps(data[k]))
                    data[k]["ttl"]=ttl
                else:
                    print(k,":Key Expired")
            except:#if the key do not have time to live property
                print(data[k])
        else:
            print("key",k," unavailable")
    def Delete(self,k):
        ''' ->Delete method takes a key as parameter
            ->loads olad data and the key is deleted if key exits and has time to live(optional)
            -> and the data is dumped into json file'''
        data=super().loaddata()
        try:#if key has time to live property
            if(time.time()<data[k]["ttl"]):#check if key is expired
                data.pop(k,None)#key is deleted if exists else does nothing
                print("Key",k," Deleted if existed")
            else:
                print("Key",k," Expired not available for deletion")
        except:#if key does not have time to live property
            data.pop(k,None)
            print("Key",k," Deleted")
        super().dumpdata(data)

