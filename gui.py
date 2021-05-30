import tkinter as tk
from thesis import *
from time import time
from tkinter import messagebox
import threading
HEIGHT = 600
WIDTH = 600

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartFrame, EnrollFrame, VerifyFrame, DeleteFrame, ConfigFrame, FormatFrame):
        # for F in (StartFrame, EnrollFrame):
            page_name = F.__name__
            frame = F(root=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartFrame(tk.Frame): #Kế thừa frame của tkinter
    def __init__(self, root, controller):
        
        tk.Frame.__init__(self, root)
        self.controller = controller
        
        # self.canvas = tk.Canvas(self, width = WIDTH, height=HEIGHT, bg='white')
        
        self.enroll_btn = tk.Button(self, text='Enrollment', width = 10, command=lambda: controller.show_frame("EnrollFrame"))
        self.delete_btn = tk.Button(self, text='Delete Data', width = 10, command=lambda: controller.show_frame("DeleteFrame"))
        self.verify_btn = tk.Button(self, text='Verification', width = 10, command=lambda: controller.show_frame("VerifyFrame"))
        self.config_btn = tk.Button(self, text='Configuration', width = 10, command=lambda: controller.show_frame("ConfigFrame"))
        self.format_btn = tk.Button(self, text='Format Data', width = 10, command=lambda: controller.show_frame("FormatFrame"))

        self.enroll_btn.pack(fill='x', padx=10)
        self.delete_btn.pack(fill='x', padx=10)
        self.verify_btn.pack(fill='x', padx=10)
        self.config_btn.pack(fill='x', padx=10)
        self.format_btn.pack(fill='x', padx=10)

class EnrollFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.record_btn = tk.Button(self, text='Start Recording', command=self.record)
        self.back_btn = tk.Button(self, text="Go to the start page",
                           command=self.back)
        
        self.record_btn.pack()
        self.back_btn.pack()
        # self.t = threading.Thread(target=self._record)
        self.t = None
        self.record_frame = tk.Frame(self)
        
        self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.record_frame, text = "Processing....")
        self.done_label = tk.Label(self.record_frame, text = "Done. Your ID is: " )


    def record(self):
        
        self.record_frame.pack()
        self.record_label.pack()
        self.back_btn.configure(state='disabled')
        
        self.t = threading.Thread(target=self._record)
        self.t.start()
        

    def back(self):
        if self.t != None and self.t.is_alive():
            self.t.join()
        self.record_btn.configure(state='active')
        self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()        
        self.controller.show_frame("StartFrame")
    def _record(self):
        self.record_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        id = gen_id()
        #os.system('arecord -r 16000 -d 5 -f S16_LE db/{}/wav/{}.wav'.format(id, id))
        os.system('arecord -D plughw:0,0 -r 16000 -d 5 -f S16_LE db/{}/wav/{}.wav'.format(id, id))
        self.process_label.pack()
        os.system('./extract.sh ' + id)
        self.back_btn.configure(state='active')
        # self.record_label.pack_forget()
        # self.process_label.pack_forget()

        self.done_label.configure(text = "Done. Your ID is: " + id) 
        self.done_label.pack()



class VerifyFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.entry = tk.Entry(self)
        self.entry.bind("<Button-1>", lambda e: self.HosoPop(root))
        self.record_btn = tk.Button(self, text='Start Recording', command=self.record)
        self.back_btn = tk.Button(self, text="Go to the start page", command=self.back)
        
        self.record_btn.pack()
        self.back_btn.pack()
        self.entry.pack()
        # self.t = threading.Thread(target=self._record)
        self.t = None
        self.record_frame = tk.Frame(self)
        self.record_frame.pack()
        self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.record_frame, text = "Processing....")
        self.done_label = tk.Label(self.record_frame, text = "Done. You are: ")
        self.buttons = ['0', '1','2','3', '4','5','6', '7','8','9', 'BACK']
        self.keyboards_button = []
        for button in self.buttons:

            command = lambda x=button: self.select(x)
            
            if button == "BACK":
                self.keyboards_button.append(tk.Button(self.record_frame, text= button,width=6, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))

            else:
                self.keyboards_button.append(tk.Button(self.record_frame, text= button,width=4, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))


    def select(self, value):
        if value == "BACK":
            self.entry.delete(len(self.entry.get())-1,tk.END)
        else:
            self.entry.insert(tk.END, value)
    
    def HosoPop(self, root):

        varRow = 1
        varColumn = 0

        for kb_btn in self.keyboards_button:

            kb_btn.pack(expand=True, side=tk.LEFT)

    def record(self):
    
        if not os.path.exists('input/wav'):
            os.makedirs('input/wav')

        self.record_label.pack()
        self.back_btn.configure(state='disabled')
        for kb_btn in self.keyboards_button:
            kb_btn.pack_forget()
        self.t = threading.Thread(target=self._record)
        # print('Go here')
        self.t.start()
    

    def back(self):
        # print(self.t.is_alive)
        if self.t != None and self.t.is_alive() :
            print('TRue')
            self.t.join()
        self.record_btn.configure(state='active')
        self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()   
        
        self.entry.delete(0, tk.END)     
        self.controller.show_frame("StartFrame")
    def _record(self):
        self.record_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        id = self.get_id()
        print(id)
        os.system('arecord -D plughw:0,0 -r 16000 -d 5 -f S16_LE input/wav/input.wav')        
        self.process_label.pack()
        os.system('./verify.sh ' + id)
        self.back_btn.configure(state='active')
        
        f = open("results")
        res = f.readlines()

        self.done_label.configure(text = "Done. You are "+res[0])
        self.done_label.pack()
    def get_id(self):
        return self.entry.get()


class DeleteFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.entry = tk.Entry(self)
        self.entry.bind("<Button-1>", lambda e: self.HosoPop(root))
        self.delete_btn = tk.Button(self, text='Start Deleting', command=self.delete)
        self.back_btn = tk.Button(self, text="Go to the start page", command=self.back)
        
        self.delete_btn.pack()
        self.back_btn.pack()
        self.entry.pack()
        # self.t = threading.Thread(target=self._record)
        self.t = None
        self.delete_frame = tk.Frame(self)
        self.delete_frame.pack()
        # self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.delete_frame, text = "Processing....")
        self.done_label = tk.Label(self.delete_frame, text = "Done.")
        self.buttons = ['0', '1','2','3', '4','5','6', '7','8','9', 'BACK']
        self.keyboards_button = []
        for button in self.buttons:

            command = lambda x=button: self.select(x)
            
            if button == "BACK":
                self.keyboards_button.append(tk.Button(self.delete_frame, text= button,width=6, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))

            else:
                self.keyboards_button.append(tk.Button(self.delete_frame, text= button,width=4, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))


    def select(self, value):
        if value == "BACK":
            self.entry.delete(len(self.entry.get())-1,tk.END)
        else:
            self.entry.insert(tk.END, value)
    
    def HosoPop(self, root):

        varRow = 1
        varColumn = 0

        for kb_btn in self.keyboards_button:

            kb_btn.pack(expand=True, side=tk.LEFT)
            
    def delete(self):
        self.delete_frame.pack()    
        for kb_btn in self.keyboards_button:
            kb_btn.pack_forget()
        self.t = threading.Thread(target=self._delete)
        self.t.start()
   

    def back(self):
        if self.t != None and self.t.is_alive():
            self.t.join()
        self.delete_btn.configure(state='active')
        # self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()   
        
        self.entry.delete(0, tk.END)     
        self.controller.show_frame("StartFrame")
    def _delete(self):
        self.delete_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        id = self.get_id()
        print(id)
        #os.system('arecord -r 16000 -d 5 -f S16_LE input/wav/input.wav')
        os.system('rm -rf ' + 'db' + '/' + id)        
        self.process_label.pack()
        self.back_btn.configure(state='active')

        # self.done_label.configure(text = "Done. You are "+res[0])
        self.done_label.pack()
    def get_id(self):
        return self.entry.get()

class ConfigFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.entry = tk.Entry(self)
        self.entry.bind("<Button-1>", lambda e: self.HosoPop(root))
        self.record_btn = tk.Button(self, text='Start Recording', command=self.record)
        self.back_btn = tk.Button(self, text="Go to the start page", command=self.back)
        
        self.record_btn.pack()
        self.back_btn.pack()
        self.entry.pack()
        # self.t = threading.Thread(target=self._record)
        self.t = None
        self.record_frame = tk.Frame(self)
        self.record_frame.pack()   
        self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.record_frame, text = "Processing....")
        self.done_label = tk.Label(self.record_frame, text = "Done.")
        self.buttons = ['0', '1','2','3', '4','5','6', '7','8','9', 'BACK']
        self.keyboards_button = []
        for button in self.buttons:

            command = lambda x=button: self.select(x)
            
            if button == "BACK":
                self.keyboards_button.append(tk.Button(self.record_frame, text= button,width=6, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))

            else:
                self.keyboards_button.append(tk.Button(self.record_frame, text= button,width=4, bg="#3c4987", fg="#ffffff",
                    activebackground = "#ffffff", activeforeground="#3c4987", 
                    # relief='raised', 
                    padx=1,
                    pady=1, 
                    # bd=1,
                    command=command))


    def select(self, value):
        if value == "BACK":
            self.entry.delete(len(self.entry.get())-1,tk.END)
        else:
            self.entry.insert(tk.END, value)
    
    def HosoPop(self, root):

        for kb_btn in self.keyboards_button:

            kb_btn.pack(expand=True, side=tk.LEFT)

    def record(self):
    
        self.record_frame.pack()
        self.record_label.pack()
        self.back_btn.configure(state='disabled')
        for kb_btn in self.keyboards_button:
            kb_btn.pack_forget()
        self.t = threading.Thread(target=self._record)
        # print('Go here')
        self.t.start()
    

    def back(self):
        # print(self.t.is_alive)
        if self.t != None and self.t.is_alive() :
            print('TRue')
            self.t.join()
        self.record_btn.configure(state='active')
        self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()   
        
        self.entry.delete(0, tk.END)     
        self.controller.show_frame("StartFrame")
    def _record(self):
        self.record_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        id = self.get_id()
        print(id)
        #os.system('arecord -r 16000 -d 5 -f S16_LE input/wav/input.wav')
        os.system('arecord -D plughw:0,0 -r 16000 -d 5 -f S16_LE db/{}/wav/{}.wav'.format(id, id))        
        self.process_label.pack()
        os.system('./extract.sh ' + id)
        self.back_btn.configure(state='active')
        
        f = open("results")
        res = f.readlines()

        # self.done_label.configure(text = "Done. You are "+res[0])
        self.done_label.pack()
    def get_id(self):
        return self.entry.get()

class FormatFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.delete_btn = tk.Button(self, text='Start Deleting All Data', command=self.delete)
        self.back_btn = tk.Button(self, text="Go to the start page", command=self.back)
        
        self.delete_btn.pack()
        self.back_btn.pack()
        # self.entry.pack()
        # self.t = threading.Thread(target=self._record)
        self.t = None
        self.delete_frame = tk.Frame(self)
        self.delete_frame.pack()

        self.process_label = tk.Label(self.delete_frame, text = "Processing....")
        self.done_label = tk.Label(self.delete_frame, text = "Done.")
        

    def delete(self):
        self.delete_frame.pack()    
        
        self.t = threading.Thread(target=self._delete_all)
        self.t.start()
   

    def back(self):
        if self.t != None and self.t.is_alive():
            self.t.join()
        self.delete_btn.configure(state='active')
        # self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()   
        
             
        self.controller.show_frame("StartFrame")
    def _delete_all(self):
        self.delete_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        self.confirm_box = tk.messagebox.askquestion ('Delete All','Are you sure you want to delete all data', icon = 'warning')
        if self.confirm_box == 'yes':
            os.system('rm -rf db')
            os.system('mkdir db')
            # Format input data (to verify)
            os.system('rm -rf input')
            os.system('mkdir input')

        else:
            # tk.messagebox.showinfo('Return','You will now return to the application screen')
            pass
    
        self.process_label.pack()
        self.back_btn.configure(state='active')

        # self.done_label.configure(text = "Done. You are "+res[0])
        self.done_label.pack()
    
def main():
    # root = tk.Tk()
    # root.geometry("600x600")
    # root.title('Speaker Verification System')
   
    # root.mainloop()
    app = App()
    app.mainloop()
if __name__ == "__main__":
    main()









