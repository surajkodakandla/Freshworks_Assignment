import code_FW as c
from threading import Thread
import time
ds=c.DataStore()
#-----------Operations Using THREAD Mechanism----------#
t1=Thread(target=ds.Create,args=("Assignment",'{"Company_name":"Freshworks","name":"Suraj","Location":"Hyderabad"}'))
t2=Thread(target=ds.Create,args=("Company1",'{"name":"Freshworks","Location":"Hyderabad"}',20))
t3=Thread(target=ds.Read,args=("Company1",))
t4=Thread(target=ds.Read,args=("Assignment",))
t5=Thread(target=ds.Delete,args=("Assignment",))
t6=Thread(target=ds.Read,args=("Company1",))
t7=Thread(target=ds.Read,args=("Assignment",))
t1.start()
t1.join()
t2.start()
t2.join()
t3.start()
t3.join()
t4.start()
t4.join()
time.sleep(20)
t6.start()
t6.join()
t5.start()
t5.join()
t7.start()
t7.join()

