from tkinter import *
from suppliers import supplier_form
from inventory import product_form
from assignments import assignments_form
from workers import workers_form
from category import category_form
import time

#GUI Part
window=Tk()

window.title('Dashboard')
window.geometry('1270x668+0+0')
window.config(bg='white')


bg_image=PhotoImage(file='inventory.png')
titlelabel=Label(window,image=bg_image,compound=LEFT,text='  Farm Management System',font=('Aptos',40,'bold'),bg='#010c48',fg='white',anchor='w',padx=20)
titlelabel.place(x=0,y=0,relwidth=1)

logoutbutton=Button(window,text='Logout',font=('Aptos',20,'bold'),bg='#010c48',fg='white')
logoutbutton.place(x=1100,y=10)

def update_time():
    current_time = time.strftime('%d-%m-%Y %I:%M:%S %p')
    subtitlelabel.config(text=f'Welcome Admin\t\t Date: {current_time}')
    window.after(1000, update_time)

subtitlelabel=Label(window,text='', font=('Aptos',20),bg='#4d636d',fg='white')
subtitlelabel.place(x=0,y=60, relwidth=1)
update_time()

leftFrame=Frame(window)
leftFrame.place(x=0,y=102,width=200,height=555)

logoImage=PhotoImage(file='logo.png')
ImageLabel=Label(leftFrame,image=logoImage)
ImageLabel.pack()

menuLabel=Label(leftFrame,text='Menu',font=('Aptos',20,),bg='#009688')
menuLabel.pack(fill=X)

suppliers_icon=PhotoImage(file='suppliers.png')
suppliers_button=Button(leftFrame,image=suppliers_icon,compound=LEFT,text='Suppliers',font=('Aptos',20,'bold'),anchor='w',padx=10,command=lambda:supplier_form(window))
suppliers_button.pack(fill=X)

category_icon=PhotoImage(file='category.png')
category_button=Button(leftFrame,image=category_icon,compound=LEFT,text='Category',font=('Aptos',20,'bold'),anchor='w',padx=10,command=lambda:category_form(window))
category_button.pack(fill=X)

workers_icon=PhotoImage(file='staff.png')
workers_button=Button(leftFrame,image=suppliers_icon,compound=LEFT,text='Workers',font=('Aptos',20,'bold'),anchor='w',padx=10,command=lambda:workers_form(window))
workers_button.pack(fill=X)

inventory_icon=PhotoImage(file='product.png')
inventory_button=Button(leftFrame,image=inventory_icon,compound=LEFT,text='Inventory',font=('Aptos',20,'bold'),anchor='w',padx=10,command=lambda :product_form(window))
inventory_button.pack(fill=X)

tasks_icon=PhotoImage(file='product.png')
tasks_button=Button(leftFrame,image=tasks_icon,compound=LEFT,text='Daily Tasks',font=('Aptos',20,'bold'),anchor='w',padx=10,command=lambda :assignments_form(window))
tasks_button.pack(fill=X)

exit_icon=PhotoImage(file='exit.png')
exit_button=Button(leftFrame,image=exit_icon,compound=LEFT,text='Exit',font=('Aptos',20,'bold'),anchor='w',padx=10)
exit_button.pack(fill=X)


emp_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,height=160,width=280)
total_emp_icon=PhotoImage(file='total_emp.png')
total_emp_icon_label=Label(emp_frame,image=total_emp_icon,bg='#27AE60')
total_emp_icon_label.pack()

total_emp_label=Label(emp_frame,text='Total Employees',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_emp_label.pack()

total_emp_count_label=Label(emp_frame,text='50',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_emp_count_label.pack()


sup_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
sup_frame.place(x=800,y=125,height=160,width=280)
total_sup_icon=PhotoImage(file='total_sup.png')
total_sup_icon_label=Label(sup_frame,image=total_sup_icon,bg='#27AE60')
total_sup_icon_label.pack()

total_sup_label=Label(sup_frame,text='Total Suppliers',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_sup_label.pack()

total_sup_count_label=Label(sup_frame,text='50',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_sup_count_label.pack()

cat_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
cat_frame.place(x=400,y=310,height=160,width=280)
total_cat_icon=PhotoImage(file='total_cat.png')
total_cat_icon_label=Label(cat_frame,image=total_cat_icon,bg='#27AE60')
total_cat_icon_label.pack()

total_cat_label=Label(cat_frame,text='Total Categories',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_cat_label.pack()

total_cat_count_label=Label(cat_frame,text='50',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_cat_count_label.pack()

prod_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
prod_frame.place(x=800,y=310,height=160,width=280)
total_prod_icon=PhotoImage(file='total_prod.png')
total_prod_icon_label=Label(prod_frame,image=total_prod_icon,bg='#27AE60')
total_prod_icon_label.pack()

total_prod_label=Label(prod_frame,text='Total Products',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_prod_label.pack()

total_prod_count_label=Label(prod_frame,text='50',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_prod_count_label.pack()

sale_frame=Frame(window,bg='#27AE60',bd=3,relief=RIDGE)
sale_frame.place(x=600,y=495,height=160,width=280)
total_sale_icon=PhotoImage(file='total_sal.png')
total_sale_icon_label=Label(sale_frame,image=total_sale_icon,bg='#27AE60')
total_sale_icon_label.pack()

total_sale_label=Label(sale_frame,text='Total Sales',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_sale_label.pack()

total_sale_count_label=Label(sale_frame,text='50',fg='white',font=('Aptos', 20,'bold'),bg='#27AE60')
total_sale_count_label.pack()


window.mainloop()
