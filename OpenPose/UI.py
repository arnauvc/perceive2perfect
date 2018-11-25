from Tkinter import *
from PIL import Image, ImageTk

class Application(Frame):
    
    def start(self):
        print "Please remain some moments still"

    def createWidgets(self):
        frametop = Frame(root)
        frametop.pack(side=TOP, fill=BOTH, expand=1)
    
        self.image = Image.open("/home/iris/Documents/LausHack/P2P/OpenPose/images/archery.jpg")
        self.image = self.image.resize((350, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = Label(image=self.photo)
        self.label.image = self.photo
        self.label.pack({"side": "left"})

        self.var = StringVar(self)
        self.var.set("Choose your pose") # initial information
        self.option = OptionMenu(frametop, self.var, "Archer", "Vrkasana", "Squats")
        self.option.pack({"side": "left"})

        self.QUIT = Button(frametop)
        self.QUIT["text"] = "FINISH"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "right"})

        self.START = Button(frametop)
        self.START["text"] = "START"
        self.START["command"] = self.start
        
        self.START.pack({"side": "right"})
        


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
