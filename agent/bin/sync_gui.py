from tkinter import *
import subprocess as sp
import os

__authors__ = "De Battisti Tommaso & Falsarolo Leonardo & Scamperle Mattia"
__version__ = "1.1 2021-01-10"


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, bg="#262626")
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


def submit():
    ip = d_entry.get()
    pathsearch = a_entry.get()
    path = b_entry.get()
    user = e_entry.get()
    passwd = f_entry.get()
    checkstate(ip, pathsearch, path, user, passwd)


def erease():
    d.set("")
    a.set("")
    b.set("")
    e.set("")
    f.set("")


def checkstate(ip, paths, path, user, passwd):
    """Checks the state of the items and executes the program using the given params
    """
    if ip != "" and paths != "" and path != "" and files != "":
        sp.run(["py", "sync.py",
                "--ipaddr=" + ip,
                "--pathsearch=" + paths,
                "--targetpath=" + path,
                "--username=" + user,
                "--password=" + passwd
                ])
    else:
        pass
    return


def example():
    a.set("..")
    d.set("192.168.1.128")
    b.set("test_sync")
    e.set("admin")
    f.set("pud596je")


if __name__ == '__main__':
    root = Tk()
    root.geometry("460x115")
    root.title("SYNC")
    d = StringVar()
    a = StringVar()
    b = StringVar()
    e = StringVar()
    f = StringVar()
    g = StringVar()
    root.configure(bg="#262626")
    root.resizable(0, 0)

    a_label = Label(text="Local folder", bg="#262626", font=('calibre', 10, 'bold'), fg="white")
    a_entry = Entry(root, textvariable=a, font=('calibre', 10, 'normal'))
    b_label = Label(text="Shared folder", bg="#262626", font=('calibre', 10, 'bold'), fg="white")
    b_entry = Entry(root, textvariable=b, font=('calibre', 10, 'normal'))
    d_label = Label(text='Hostname', font=('calibre', 10, 'bold'), fg="white", bg="#262626")
    d_entry = Entry(root, textvariable=d, font=('calibre', 10, 'normal'))
    e_label = Label(text="Username", font=('calibre', 10, 'bold'), fg="white", bg="#262626")
    e_entry = Entry(root, textvariable=e, font=('calibre', 10, 'normal'))
    f_label = Label(text="Password", font=('calibre', 10, 'bold'), fg="white", bg="#262626")
    f_entry = Entry(root, textvariable=f, font=('calibre', 10, 'normal'), show="*")
    bottone = Button(root, text='Exit', command=root.quit, font=('calibre', 10, 'bold'), bg="red")
    sub_btn = Button(root, text='Submit', command=submit, font=('calibre', 10, 'bold'), bg="#80ff00")
    reset = Button(root, text='Reset', command=erease, font=('calibre', 10, 'bold'), bg="orange")
    exmpl = Button(root, text='Example', command=example, font=('calibre', 10, 'bold'), bg="purple")
    files = Label(textvariable=g, font=('calibre', 10, 'bold'), fg="white", bg="#262626")

    d_label.grid(row=1, column=0)
    d_entry.grid(row=1, column=1)
    a_label.grid(row=3, column=0)
    a_entry.grid(row=3, column=1)
    b_label.grid(row=2, column=0)
    b_entry.grid(row=2, column=1)
    e_label.grid(row=1, column=2)
    e_entry.grid(row=1, column=3)
    f_label.grid(row=2, column=2)
    f_entry.grid(row=2, column=3)
    sub_btn.place(x=10, y=75)
    reset.place(x=75, y=75)
    bottone.place(x=130, y=75)
    exmpl.place(x=385, y=75)
    files.place(x=300, y=75)

    root.mainloop()
