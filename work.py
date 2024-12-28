from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connection_database import connect_database

def delete_work(id,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM work_data WHERE =%s',id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info', 'Record is deleted')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()


def clear(id_entry,name_entry,treeview):
        id_entry.delete(0,END)
        name_entry.delete(0,END)
        treeview.selection_remove(treeview.selection())

def search_work(search_combobox,search_entry,treeview):
    if search_combobox.get=='Search By':
        messagebox.showerror('ERROR', 'Please enter Employee Name')
    elif search_entry.get=='':
        messagebox.showerror('ERROR', 'Please enter the Name to Search')
    else:
        cursor,connection=connect_database()
    if not cursor or not connection:
        return
    
    cursor.execute('use inventory_system')
    cursor.execute(f'SELECT * from work_data WHERE {search_combobox.get()}=%s',search_entry.get())
    record=cursor.fetchall()
    if len(record)==0:
        messagebox.showerror('Error', 'No record found')
        return

    treeview.delete(*treeview.get_children())
    for record in record:
        treeview.insert('',END, values=record)

def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)



def select_data(event,id_entry,name_entry,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    id_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
   
def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('Select * from work_data')
    records=cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for record in records:
        treeview.insert('',END,values=record)

def add_work(id,type,treeview):
    if id=='' or type=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS work_data (id INT PRIMARY KEY,type VARCHAR(200))')

        cursor.execute('INSERT INTO work_data VALUES(%s,%s)',(id,type))
        connection.commit()
        messagebox.showinfo('Info','Data is inserted')
        treeview_data(treeview)


def work_form(window):
    global back_image
    work_frame=Frame(window,width=1070,height=567,bg='white')
    work_frame.place(x=200,y=100)

    heading_label=Label(work_frame,text='Work Type',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(work_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: work_frame.place_forget())
    back_button.place(x=10,y=30)

    left_frame = Frame(work_frame,bg='white')
    left_frame.place(x=10,y=100)

    id_label=Label(left_frame,text='#',font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=(20,40), sticky='w')
    id_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Work Type',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25, sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :add_work(id_entry.get(),name_entry.get(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :delete_work(id_entry.get(),name_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=20)


    right_frame=Frame(work_frame,bg='white')
    right_frame.place(x=520,y=95,width=500.,height=350)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=('id','type'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.pack()
    treeview.heading('id',text='#')
    treeview.heading('name',text='Work Type')
    
    treeview.column('id',width=5)
    treeview.column('name',width=160)
   
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,id_entry,name_entry,treeview))
    





