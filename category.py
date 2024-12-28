from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connection_database import connect_database

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('Select * from category_data')
    records=cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for record in records:
        treeview.insert('',END,values=record)

def add_category(id,name,treeview):
    if id=='' or name=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY,name VARCHAR(200))')

        cursor.execute('INSERT INTO category_data VALUES(%s,%s)',(id,name))
        connection.commit()
        messagebox.showinfo('Info','Data is inserted')
        treeview_data(treeview)

def category_form(window):
    global back_image
    category_frame=Frame(window,width=1070,height=567,bg='white')
    category_frame.place(x=200,y=100)

    heading_label=Label(category_frame,text='Category Names',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)  
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(category_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: category_frame.place_forget())
    back_button.place(x=10,y=30)

    left_frame = Frame(category_frame,bg='white')
    left_frame.place(x=10,y=100)

    id_label=Label(left_frame,text='category Id',font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=(20,40), sticky='w')
    id_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Category Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25, sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command= lambda:add_category(id_entry.get(),name_entry.get(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text='Update',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    update_button.grid(row=0,column=1)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    clear_button.grid(row=0,column=3)

    right_frame=Frame(category_frame,bg='white')
    right_frame.place(x=520,y=95,width=500.,height=350)

    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Category Name',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15), sticky='w')
    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=15)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    search_button.grid(row=0,column=2,padx=15)

    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d')
    show_button.grid(row=0,column=3)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=('id','name'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.pack()
    treeview.heading('id',text='#')
    treeview.heading('name',text='category Name')
   
    treeview.column('id',width=5)
    treeview.column('name',width=16)
   
    treeview_data(treeview)