from Tkconstants import W, BOTH, END
from Tkinter import Tk, Label, Button, Toplevel, Text
from tkinter import ttk
from paramiko import SSHClient, AutoAddPolicy
import threading

# Server list lives in servers_to_check.py
import servers_to_check
servers_to_check = servers_to_check.servers_to_check


class MainWindow:  # The main status monitor window
    website_labels = {}
    ssh_labels = {}
    server_info_windows = {}
    ssh_connections = {}
    image = None

    def __init__(self):
        self.root = Tk()

        self.root.title('Server Status')
        self.root.protocol("WM_DELETE_WINDOW", self.on_delete)

        Label(self.root, text='Servers', bg='black', fg='white').pack()
        for name, url in servers_to_check.items():
            self.ssh_labels[name] = Label(self.root, text=name)
            self.ssh_labels[name].bind(
                    "<Button-1>",  # Mouse click
                    lambda e, name=name, url=url: self.open_server_detail_window(name, url)
            )
            self.ssh_labels[name].pack(anchor=W)

        check_all_button = Button(self.root, text='Check All', command=self.test_server_connections)
        check_all_button.pack()

    def on_delete(self):
        for name, client in self.ssh_connections.items():
            client.close()
        self.root.destroy()

    def open_server_detail_window(self, name, url):
        try:
            # If it exists just focus it
            self.server_info_windows[name].bring_to_front()
        except:
            # Check if the ssh connection exists, if not, create one
            try:
                self.ssh_connections[name]
            except:
                self.check_ssh(name, url)
            # Create the server info window now that we are sure we have a connection
            self.server_info_windows[name] = ServerInfoWindow(name, self.ssh_connections[name])

    def test_server_connections(self):
        for name, url in servers_to_check.items():
            threading.Thread(target=self.check_ssh, kwargs={'name': name, 'url': url}).start()

    def check_ssh(self, name, url):
        self.ssh_labels[name].config(fg='orange')
        self.ssh_connections[name] = SSHClient()
        self.ssh_connections[name].load_system_host_keys()
        self.ssh_connections[name].set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.ssh_connections[name].connect(url)
        except Exception as e:  # Connection failed
            print(e)
            self.ssh_labels[name].config(fg='red', text=name + ' (Connection failed)')
        else:  # Connection successful
            self.ssh_labels[name].config(fg='green')

    def run(self):
        self.root.mainloop()


class ServerInfoWindow:
    combined_commands = [
        'uptime',
        'users',
        'uname -a',
        'w',
        'who',
        'df -h',
        'cat /etc/hosts',
        'free -h',
        'iostat',
        'vmstat',
    ]

    command_list = [
        'last',
        'ps aux',
        'vmstat -stats',
        'netstat -l',
        'netstat -t',
        'netstat -u',
        'netstat -x',
        'lscpu',
        'ls ~'
    ]

    def __init__(self, name, ssh_connection=None):
        self.name = name
        self.ssh = ssh_connection
        self.window = Toplevel()
        self.window.geometry('800x600')
        self.window.title(name)
        self.window.option_add("*Font", "TkFixedFont")

        self.command_notebook = ttk.Notebook(self.window)
        self.pack_all_command_tabs()
        self.command_notebook.pack(fill=BOTH, expand=1)

    def bring_to_front(self):
        self.window.focus_force()

    def pack_all_command_tabs(self):
        # Combined commands in one tab
        combined_commands_txt = Text(self.command_notebook)
        combined_commands_txt.tag_config('highlight', foreground='blue')
        for command in self.combined_commands:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            combined_commands_txt.insert(
                    END,
                    ("===== " + command + " =====\n").encode('utf-8'),
                    ('highlight',)
            )
            combined_commands_txt.insert(END, stdout.read())
        self.command_notebook.add(combined_commands_txt, text='Info')

        # Individual commands that get their own tab
        for command in self.command_list:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            command_txt = Text(self.command_notebook)
            command_txt.insert(END, stdout.read())
            self.command_notebook.add(command_txt, text=command)


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.run()
