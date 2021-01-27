from tkinter import *
import subprocess as sp

__author__ = " Falsarolo Leonardo & De Battisti Tommaso & Scamperle Mattia"
__version__ = "1.2 2021-01-20"


def submit():
    # fix parameters
    v = ""
    vonly = "--vonly=" + v0.get()
    frm = "--format=" + v11.get().replace("'", "").replace('"', "")
    lgfile = "--logfile=" + v41.get()
    if v41.get() == "":
        lgfile = ""
    if v0.get() == "":
        vonly = ""
    if v11.get() == "":
        frm = ""

    # launching programs
    if v6.get() == 1:
        v = "-v"
    if v1.get() == 1:
        sp.run(["py", "netinfo.py", v, vonly, frm])
    if v2.get() == 1:
        sp.run(["py", "osversion.py", v, vonly])
    if v3.get() == 1:
        sp.run(["py", "product.py", v, vonly])
    if v4.get() == 1:
        sp.run(["py", "eventsview.py", v, vonly, lgfile])
    if v5.get() == 1:
        sp.run(["py", "ldisk.py", v, vonly])


def sync():
    sp.run("py sync.py")


if __name__ == "__main__":
    root = Tk()
    root.geometry("450x250")
    root.title("AGENT")
    root.configure(background="#262626")
    root.resizable(0, 0)

    v1 = IntVar()
    l1 = StringVar()
    v2 = IntVar()
    l2 = StringVar()
    v3 = IntVar()
    l3 = StringVar()
    v4 = IntVar()
    l4 = StringVar()
    v5 = IntVar()
    l5 = StringVar()
    v6 = IntVar()
    l6 = StringVar()

    v0 = StringVar()   # verboseonly
    v41 = StringVar()  # eventsview's registry
    v11 = StringVar()  # netinfo's mac address format

    b1 = Checkbutton(root, text="netinfo", variable=v1, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=0)
    b2 = Checkbutton(root, text="osversion", variable=v2, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=30)
    b3 = Checkbutton(root, text="product", variable=v3, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=60)
    b4 = Checkbutton(root, text="eventsview", variable=v4, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=90)
    b5 = Checkbutton(root, text="ldisk", variable=v5, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=120)
    b6 = Checkbutton(root, text="verbose", variable=v6, bg="#262626", selectcolor="orange", fg="white",
                     activeforeground="orange", activebackground="#262626", font=("Arial", "15")).place(x=10, y=150)
    b7 = Label(root, text="Show only", bg="#262626", fg="white", font=("Arial", "15")).place(x=200, y=152)
    b8 = Entry(root, textvariable=v0).place(x=300, y=158)

    Button(root, text="Submit", command=submit, bg="lime", font=("Arial", "13", "bold")).place(x=10, y=190)
    Button(root, text="Sync", command=sync, bg="orange", font=("Arial", "13", "bold")).place(x=90, y=190)
    Button(root, text="Exit", command=root.quit, bg="red", font=("Arial", "13", "bold")).place(x=154, y=190)

    b41 = Radiobutton(root, text="Application", variable=v41, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value="Application").place(x=150, y=96)
    b42 = Radiobutton(root, text="System", variable=v41, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value="System").place(x=240, y=96)
    b43 = Radiobutton(root, text="Security", variable=v41, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value="Security").place(x=300, y=96)

    b11 = Radiobutton(root, text=":", variable=v11, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value=":", font=("Arial", "12")).place(
        x=150, y=0)
    b12 = Radiobutton(root, text="-", variable=v11, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value="-", font=("Arial", "12")).place(
        x=190, y=0)
    b13 = Radiobutton(root, text="empty", variable=v11, bg="#262626", selectcolor="orange", fg="white",
                      activeforeground="orange", activebackground="#262626", value="'", font=("Arial", "12")).place(
        x=230, y=0)

    root.mainloop()
