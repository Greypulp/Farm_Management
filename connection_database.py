from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql

def connect_database():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='1234')
        cursor=connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue, please open mysql command line client')
        return None, None
    return cursor,connection
