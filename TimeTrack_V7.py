import os
import calendar
import tkinter
from tkinter import *
import tkcalendar
from tkcalendar import *
import babel.numbers
import datetime
import getpass
import csv
import pytz
import easygui
import matplotlib.pyplot as plt
tz_NY = pytz.timezone('Asia/Kolkata')
user= str(getpass.getuser()).upper()

database="//its9010290/cae_root/cae_data/Tase/FNA/PROJECT_DOCUMENTS/TRANSIENT/SCRIPT_DEVELOPMENT/DATABASE/TimeTrack/Timetrack2020"
mfile="//its9010290/cae_root/cae_data/Tase/FNA/PROJECT_DOCUMENTS/TRANSIENT/SCRIPT_DEVELOPMENT/DATABASE/TimeTrack/message.txt"


def main():
    if not os.path.isfile(database):easygui.msgbox("server not connected; contact developer");return

    def stat():
        try:plt.close()
        except:pass
        MONTH=(cal.selection_get().strftime("%B")).upper()
        year=int(cal.selection_get().strftime("%Y"))
        month=int(cal.selection_get().strftime("%m"))

        id=user+MONTH


        CAL = calendar.Calendar()
        xdata=[]
        for week in CAL.monthdayscalendar(year, month):
            for day in week[:-2]:
                if day!=0:xdata.append(day)

        file=open(database,'r')

        string={}
        data={}
        for row in file:
            if row.startswith(id):
                key=row.split(',')[0]
                t=row.split(',')[1][:-1]
                string[key]=t
                value=t.split(':')
                value1=int(value[0])+(int(value[1])/60.0)
                data[key]=value1

        file.close()

        stringdata=[]
        for i in xdata:
            IN='';OUT='';delta=''
            if id+str(i)+str(year)+'IN' in string:IN=string[id+str(i)+str(year)+'IN']
            if id+str(i)+str(year)+'OUT' in string:OUT=string[id+str(i)+str(year)+'OUT']
            stringdata=stringdata+[[str(i),IN,OUT]]

        ydata=[]
        ystring=[]
        for i in xdata:
            if id+str(i)+str(year)+'IN' in data and id+str(i)+str(year)+'OUT' in data:
                ydata.append(data[id+str(i)+str(year)+'OUT']-data[id+str(i)+str(year)+'IN'])
                val=data[id+str(i)+str(year)+'OUT']-data[id+str(i)+str(year)+'IN']
                val=str(int(val))+':'+str(int((val-int(val))*60))
                ystring.append(val)
            else:
                ydata.append(0)
                ystring.append('')


        plt.rcdefaults()
        y_pos = range(len(xdata))
        performance = ydata

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, xdata)
        plt.ylabel('hours')
        plt.xlabel('dates')
        plt.title(str(MONTH)+' '+str(year))
        plt.axhline(y=8,c='r', linestyle='--', alpha=0.3)
        plt.subplots_adjust(right=0.75)
        the_table = plt.table(cellText=stringdata,colWidths =[0.1] * 3,colLabels=['Date','In','Out'],loc='right')

        for i in range(len(xdata)):plt.text(x = i-0.3 , y = ydata[i]+0.1, s = ystring[i])

        plt.show()

    def recall():
        date=cal.selection_get().strftime("%B%d%Y")
        word=(user+date+"Out").upper()
        fd= open(database,'r')
        new=[row for row in fd if not row.startswith(word)]
        fd.close()
        fd=open(database,'w')
        fd.writelines(new)
        fd.close()
        refresh()

    def check(event):
        fd= open(database,'r')
        datas={row[0].upper():row[1] for row in csv.reader(fd) if row }
        fd.close()
        date=cal.selection_get().strftime("%B%d%Y")
        x=(user+date+"In").upper()
        if x in datas:L7.config(text=datas[x])
        else:L7.config(text='')
        x=(user+date+"Out").upper()
        if x in datas:L8.config(text=datas[x])
        else:L8.config(text='')


    def update(text):
        timenow=datetime.datetime.now(tz_NY).strftime("%H:%M")
        date=str(datetime.datetime.now(tz_NY).strftime("%B%d%Y"))
        if datetime.datetime.now(tz_NY)<datetime.datetime.now(tz_NY).replace(hour=4, minute=00):date=int(date)-1;date=str("%02d" % date)
        row=[i.upper() for i in [user+date+text,timenow]]
        fd= open(database,'a')
        writer = csv.writer(fd,lineterminator='\n')
        writer.writerow(row)
        fd.close()
        refresh()

    def maximize():
        if window.winfo_height()!=500:window.geometry("280x500");bmax.config(text="-")
        else:window.geometry("280x55");bmax.config(text="+")

    def exitwin():
        window.destroy()
        plt.close()

    def refresh():

        date=str(datetime.datetime.now(tz_NY).strftime("%B%d%Y"))
        fd= open(database,'r')
        datas={row[0].upper():row[1] for row in csv.reader(fd) if row }
        fd.close()

        x=(user+date+"In").upper()
        if x in datas:L2.config(text=datas[x]);bIN.configure(state=DISABLED,bg="green2");bOUT.configure(state=NORMAL,bg="SystemButtonFace")
        else:L2.config(text='');L1.config(text='0:0');bIN.configure(state=NORMAL,bg="SystemButtonFace");bOUT.configure(state=DISABLED,bg="SystemButtonFace")
        x=(user+date+"Out").upper()
        if x in datas:L3.config(text=datas[x]);bOUT.configure(state=DISABLED,bg="green2");brec.configure(state=NORMAL)
        else:L3.config(text='');brec.configure(state=DISABLED,bg="SystemButtonFace")

        cal.calevent_remove('all')
        cal.calevent_create(cal.datetime.today(), 'Today','message')
        cal.selection_set(datetime.datetime.today().date())
        check(None)

        if L2.cget("text")!='' and L3.cget("text")!="":
            t=L2.cget("text").split(':')
            t2=L3.cget("text").split(':')
            x=str(datetime.datetime.now().replace(hour=int(t2[0]), minute=int(t2[1]),second=0)-datetime.datetime.now().replace(hour=int(t[0]), minute=int(t[1]),second=0)).split(':')
            L1.config(text=x[0]+':'+x[1])

        f=open(mfile,'r');message=f.readline();f.close()
        l.config(text=message)

    def tick():
        L4.config(text=datetime.datetime.now(tz_NY).strftime("%D"))
        L5.config(text=datetime.datetime.now(tz_NY).strftime("%I:%M:%S %p"))
        L5.after(500, tick)

        if L2.cget("text")!='' and L3.cget("text")=="":
            t=L2.cget("text").split(':')
            x=str(datetime.datetime.now(tz_NY).replace(tzinfo=None,second=1)-datetime.datetime.now().replace(hour=int(t[0]), minute=int(t[1]),second=0)).split(':')
            L1.config(text=x[0]+':'+x[1])


        if datetime.datetime.now(tz_NY).strftime("%M:%S")=="00:00":refresh()

    def callback(event):
        x=window.winfo_pointerx()
        if x>300:x=x-280
        y=0;
        window.geometry("280x55+"+str(x)+"+"+str(y))
        bmax.config(text="+")

    def scroll():
        x=l.winfo_x()-2
        if x <- l.winfo_width():x=window.winfo_width()
        l.place(x=x,y=36)
        l.after(100,scroll)


    window = Tk()
    window.title('Time track')
    window.wm_attributes("-topmost", 1)
    window.overrideredirect(1)
    window.resizable(width=False, height=False)
    window.geometry("280x55")
    window.bind('<B1-Motion>', callback)
    window.attributes('-alpha', 0.9)


    bIN= Button(window,text = "In",width=10,command=lambda:update("In"));bIN.place(x = 10,y = 10)
    bOUT= Button(window,text = "Out",width=10,command=lambda:update("Out"));bOUT.place(x = 100,y = 10)
    L1=Label(window,fg="green");L1.place(x = 200,y = 15)

    L2=Label(window,fg="green");L2.place(x = 10,y = 55)
    L3=Label(window,fg="green");L3.place(x = 100,y = 55)


    Label(window, text='Date').place(x = 10,y = 80);    L4=Label(window,fg="green");            L4.place(x = 50,y = 80)
    Label(window, text='Time').place(x = 10,y = 110);    L5=Label(window,fg="green");            L5.place(x = 50,y = 110)
    Label(window, text='User').place(x = 10,y = 140);    L6=Label(window,text=user,fg="green");  L6.place(x = 50,y = 140)



    bmax= Button(window,text = "+",width=2,command=maximize,relief='flat');bmax.place(x = 230,y = 10)
    bref= Button(window,text = "!",width=2,command=refresh,relief='flat');bref.place(x = 250,y = 10)
    brec= Button(window,text = "recall",command=recall,relief='flat');brec.place(x = 230,y = 50)
    bcl= Button(window,text = "X",width=2,command=exitwin,relief='flat');bcl.place(x = 250,y = 480)

    cal =Calendar(window,font="Arial 8",cursor="hand1",background='green',foreground='white',selectbackground='green', borderwidth=2)
    cal.bind("<<CalendarSelected>>", check)
    cal.place(x = 30,y = 180)

    Label(window, text='In time').place(x = 10,y = 365);L7=Label(window,fg="green");L7.place(x = 80,y = 365)
    Label(window, text='Out time').place(x = 10,y = 385);L8=Label(window,fg="green");L8.place(x = 80,y = 385)

    bSTAT= Button(window,text = "Statistics",width=10,command=stat);bSTAT.place(x = 10,y = 420)
    Label(window, text='Version 7').place(x = 10,y = 460)
    Label(window, text='Updated On: 02/JAN/2020').place(x = 10,y = 480)

    l=Label(window,fg='red')

    refresh()
    tick()
    scroll()
    mainloop()
main()