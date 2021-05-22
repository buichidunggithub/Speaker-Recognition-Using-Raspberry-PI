import tkinter as tk
from thesis import *

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
        record_btn = tk.Button(self, text='Start Recording')
        back_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartFrame"))
        
        record_btn.pack()
        back_button.pack()

class VerifyFrame(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        # record_btn = tk.Button(self, text='Start Recording')
        back_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartFrame"))
        
        # record_btn.pack()
        back_button.pack()

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









