import re
import sys
import json
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox

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
                                  command=self.open_lto)

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




    def print_from_return(self, event):
        print self.username.get()
        print self.password.get()

    def print_logins(self):
        print self.username.get()
        print self.password.get()



# User first has to log onto CatDV
    def catdv_login(self):
        self.usr = self.username.get()
        self.pwd = self.password.get()
        try:
            c.set_auth(username=self.usr, password=self.pwd)
            c.get_session_key()
            if c.key:
                self.fstatus.set("Connected to CatDV")
                c.get_catalog_name()
                self.login_win.destroy()
            else:
                raise AttributeError
        except AttributeError:
            tkMessageBox.showwarning("Login error", "Incorrect login details")

# User should then locate their LTO file
    def open_lto(self):
        self.name_size = None
        get_lto = True
        try:
            while get_lto:
                lto_fname = tkFileDialog.askopenfilename(title='Open LTO file')
                if lto_fname:
                    self.fstatus.set("LTO file loaded")
                    if '.json' in lto_fname:
                        self.jdata = self.get_json(lto_fname)
                        self.current = self.json_list(self.jdata)
                        self.name_size = self.json_final(self.current)
                        get_lto = False
                    else:
                        raise TypeError
            return self.name_size
        except TypeError:
            tkMessageBox.showwarning("File error", "Unsupported file type")

    def convert_to_tb(self, byte):
        """
        Converts byte data from the LTO file to terabytes
        """
        try:
            f = float(byte)
            tb = ((((f / 1024) / 1024) / 1024) / 1024)
            return tb
        except ValueError:
            print("Value could not be converted to float. {}".format(str(byte)))

    def convert_gigab(self, byte):
        """
        Converts byte data from the LTO file to gigabytes
        """
        try:
            f = float(byte)
            gb = (((f / 1024) / 1024) / 1024)
            return gb
        except ValueError:
            print("Value could not be converted to float. {}".format(str(byte)))

    def get_json(self, submitted_file):
        """Returns JSON file as dictionary."""
        lto_data = open(submitted_file, 'r')
        jfile = json.load(lto_data)
        return jfile

    def json_list(self, json_data):
        collect = []
        for i in json_data['tapes']:
            collect.append((i['name'], i['used_size']))
        return collect

    def json_final(self, collected):
        final = []
        for item in collected:
            try:
                tb = self.convert_to_tb(item[1])  # converts GB byte data to TB
                a = re.search(r'(IV\d\d\d\d)', item[0])  # removes unicode
                final.append((str(a.group()), round(tb, 2)))
            except AttributeError:
                pass
        return final

# users uses button to view results

    def client_id(self):
        clients = {}
        try:
            for name in c.catalog_names:
                clients[name[0]] = name[1]
            return clients
        except Exception, e:
            tkMessageBox.showerror("Error", "Catalog name error: %s" % e)

root = tk.Tk()

root.title('lto history gui')
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

app = Application(root)

root.mainloop()