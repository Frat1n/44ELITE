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

def main():
    root = tk.Tk()
    app = PenetrationTestingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
