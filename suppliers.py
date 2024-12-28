from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connection_database import connect_database

def delete_supplier(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to delete')
        return

    item = treeview.item(selected_item)
    values = item['values']
    supplier_id = values[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE id=%s', (supplier_id,))
        connection.commit()
        messagebox.showinfo('Success', 'Supplier deleted successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def clear(id_entry,name_entry,contact_entry,location_text,treeview):
        id_entry.delete(0,END)
        name_entry.delete(0,END)
        contact_entry.delete(0,END)
        location_text.delete(1.0,END)
        treeview.selection_remove(treeview.selection())

def search_supplier(search_supplier,treeview):
    if search_supplier=='': 
        messagebox.showerror('ERROR', 'Please enter supplier Name.')
    else:
        cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * from supplier_data')
        record=cursor.fetchone()
        if not record:
            messagebox.showerror('Error', 'No record found')
            return

        treeview.delete(*treeview.get_children())
        treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()  

def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)

    

def update_supplier(id,name,contact,location,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * from supplier_data WHERE name=%s',name)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        new_data=(id,name,contact,location)
     
        if current_data==new_data:
            messagebox.showinfo('Info', 'No changes detected')

        cursor.execute('UPDATE supplier_Data SET id=%s, name=%s, contact=%s, location=%s',(id,name,contact,location))
        connection.commit()
        messagebox.showinfo('Info', 'Data is updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()

def select_data(event,id_entry,name_entry,contact_entry,location_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    location_text.delete(1.0,END)
    id_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    location_text.insert(1.0,actual_content[3])


def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('Select * from supplier_data')
    records=cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for record in records:
        treeview.insert('',END,values=record)

def add_supplier(id,name,contact,location,treeview):
    if id=='' or name=='' or contact=='' or location=='': 
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data (id INT PRIMARY KEY,name VARCHAR(200), contact VARCHAR(15), location TEXT)')

        cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)',(id,name,contact,location))
        connection.commit()
        messagebox.showinfo('Info','Data is inserted')
        treeview_data(treeview)


def supplier_form(window):
    global back_image
    supplier_frame=Frame(window,width=1070,height=567,bg='white')
    supplier_frame.place(x=200,y=100)

    heading_label=Label(supplier_frame,text='Supplie Names',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)  
    back_image=PhotoImage(file='back_button.png')
    back_button=Button(supplier_frame,image=back_image,bd=0,cursor='hand2',bg='white',command=lambda: supplier_frame.place_forget())
    back_button.place(x=10,y=30)

    left_frame = Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)

    supplier_id_label=Label(left_frame,text='Supplier Id',font=('times new roman',14,'bold'),bg='white')
    supplier_id_label.grid(row=0,column=0,padx=(20,40), sticky='w')
    supplier_id_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    supplier_id_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Supplier Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25, sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Contact',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40), sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    location_label=Label(left_frame,text='Location',font=('times new roman',14,'bold'),bg='white')
    location_label.grid(row=3,column=0,padx=(20,40),sticky='nw',pady=25)
    location_text=Text(left_frame,width=25,height=1.5,bd=2,bg='lightyellow')
    location_text.grid(row=3,column=1,pady=25)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :add_supplier(supplier_id_entry.get(),name_entry.get(),contact_entry.get(),location_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text='Update',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :update_supplier(supplier_id_entry.get(),name_entry.get(),contact_entry.get(),location_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_supplier(treeview))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :clear(supplier_id_entry,name_entry,contact_entry,location_text,treeview))
    clear_button.grid(row=0,column=3)

    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=520,y=95,width=500.,height=350)

    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Supplier Name',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15), sticky='w')
    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=15)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0,column=2,padx=15)

    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda :show_all(treeview,search_entry))
    show_button.grid(row=0,column=3)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=('id','name','contact','location'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.pack()
    treeview.heading('id',text='#')
    treeview.heading('name',text='Supplier Name')
    treeview.heading('contact',text='Supplier Contact')
    treeview.heading('location',text='location')

    treeview.column('id',width=5)
    treeview.column('name',width=160)
    treeview.column('contact',width=120)
    treeview.column('location',width=50)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,supplier_id_entry,name_entry,contact_entry,location_text,treeview))





