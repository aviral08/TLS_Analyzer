#!/usr/bin/env python
# coding: utf-8

# In[19]:


from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import subprocess
import socket
from contextlib import closing
import os
master=Tk()
width=600
height=500
screenwidth = master.winfo_screenwidth()
screenheight = master.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
master.geometry(alignstr)
master.resizable(width=True, height=True)
master.title("SSL Tool")
# pb = ttk.Progressbar(
#     master,
#     orient='horizontal',
#     mode='indeterminate',
#     length=280
# )


file_name=[]
def upload():
    file_name.clear()
    file_path = askopenfilename(parent=master, filetypes=[('Text Files', '*txt')])
    file_name.append(file_path)
    btn1.config(state="normal")
    btn5.config(state="normal")
    messagebox.showinfo("File Upload","Successfully uploaded file")

def scan_command():
#         pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
#         pb.start
        index=file_name[0].rfind('/')
        result= subprocess.run(f'nmap -iL {file_name[0]}  -p 443 -n -Pn --script ssl-enum-ciphers -oN {file_name[0][0:index]}/nmap_test_result.txt', stdout=subprocess.PIPE, shell=True)
        with open(f'{file_name[0][0:index]}/nmap_test_result.txt','r') as file:
            lines=file.readlines()
    
        sslv3=[]
        TLSv10=[]
        TLSv11=[]
    
        for i in range(len(lines)):
            if 'SSLv3:' in lines[i]:
                for k in range(i-10,len(lines)):
                    if 'Nmap scan report for' in lines[k]:
                        res=lines[k].split()
                        sslv3.append(res[4])
                        break
            if 'TLSv1.0:' in lines[i]:
                for k in range(i-10,len(lines)):
                    if 'Nmap scan report for' in lines[k]:
                        res=lines[k].split()
                        TLSv10.append(res[4])
                        break
            if 'TLSv1.1:' in lines[i]:
                for k in range(i-10,len(lines)):
                    if 'Nmap scan report for' in lines[k]:
                        res=lines[k].split()
                        TLSv11.append(res[4])
                        break
        with open(f'{file_name[0][0:index]}/sslv3.txt','w') as sslv3_result:
            for i in sslv3:
                sslv3_result.write(str(i))
                sslv3_result.write('\n')
        with open(f'{file_name[0][0:index]}/TLS10.txt','w') as TLSv10_result:
            for i in TLSv10:
                TLSv10_result.write(str(i))
                TLSv10_result.write('\n')
        with open(f'{file_name[0][0:index]}/TLS11.txt','w') as TLSv11_result:
            for i in TLSv11:
                TLSv11_result.write(str(i))
                TLSv11_result.write('\n')
        messagebox.showinfo("SSL Scan","Scan is complete")
#         pb.stop
        btn2.config(state="normal")
        btn3.config(state="normal")
        btn4.config(state="normal")


Output = Text(master, height = screenheight,
			width = screenwidth)

def scan_command2():
        index=file_name[0].rfind('/')
        Output.config(state='normal')
        Output.delete("1.0","end")
        with open(f'{file_name[0][0:index]}/sslv3.txt','r') as file:
            lines=file.readlines()
        for i in range(len(lines)):
            Output.insert('end',lines[i])
#         Output.place(relx=0.5, rely=0.0)
        Output.config(state='disabled')
def scan_command3():
        index=file_name[0].rfind('/')
        Output.config(state='normal')
        Output.delete("1.0","end")
        with open(f'{file_name[0][0:index]}/TLS10.txt','r') as file:
            lines=file.readlines()
        for i in range(len(lines)):
            Output.insert('end',lines[i])
#         Output.place(relx=0.5, rely=0.0)
        Output.config(state='disabled')

def scan_command4():
        index=file_name[0].rfind('/')
        Output.config(state='normal')
        Output.delete("1.0","end")
        with open(f'{file_name[0][0:index]}/TLS11.txt','r') as file:
            lines=file.readlines()
        for i in range(len(lines)):
            Output.insert('end',lines[i])
#         Output.place(relx=0.5, rely=0.0)
        Output.config(state='disabled')


def port_scan():
    Output.config(state='normal')
    Output.delete("1.0","end")
    index=file_name[0].rfind('/')
    f=open(f'{file_name[0]}','r')
    with open(f'{file_name[0][0:index]}/port_status.txt','w') as port_status:
        def check_socket(host, port):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex((host, port)) == 0:
                    port_status.write(host + " " + "open\n")
                else:
                    port_status.write(host + " " + "close\n")



        domain_list = []


        for x in f.readlines():
            domain_list.append(x.rstrip())

        for y in domain_list:
            try:
                check_socket(y,443)
            except:
                port_status.write(y+" NA\n")
    with open(f'{file_name[0][0:index]}/port_status.txt','r') as file:
        lines=file.readlines()
        for i in range(len(lines)):
            Output.insert('end',lines[i])
    Output.config(state='disabled')

btn=Button(master, text="Upload Text file", command=upload)
btn1=Button(master,state="disabled",text="Scan for ciphers", command= scan_command)
btn2=Button(master,state="disabled",text="SSLv3 Sites", command= scan_command2)
btn3=Button(master,state="disabled",text="TLSv1.0 Sites", command= scan_command3)
btn4=Button(master,state="disabled",text="TLSv1.1 Sites", command= scan_command4)
btn5=Button(master,state="disabled", text= "port 443 Status", command=port_scan)
Output.place(relx=0.5, rely=0.0)
btn.place(relx=0.1, rely=0.05, height=51, width=138)
btn1.place(relx=0.1, rely=0.20, height=51, width=138)
btn2.place(relx=0.1, rely=0.35, height=51, width=138)
btn3.place(relx=0.1, rely=0.50, height=51, width=138)
btn4.place(relx=0.1, rely=0.65, height=51, width=138)
btn5.place(relx=0.1, rely=0.80, height=51, width=138)
master.mainloop()


# In[ ]:




