import numpy as np
import hashlib
import string
import random
from datetime import datetime, timedelta
import pytz

def hashing(password):
    hash = hashlib.sha512(password.encode()).hexdigest()
    return hash

def pass_decoder(code):   
    decode=''
    for l in range(int(len(code)/8)):  
        v=0
        j=0
        for i in range(7,-1,-1):
            v=v+int(code[8*l+j])*2**(i)
            j=j+1
        newv=chr(v)
        decode=decode+newv
    return decode

def random_number(n):
    x = np.random.randint(10**n,10**(n+1))
    return "" + str(x)

def random_string(n):
    sings = (string.ascii_letters+string.digits+"@_?!-+=*/#$&")
    out = ""
    for i in range(n):
        out = out + random.choice(sings)
    return out

def generate_current_datetime():
    zone = pytz.timezone('Europe/Warsaw')
    date = datetime.now(zone)
    return date.strftime('%Y-%m-%d %H:%M:%S')

def inactivate_user_to_remove(users):
    zone = pytz.timezone('Europe/Warsaw')
    date_time = datetime.now(zone) - timedelta(hours=1)
    to_remove = []
    for user in users:
        if user[1] <= date_time:
            to_remove.append(user)
    return to_remove
    
def str_for_date_and_time(date, time, end):
    if end:
        date_time = (date + " " + time + ":59")
    else:
        date_time = (date + " " + time + ":00")
    return date_time

def list_of_added_user(list_user):
    list_added_user = []
    for i in list_user:
        list_added_user.append(i[0])
    return list_added_user

def get_str_time_from_datetime(date_time):
    time = date_time.strftime('%H:%M:%S')
    return time

def get_str_date_from_datetime(date_time):
    date = date_time.strftime('%Y-%m-%d')
    return date

def if_date_and_time_before_datetime(date, time, date_time):
    date_and_time = datetime.strptime((date + " " + time), "%Y-%m-%d %H:%M:%S")
    if date_and_time < date_time:
        return True
    else:
        return False

def str_for_datetime(date_time):
    out = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return out
