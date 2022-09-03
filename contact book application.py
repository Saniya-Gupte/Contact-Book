import tkinter
from tkinter import ttk
from tkinter import messagebox as m, TOP
import sqlite3

con = sqlite3.connect("contacts.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS CONTACT_BOOK(SR_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,NAME TEXT,"
            "PHONE TEXT,EMAIL TEXT,DOB TEXT)")


def add_record():  #Adds a new contact
    global name_var, phone_var, email_var, dob_var
    name, phone_no, email, dob = name_var.get(), phone_var.get(), email_var.get(), dob_var.get()
    if name == '' or phone_no == '':
        m.showerror('Error!', 'Name and Phone Number cannot be empty')
    else:
        cur.execute("INSERT INTO CONTACT_BOOK(NAME,PHONE,EMAIL,DOB) VALUES(?,?,?,?)", (name, phone_no, email, dob))
        con.commit()
        m.showinfo('Contact added', 'Contact added successfully')
        clear_records()
        list_of_contacts()


def list_of_contacts():
    for item in tree.get_children():
        tree.delete(item)
    cur.execute('SELECT NAME,PHONE,EMAIL,DOB FROM CONTACT_BOOK')
    for row in cur.fetchall():
        tree.insert("", tkinter.END, values=row)


def delete_record():  #deletes a selected contact
    selected = tree.focus()
    if selected == '':
        m.showerror("Error",'No Item Selected')

    temp = tree.item(selected, 'values')
    name = str(temp[0])
    sql_query = 'DELETE FROM CONTACT_BOOK WHERE NAME = "' + name + '"'
    cur.execute(sql_query)
    con.commit()

    m.showinfo('Contact deleted', 'The desired contact has been deleted')
    tree.delete(selected)


def delete_all():  #deletes all the contacts in the contact book

    sql_query = 'DELETE FROM CONTACT_BOOK'
    cur.execute(sql_query)
    con.commit()

    m.showinfo('Message', 'All contacts have been deleted')
    for item in tree.get_children():
        tree.delete(item)

def view_record():  #searches for a contact
    query = str(name_var.get())
    cur.execute('SELECT NAME,PHONE,EMAIL,DOB FROM CONTACT_BOOK WHERE NAME LIKE ?', ('%' + query + '%',))
    for item in tree.get_children():
        tree.delete(item)
    for row in cur.fetchall():
        tree.insert("", tkinter.END, values=row)


def clear_records():
    name_var.set('')
    phone_var.set('')
    email_var.set('')
    dob_var.set('')


# GUI WINDOW
window = tkinter.Tk()
window.geometry('1200x550')
frame = tkinter.Frame(window)
frame.place(relx=0, relheight=1, y=0, relwidth=1)

name_var = tkinter.StringVar()
phone_var = tkinter.StringVar()
email_var = tkinter.StringVar()
dob_var = tkinter.StringVar()

window.title("Contact Book")
label = tkinter.Label(window, text='CONTACT BOOK')
label.pack(side=TOP)

label1 = tkinter.Label(frame, text='Name')
label1.place(relx=0.0, rely=0.1)
entry1 = tkinter.Entry(frame, textvariable=name_var)
entry1.place(relx=0.1, rely=0.1)

label2 = tkinter.Label(frame, text='Phone No')
label2.place(relx=0.2, rely=0.1)
entry1 = tkinter.Entry(frame, textvariable=phone_var)
entry1.place(relx=0.3, rely=0.1)

label3 = tkinter.Label(frame, text='Email')
label3.place(relx=0.0, rely=0.2)
entry1 = tkinter.Entry(frame, textvariable=email_var)
entry1.place(relx=0.1, rely=0.2)

label4 = tkinter.Label(frame, text='Date of Birth')
label4.place(relx=0.2, rely=0.2)
entry1 = tkinter.Entry(frame, textvariable=dob_var)
entry1.place(relx=0.3, rely=0.2)

button1 = tkinter.Button(frame, text='Add Contact', width=15, command=add_record)
button1.place(relx=0.0, rely=0.3)

button2 = tkinter.Button(frame, text='Delete Contact', width=15, command=delete_record)
button2.place(relx=0.1, rely=0.3)

button3 = tkinter.Button(frame, text='Search', width=15, command=view_record)
button3.place(relx=0.2, rely=0.3)

button4 = tkinter.Button(frame, text='Delete All Contacts', width=16, command=delete_all)
button4.place(relx=0.3, rely=0.3)

tree = ttk.Treeview(frame, column=("c1", "c2", "c3", "c4"), show='headings')
tree.place(relx=0.0, rely=0.4)

tree.column("#1", anchor=tkinter.CENTER)

tree.heading("#1", text="Name")

tree.column("#2", anchor=tkinter.CENTER)

tree.heading("#2", text="Phone No")

tree.column("#3", anchor=tkinter.CENTER)

tree.heading("#3", text="Email")

tree.column("#4", anchor=tkinter.CENTER)

tree.heading("#4", text="Date of Birth")

list_of_contacts()

window.mainloop()
