import numpy as np
import hashlib
import string
import random
from datetime import datetime, timedelta
import pytz
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCan
from matplotlib.figure import Figure
import csv
import codecs
import pdfkit

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

def get_current_datetime():
    return datetime.strptime(generate_current_datetime(), "%Y-%m-%d %H:%M:%S")

def inactivate_user_to_remove(users):
    date_time = datetime.strptime(generate_current_datetime(), "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
    to_remove = []
    for user in users:
        if user[1] <= date_time:
            to_remove.append(user)
    return to_remove

def get_time_for_cancel_poll():
    zone = pytz.timezone('Europe/Warsaw')
    date_time = datetime.now(zone) - timedelta(weeks=2)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')
    
def str_for_date_and_time(date, time, end):
    if end:
        date_time = (date + " " + time + ":59")
    else:
        date_time = (date + " " + time + ":00")
    return date_time

def str_date_and_time(date, time):
    date_time = (date + " " + time)
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

def if_poll_duration_wrong(start_datetime, end_datetime):
    start_date_and_time = datetime.strptime((start_datetime), "%Y-%m-%d %H:%M:%S")
    end_date_and_time = datetime.strptime((end_datetime), "%Y-%m-%d %H:%M:%S")
    if start_date_and_time < end_date_and_time+timedelta(minutes=5):
        return True
    return False

def if_start_time_before_datetime(start_datetime):
    date_time = datetime.strptime(generate_current_datetime(), "%Y-%m-%d %H:%M:%S")
    start_date_and_time = datetime.strptime((start_datetime), "%Y-%m-%d %H:%M:%S")
    if date_time > start_date_and_time-timedelta(minutes=10):
        return True
    return False

def str_for_datetime(date_time):
    out = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return out

def gen_plots(questions):
    images=[]
    for question_answers in questions:
        question = question_answers[0][0]
        answers = question_answers[1]
        labels=[]
        values=[]
        x = 0

        for answer in answers:
            labels.append(answer[0])
            values.append(answer[1])
            x += int(answer[1])
        if x != 0:
            values = np.array(values)/x*100
        
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.pie(values, autopct=lambda p:'{:.2f}%'.format(round(p,2)) if p>0 else '', shadow=True)
        axis.legend(labels, title="Odpowiedzi")#, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)) #, prop={'family':'Italic'}
        
        pngim = io.BytesIO()
        FigCan(fig).print_png(pngim)
        pngimstr = "data:image/png;base64,"
        pngimstr += base64.b64encode(pngim.getvalue()).decode('utf8')
        images.append(pngimstr)
    return images

def generate_csv(result):
    output = io.StringIO()
    writer = csv.writer(output)
    line=["Pytania;Odpowiedzi;Liczba głosów"]
    writer.writerow(line)
    for row in result:
        question = row[0][0]
        answers = row[1]
        line=[question+";; "]
        writer.writerow(line)
        for answer in answers:
            line = [";"+answer[0]+";"+str(answer[1])]
            writer.writerow(line)
    return codecs.BOM_UTF8.decode("utf8") + codecs.BOM_UTF8.decode() + output.getvalue()

def generate_pdf(html):
    path_wkhtmltopdf = './bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf = pdfkit.from_string(html, False, configuration=config)
    return pdf
