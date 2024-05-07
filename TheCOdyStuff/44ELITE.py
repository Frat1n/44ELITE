import socket
import subprocess
import os
import threading
import tkinter as tk

class PenetrationTestingApp:
    def __init__(self, master):
        self.master = master
        master.title("44ELITE - Penetration Testing Tool")

        self.target_label = tk.Label(master, text="Target IP:")
        self.target_label.grid(row=0, column=0)
        self.target_entry = tk.Entry(master)
        self.target_entry.grid(row=0, column=1)

        self.port_label = tk.Label(master, text="Port Range (start-end):")
        self.port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(master)
        self.port_entry.grid(row=1, column=1)

        self.scan_button = tk.Button(master, text="Scan Ports", command=self.scan_ports)
        self.scan_button.grid(row=2, columnspan=2)

        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.grid(row=3, columnspan=2)

        self.brute_force_button = tk.Button(master, text="Brute Force Login", command=self.brute_force_login)
        self.brute_force_button.grid(row=4, columnspan=2)

        self.command_label = tk.Label(master, text="Command to Execute:")
        self.command_label.grid(row=5, column=0)
        self.command_entry = tk.Entry(master)
        self.command_entry.grid(row=5, column=1)

        self.execute_button = tk.Button(master, text="Execute Command", command=self.execute_command)
        self.execute_button.grid(row=6, columnspan=2)

    def scan_ports(self):
        target = self.target_entry.get()
        port_range = self.port_entry.get().split("-")
        start_port = int(port_range[0])
        end_port = int(port_range[1])

        open_ports = self._scan_ports(target, start_port, end_port)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Open ports: " + str(open_ports))

    def _scan_ports(self, target, start_port, end_port):
        open_ports = []
        for port in range(start_port, end_port+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    def brute_force_login(self):
        target = self.target_entry.get()
        port = int(input("Enter the port to brute force: "))
        usernames = input("Enter usernames (separated by comma): ").split(',')
        passwords = input("Enter passwords (separated by comma): ").split(',')
        self.output_text.delete(1.0, tk.END)
        if self._brute_force_login(target, port, usernames, passwords):
            self.output_text.insert(tk.END, "Brute force successful!")
        else:
            self.output_text.insert(tk.END, "Brute force failed.")

    def _brute_force_login(self, target, port, usernames, passwords):
        for username in usernames:
            for password in passwords:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target, port))
                    banner = self._get_banner(sock)
                    sock.sendall("{}:{}\n".format(username, password).encode())
                    response = sock.recv(1024).decode().strip()
                    if "Login successful" in response:
                        return True
                    sock.close()
                except:
                    pass
        return False

    def _get_banner(self, sock):
        try:
            return sock.recv(1024).decode().strip()
        except Exception as e:
            return str(e)

    def execute_command(self):
        target = self.target_entry.get()
        port = int(input("Enter the port to execute command on: "))
        command = self.command_entry.get()
        self.output_text.delete(1.0, tk.END)
        self._execute_command(target, port, command)

    def _execute_command(self, target, port, command):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.send(command.encode())
            response = sock.recv(4096).decode()
            self.output_text.insert(tk.END, response)
            sock.close()
        except Exception as e:
            self.output_text.insert(tk.END, "Error: " + str(e))

def main():
    root = tk.Tk()
    app = PenetrationTestingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
