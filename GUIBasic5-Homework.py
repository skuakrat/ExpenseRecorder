from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter.ttk import Notebook
from tkinter import messagebox, filedialog
import csv
import os
from csv import DictReader

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย v.1.0 by ชามา')
GUI.geometry('500x650')

###################################### Menu

menubar = Menu(GUI)
GUI.config(menu=menubar)

#menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
def About():
        messagebox.showinfo('About','โปรแกรมบันทึกค่าใช้จ่ายเขียนจาก tkinter\nด้วยภาษา Python')
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
def Donate():
	messagebox.showinfo('Donate','โปรดสนับสนุนเพื่อเป็นปัจจัยในการศึกษาต่อไป')
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)



######################################


FONT1 = (None,20)
FONT2 = (None,14)
nl = '\n'

F1 = Frame(GUI)
F1.place(x=100,y=50)

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัส',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Syn':'อาทิตย์'}




##############
Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)

Tab.pack(fill=BOTH, expand=1)

try:

	add = PhotoImage(file='add.png').subsample(4, 4)
	hist = PhotoImage(file='his.png').subsample(4, 4)

	Tab.add(T1, text=f'{"เพิ่ม": ^{20}}', image=add,compound='top')
	Tab.add(T2, text=f'{"ประวัติ": ^{20}}', image=hist,compound='top')

except:
	Tab.add(T1, text=f'{"เพิ่ม": ^{20}}')
	Tab.add(T2, text=f'{"ประวัติ": ^{20}}')


	
##############

	

img_cart = PhotoImage(file='cart.png')
logo = ttk.Label(T1,text='เพิ่ม',image=img_cart)
logo.pack()

F1 = Frame(T1)
F1.pack()


        

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '' or price == '' and quantity == '':
            print('No Data')
            messagebox.showwarning('Error','กรุณากรอกข้อมูลให้ครบ')
            return
    elif price == '':
            print('No Data')
            messagebox.showwarning('Error','กรุณากรอกราคา')
            return
    elif quantity == '':
            print('No Data')
            messagebox.showwarning('Error','กรุณากรอกจำนวน')
            return
        
    try:
            total = float(price)*float(quantity)
            today = datetime.now().strftime('%a')
            dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            dt = days[today] + '-' + dt
            print('รายการ: {} ราคา: {} จำนวน: {} รวม: {} เวลา: {}'.format(expense,price,quantity,total,dt))
            v_expense.set('')
            v_price.set('')
            v_quantity.set('')
            text = f"รายการ: {expense} ราคา: {price} จำนวน: {quantity} รวม: {total}{nl}เวลา: {dt}"
            v_result.set(text)
            with open('savedata.csv','a',newline='',encoding='utf-8') as f:
                fw = csv.writer(f)
                data = [expense,price,quantity,total,dt]
                fw.writerow(data)
            E1.focus()
    except Exception as e:
            print('ERROR')
            messagebox.showwarning('Error','กรุณากรอกใหม่ ข้อความไม่ถูกต้อง')

GUI.bind('<Return>',Save)
        


L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

L = ttk.Label(F1,text='ราคา(บาท)',font=FONT1).pack()
v_price = IntVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

L = ttk.Label(F1,text='จำนวน(ชิ้น)',font=FONT1).pack()
v_quantity = IntVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()

save = PhotoImage(file='save.png').subsample(6, 6)
#B2 = ttk.Button(F1,text='Save',image=save,compound='left', command=Save)
B2 = ttk.Button(F1,text='Save',image=save,compound='left', command=lambda:[Save(),fetchdata()])
B2.pack(ipadx=50,ipady=20,pady=40)

v_result = StringVar()
v_result.set('--------ผลลัพธ์---------')
result = ttk.Label(F1, textvariable=v_result,font=FONT2)
result.pack()

################################################################## TAB 2

F2 = Frame(T2)
F2.pack()

L = ttk.Label(F2,text='ประวัติการใช้จ่าย',font=FONT1).pack()
v_expensenum = StringVar()

tree = ttk.Treeview(F2)
tree['columns'] = ("DT", "ITEM", "QTY", "PRICE", "TOTAL")
tree.column("#0", width=0)
tree.column("DT", anchor=W, width=80)
tree.column("ITEM", anchor=W, width=120)
tree.column("QTY", anchor=CENTER, width=80)
tree.column("PRICE", anchor=CENTER, width=80)
tree.column("TOTAL", anchor=CENTER, width=80)

tree.heading("0", text="Label",anchor=CENTER)
tree.heading("DT", text="วันที่",anchor=CENTER)
tree.heading("ITEM", text="รายการ",anchor=CENTER)
tree.heading("QTY", text="จำนวน",anchor=CENTER)
tree.heading("PRICE", text="ราคา",anchor=CENTER)
tree.heading("TOTAL", text="ราคาสุทธิ",anchor=CENTER)




tree.pack(pady=20)

def fetchdata():
        tree.delete(*tree.get_children())
        with open('savedata.csv', encoding='utf-8') as csvf:
            reader = csv.DictReader(csvf, delimiter=',')
            for row in reader:
                citem = row['item']
                cprice = row['price']
                cqty = row['qty']
                ctotal = row['total']
                cdt = row['dt']
                tree.insert(parent='', index='end', iid=row, text="", values=(cdt,citem,cqty,cprice,ctotal))
                print(citem)
                
# Tab.bind('<<NotebookTabChanged>>', fetchdata)
fetchdata()



GUI.mainloop()
