import tkinter as tk
from thesis import *
from time import time
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
        self.t = threading.Thread(target=self._record)
        self.record_frame = tk.Frame(self)
        
        self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.record_frame, text = "Processing....")
        self.done_label = tk.Label(self.record_frame, text = "Done. Your ID is: " )
        
    def record(self):
        
        self.record_frame.pack()
        self.record_label.pack()
        self.back_btn.configure(state='disabled')
        
        
        self.t.start()
        

    def back(self):
        if self.t.is_alive():
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
        os.system('arecord -r 16000 -d 5 -f S16_LE db/{}/wav/{}.wav'.format(id, id))
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
        self.record_btn = tk.Button(self, text='Start Recording', command=self.record)
        self.back_btn = tk.Button(self, text="Go to the start page",
                           command=self.back)
        
        self.record_btn.pack()
        self.back_btn.pack()
        self.entry.pack()
        self.t = None
        self.record_frame = tk.Frame(self)
        
        self.record_label = tk.Label(self.record_frame, text = "Recording....")
        self.process_label = tk.Label(self.record_frame, text = "Processing....")
        self.done_label = tk.Label(self.record_frame, text = "Done. You are: ")
    def record(self):
        
        self.record_frame.pack()
        self.record_label.pack()
        self.back_btn.configure(state='disabled')
        
        self.t = threading.Thread(target=self._record)
        self.t.start()
        

    def back(self):
        if self.t.is_alive():
            self.t.join()
        self.record_btn.configure(state='active')
        self.record_label.pack_forget()
        self.process_label.pack_forget()
        self.done_label.pack_forget()        
        self.controller.show_frame("StartFrame")
    def _record(self):
        self.record_btn.configure(state='disable')
        self.back_btn.configure(state='disabled')
        id = self.get_id()
        print(id)
        os.system('arecord -r 16000 -d 5 -f S16_LE input/wav/input.wav')
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
        # record_btn = tk.Button(self, text='Start Recording')
        back_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartFrame"))
        
        # record_btn.pack()
        back_button.pack()

class ConfigFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        # record_btn = tk.Button(self, text='Start Recording')
        back_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartFrame"))
        
        # record_btn.pack()
        back_button.pack()

class FormatFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        # record_btn = tk.Button(self, text='Start Recording')
        back_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartFrame"))
        
        # record_btn.pack()
        back_button.pack()


def main():
    # root = tk.Tk()
    # root.geometry("600x600")
    # root.title('Speaker Verification System')
   
    # root.mainloop()
    app = App()
    app.mainloop()
if __name__ == "__main__":
    main()









