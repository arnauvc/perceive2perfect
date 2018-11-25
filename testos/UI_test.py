from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import time

archery =  [(176, 194), (157, 250), (129, 264), (55, 264), (111, 250), (185, 264), (259, 264), (315, 250), (139, 403), (129, 500), (120, 612), (185, 389), (213, 486), (241, 570), (157, 333)]
vrksasana =  [(273, 150), (273, 244), (221, 263), (182, 150), (260, 75), (326, 263), (365, 150), (300, 75), (234, 470), (247, 639), (286, 808), (313, 470), (456, 545), (300, 545), (273, 376)]
squats =  [(313, 104), (250, 229), (187, 271), (360, 292), (438, 271), (250, 271), (516, 271), (563, 271), (46, 563), (266, 563), (172, 813), (46, 542), (375, 563), (281, 772), (156, 417)]

class Application(Frame):
    
    def start(self):
        print "Please remain some moments still"

###
        cap = cv2.VideoCapture(1)
        factor = 2.5
        fgbg = cv2.createBackgroundSubtractorMOG2()

        for x in range(0,120):
            ret, frame = cap.read()
            if ret == 0:
                break
            fgmask = fgbg.apply(frame)
            cv2.imshow('frame',fgmask)
            self.image_v = Image.Fromarray(frame)
            self.image_v = self.image_v.resize((500, 500), Image.ANTIALIAS)
            self.photo_v = ImageTk.PhotoImage(self.image_v)
            
            self.label_v.imgtk = self.photo_v  # anchor imgtk so it does not be deleted by garbage-collector
            self.label_v.config(image=imgtk)  # show the image
            
            self.label_v.image = self.photo_v
            #self.label_v.pack({"side": "right"})

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break


        print("Stand still for a little bit")
        threshold = 0
        for x in range(0,30):
            ret, frame = cap.read()
            if ret == 0:
                break
            fgmask = fgbg.apply(frame)
            threshold = threshold + fgmask.sum()
            cv2.imshow('frame',fgmask)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        threshold = threshold / 30
        print('El threshold es ')
        print(threshold)

        first = True
        while(1):
            ret, frame = cap.read()
            if ret == 0:
                break
            fgmask = fgbg.apply(frame)
            currentsum = fgmask.sum()
            #print(currentsum)
            if(currentsum < factor*threshold):
                show = "ESTA QUIET"
            else:
                show = "ESTA EN MOVIMENT"
            cv2.putText(frame, show, (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv2.LINE_AA)
            cv2.imshow('frame',frame)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

###
        
    def select(self, v):
        if(self.var.get() == "Archer"):
            self.source = "../OpenPose/images/archery.jpg"
            points_1 = archery
        elif(self.var.get() == "Vrkasana"):
            self.source = "../OpenPose/images/vrkasana.jpg"
            points_1 = vrksasana
        elif(self.var.get() == "Squats"):
            self.source = "../OpenPose/images/squats.jpg"
            points_1 = squats
        self.image2 = Image.open(self.source)
        self.image = self.image2.resize((350, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label.configure(image=self.photo)
        self.label.image = self.photo


    def createWidgets(self):
        frametop = Frame(root)
        frametop.pack(side=TOP, fill=BOTH, expand=1)

        self.var = StringVar(self)
        self.var.set("Select your pose") # initial information
        self.option = OptionMenu(frametop, self.var, "Archer", "Vrkasana", "Squats",  command = self.select)
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
        
        self.source_v = "../OpenPose/images/white.jpg"

        self.image_v = Image.open(self.source_v)
        self.image_v = self.image_v.resize((500, 500), Image.ANTIALIAS)
        self.photo_v = ImageTk.PhotoImage(self.image_v)

        self.label_v = Label(image=self.photo_v)
        self.label_v.image = self.photo_v
        self.label_v.pack({"side": "right"})
        
        self.source = "../OpenPose/images/white.jpg"

        self.image = Image.open(self.source)
        self.image = self.image.resize((350, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = Label(image=self.photo)
        self.label.image = self.photo
        self.label.pack({"side": "right"})


        


    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        self.vid = cv2.VideoCapture(video_source)
                # Create a canvas that can fit the above video source size
        self.canvas = Tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        #Frame.__init__(self, master)
        #self.pack()
        self.createWidgets()
        

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
