from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connection_database import connect_database
from tkcalendar import DateEntry

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('Select * from assignments_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()

def fetch_worker(worker_combobox):
    worker_option=[]
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT name from workers_data')
    names=cursor.fetchall()
    if len(names)>0:
        worker_combobox.set('Select')
        for name in names:
            worker_option.append(name[0])
        worker_combobox.config(values=worker_option)


def add_assignments(date,worker,work,block,amount,treeview):
    if worker=='Empty':
        messagebox.showerror('Error','Please add Workers Name')
    elif work=='Empty':
        messagebox.showerror('Error','Please add Task')
    elif block=='Empty':
        messagebox.showerror('Error','Please add Block')
    elif worker=='Select' or work=='Select' or block=='Select' or amount=='Empty':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS assignments_data (date VARCHAR(30), worker VARCHAR(50), work VARCHAR(50), block VARCHAR(30), amount INT)')

        cursor.execute('SELECT * from assignments_data WHERE date=%s AND worker=%s AND work=%s AND block=%s AND amount=%s',(date,worker,work,block,amount))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error','Product already exists')
            return

        cursor.execute('INSERT INTO assignments_data (date,worker,work,block,amount) VALUES(%s,%s,%s,%s,%s)',(date,worker,work,block,amount))

        connection.commit()
        messagebox.showinfo('Success','Data is added successfully')

def delete_assignments(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to delete')
        return

    item = treeview.item(selected_item)
    values = item['values']
    date, worker, work, block, amount = values

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM assignments_data WHERE date=%s AND worker=%s AND work=%s AND block=%s AND amount=%s',
                       (date, worker, work, block, amount))
        connection.commit()
        messagebox.showinfo('Success', 'Assignment deleted successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def update_assignments(date, worker, work, block, amount, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to update')
        return

    item = treeview.item(selected_item)
    old_values = item['values']
    old_date, old_worker, old_work, old_block, old_amount = old_values

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('UPDATE assignments_data SET date=%s, worker=%s, work=%s, block=%s, amount=%s WHERE date=%s AND worker=%s AND work=%s AND block=%s AND amount=%s',
                       (date, worker, work, block, amount, old_date, old_worker, old_work, old_block, old_amount))
        connection.commit()
        messagebox.showinfo('Success', 'Assignment updated successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def search_assignments(search_by, search_value, treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        query = f"SELECT * FROM assignments_data WHERE {search_by} LIKE %s"
        cursor.execute(query, ('%' + search_value + '%',))
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def select_assignments(event,treeview, date_entry, workers_combobox, work_entry, block_entry, amount_entry):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    date_entry.delete(0,END)
    workers_combobox.delete(0,END)
    work_entry.delete(0,END)
    block_entry.delete(0,END)
    amount_entry.delete(0,END)
    workers_combobox.set(content[1])
    date_entry.insert(0,content[2])
    work_entry.insert(0,content[3])
    block_entry.insert(0,content[4])
    amount_entry.insert(0,content[5])

def refresh_assignments(treeview):
    treeview_data(treeview)

def show_all_assignments(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0, END)
    
def assignments_form(window):
    global back_image
    tasks_frame=Frame(window,width=1070,height=567,bg='white')
    tasks_frame.place(x=200,y=100)
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(tasks_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: tasks_frame.place_forget())
    back_button.place(x=10,y=10)

    left_frame = Frame(tasks_frame,bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=20,y=60)

    heading_label=Label(left_frame,text='Task Assignment',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.grid(row=0,column=0,columnspan=2)

    date_label=Label(left_frame,text='Date',font=('times new roman',14,'bold'),bg='white')
    date_label.grid(row=1,column=0,padx=20,sticky='w')
    date_entry=DateEntry(left_frame,font=('times new roman',14,'bold'),width=18)
    date_entry.grid(row=1,column=1)

    workers_label=Label(left_frame,text='Employee Name',font=('times new roman',14,'bold'),bg='white')
    workers_label.grid(row=2,column=0,padx=20,sticky='w')
    workers_combobox=ttk.Combobox(left_frame,font=('times new roman',14,'bold'),width=18,state='readonly')
    workers_combobox.grid(row=2,column=1,pady=10)
    workers_combobox.set('Empty')

    work_label=Label(left_frame,text='Task Allocated',font=('times new roman',14,'bold'),bg='white')
    work_label.grid(row=3,column=0,padx=20,sticky='w')
    work_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    work_entry.grid(row=3, column=1,pady=20)

    block_label=Label(left_frame,text='Block',font=('times new roman',14,'bold'),bg='white')
    block_label.grid(row=4,column=0,padx=20,sticky='w')
    block_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    block_entry.grid(row=4, column=1,pady=20)

    amount_label=Label(left_frame,text='Pay',font=('times new roman',14,'bold'),bg='white')
    amount_label.grid(row=5,column=0,padx=20,sticky='w')
    amount_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    amount_entry.grid(row=5, column=1,pady=20)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=7,columnspan=2,pady=(30,10))

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :add_assignments(date_entry.get(),workers_combobox.get(),work_entry.get(),block_entry.get(),amount_entry.get(),treeview))
    add_button.grid(row=0,column=0,padx=10)

    update_button=Button(button_frame,text='Update',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: update_assignments(date_entry.get(),workers_combobox.get(),work_entry.get(),block_entry.get(),amount_entry.get(),treeview))
    update_button.grid(row=0,column=2,padx=10)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_assignments(treeview))
    delete_button.grid(row=0,column=3,padx=10)

    refresh_button=Button(button_frame,text='Refresh',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: refresh_assignments(treeview))
    refresh_button.grid(row=0,column=4,padx=10)

    right_frame=Frame(tasks_frame,bg='white')
    right_frame.place(x=450,y=5,width=590,height=200)

    search_frame=LabelFrame(right_frame,text='Search Assignment',font=('times new roman',12,'bold'),bg='white')
    search_frame.place(x=20,y=10)

    search_combobox=ttk.Combobox(search_frame,values=('Date','Worker','Work','Block'),state='readonly',width=12,font=('times new roman',14))
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')

    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=16)
    search_entry.grid(row=0, column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: search_assignments(search_combobox.get().lower(), search_entry.get(), treeview))
    search_button.grid(row=0,column=2,padx=(10,0),pady=10)

    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: show_all_assignments(treeview, search_combobox, search_entry))
    show_button.grid(row=0,column=3,padx=10)

    treeview_frame=Frame(tasks_frame)
    treeview_frame.place(x=480, y=100,width=570,height=450)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=('date','workers','work','block','amount'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)

    treeview.heading('date',text='Date')
    treeview.heading('workers',text='Name')
    treeview.heading('work',text='Task')
    treeview.heading('block',text='Block')
    treeview.heading('amount',text='Pay')

    treeview.column('date',width=15)
    treeview.column('workers',width=50)
    treeview.column('work',width=50)
    treeview.column('block',width=5)
    treeview.column('amount',width=20)

    treeview_data(treeview)  # Call to populate the treeview with data
    fetch_worker(workers_combobox)
    treeview.bind('<<TreeviewSelect>>', lambda event: select_assignments(event,treeview, date_entry, workers_combobox, work_entry, block_entry, amount_entry))