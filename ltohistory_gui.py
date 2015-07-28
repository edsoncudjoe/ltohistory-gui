import sys
import json
import Tkinter as tk
import ttk
import tkFileDialog

sys.path.insert(0, '../ltohistory')
sys.path.insert(0, '../py-catdv')
#from ltohistory import get_json, json_to_list, json_final
from pycatdv import Catdvlib

# users may want to save results as text file.
# user wants to quit application

c = Catdvlib()

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.build_variables()
        self.login_window()

        # Main
        self.locate_frame = tk.Frame(self.parent, bg='yellow', padx=10,
                                     pady=10)
        self.locate_frame.grid(row=0, column=0)

        self.lto_btn = ttk.Button(self.locate_frame, text="Open LTO file",
                                  command=self.print_logins)

        self.lto_file_label = tk.Label(self.locate_frame, width=50,
                                       textvariable=self.fstatus)
        self.get_data_btn = ttk.Button(self.locate_frame,
                                       text="Get archived data",
                                       width=30)
        self.results = tk.Listbox(self.locate_frame, width=90)

        self.lto_btn.grid(row=0, column=0, pady=5)
        self.lto_file_label.grid(row=0, column=1, pady=5)
        self.get_data_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.results.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def login_window(self):
        # user needs to log in to CatDV
        self.login_win = tk.Toplevel(self, bg='green', width=90, height=50, \
                                                                    padx=10,
                                     pady=10)
        self.login_frm = tk.Frame(self.login_win, padx=5, pady=5)
        self.user_label = tk.Label(self.login_frm, text='Username')
        self.pwd_label = tk.Label(self.login_frm, text='Password')
        self.user_ent = tk.Entry(self.login_frm, width=30,
                                 textvariable=self.username)
        self.user_pwd = tk.Entry(self.login_frm, width=30, show="*",
                                 textvariable=self.password)
        self.cancel_btn = ttk.Button(self.login_frm, text='cancel',
                                     command=self.login_win.destroy)
        self.login_btn = ttk.Button(self.login_frm, text='login',
                                    command=self.catdv_login)
        self.user_pwd.bind('<Return>', self.print_from_return)

        self.login_frm.grid(row=0)
        self.user_label.grid(row=0, column=0)
        self.user_ent.grid(row=0, column=1)
        self.pwd_label.grid(row=1, column=0)
        self.user_pwd.grid(row=1, column=1)
        self.cancel_btn.grid(row=2, column=0)
        self.login_btn.grid(row=2, column=1)

    def build_variables(self):
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.fstatus = tk.StringVar()
        # user then needs to locate lto history file
        # users users button to get results

        # users sees results in list

    def print_from_return(self, event):
        print self.username.get()
        print self.password.get()

    def print_logins(self):
        print self.username.get()
        print self.password.get()

    def open_lto(self):
        name_size = None
        get_lto = True
        while get_lto:
            lto_fname = tkFileDialog.askopenfilename(title='Open LTO file')
            get_lto = False
        assert lto_fname

#           if lto_fname:
#                print('File loaded.\n')
#            if '.json' in lto_fname:
#                jdata = get_json(lto_fname)
#                current = json_to_list(jdata)
#                self.name_size = json_final(current)
#                get_lto = False
#            return self.name_size

    def catdv_login(self):
        self.usr = self.username.get()
        self.pwd = self.password.get()
        try:
            c.set_auth(username=self.usr, password=self.pwd)
            c.get_session_key()
            assert c.key
            self.fstatus.set("Connected to CatDV")
            c.get_catalog_name()
            self.login_win.destroy()
        except Exception, e:
            print e

root = tk.Tk()

root.title('lto history gui')
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

app = Application(root)

root.mainloop()