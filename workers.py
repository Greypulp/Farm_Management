from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connection_database import connect_database


def clear(id_entry,name_entry,contact_entry,treeview):
        id_entry.delete(0,END)
        name_entry.delete(0,END)
        contact_entry.delete(0,END)
        treeview.selection_remove(treeview.selection())

def update_workers(id, name, contact, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to update')
        return

    item = treeview.item(selected_item)
    values = item['values']
    worker_id = values[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('UPDATE workers_data SET name=%s, contact=%s WHERE id=%s', (name, contact, worker_id))
        connection.commit()
        messagebox.showinfo('Success', 'Worker updated successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def delete_worker(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to delete')
        return

    item = treeview.item(selected_item)
    values = item['values']
    worker_id = values[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM workers_data WHERE id=%s', (worker_id,))
        connection.commit()
        messagebox.showinfo('Success', 'Worker deleted successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event,id_entry,name_entry,contact_entry,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    id_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])


def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('Select * from workers_data')
    records=cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for record in records:
        treeview.insert('',END,values=record)

def add_workers(id,name,contact,treeview):
    if id=='' or name=='' or contact=='': 
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS workers_data (id INT PRIMARY KEY,name VARCHAR(200), contact VARCHAR(15))')

        cursor.execute('INSERT INTO workers_data VALUES(%s,%s,%s)',(id,name,contact))
        connection.commit()
        messagebox.showinfo('Info','Data is inserted')
        treeview_data(treeview)


def search_workers(search_combobox, search_entry, treeview):
    if search_combobox.get() == 'Search By':
        messagebox.showerror('ERROR', 'Please select a search criteria')
    elif search_entry.get() == '':
        messagebox.showerror('ERROR', 'Please enter the value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_system')
            query = f"SELECT * FROM workers_data WHERE {search_combobox.get().lower()} LIKE %s"
            cursor.execute(query, ('%' + search_entry.get() + '%',))
            records = cursor.fetchall()
            if len(records) == 0:
                messagebox.showerror('Error', 'No record found')
                return

            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert('', END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def show_all_workers(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0, END)


def workers_form(window):
    global back_image
    worker_frame=Frame(window,width=1070,height=567,bg='white')
    worker_frame.place(x=200,y=100)

    heading_label=Label(worker_frame,text='List of Workers',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(worker_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: worker_frame.place_forget())
    back_button.place(x=10,y=30)

    left_frame = Frame(worker_frame,bg='white')
    left_frame.place(x=10,y=100)

    id_label=Label(left_frame,text='#',font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=(20,40), sticky='w')
    id_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Employee Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25, sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Contact',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40), sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :add_workers(id_entry.get(),name_entry.get(),contact_entry.get(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text='Update',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: update_workers(id_entry.get(), name_entry.get(), contact_entry.get(), treeview))
    update_button.grid(row=0,column=1)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_worker(treeview))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :clear(id_entry,name_entry,contact_entry,treeview))
    clear_button.grid(row=0,column=3)

    right_frame=Frame(worker_frame,bg='white')
    right_frame.place(x=520,y=95,width=500,height=350)

    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    search_combobox=ttk.Combobox(search_frame,values=('Name'),state='readonly',width=12,font=('times new roman',14))
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')

    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=15)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: search_workers(search_combobox, search_entry, treeview))
    search_button.grid(row=0,column=2,padx=15)

    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: show_all_workers(treeview, search_combobox, search_entry))
    show_button.grid(row=0,column=3,padx=10)
    
    
    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=('id','name','contact'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.pack()
    treeview.heading('id',text='#')
    treeview.heading('name',text='Employee Name')
    treeview.heading('contact',text='Employee Contact')

    treeview.column('id',width=5)
    treeview.column('name',width=160)
    treeview.column('contact',width=120)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,id_entry,name_entry,contact_entry,treeview))





