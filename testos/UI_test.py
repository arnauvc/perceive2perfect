import Tkinter
import PIL.Image, PIL.ImageTk
import numpy as np
import cv2
import time

archery =  [(176, 194), (157, 250), (129, 264), (55, 264), (111, 250), (185, 264), (259, 264), (315, 250), (139, 403), (129, 500), (120, 612), (185, 389), (213, 486), (241, 570), (157, 333)]
vrksasana =  [(273, 150), (273, 244), (221, 263), (182, 150), (260, 75), (326, 263), (365, 150), (300, 75), (234, 470), (247, 639), (286, 808), (313, 470), (456, 545), (300, 545), (273, 376)]
squats =  [(313, 104), (250, 229), (187, 271), (360, 292), (438, 271), (250, 271), (516, 271), (563, 271), (46, 563), (266, 563), (172, 813), (46, 542), (375, 563), (281, 772), (156, 417)]

class Application:
    
    def start(self):
        print "Starting configuration"

###
        cap = self.vid
        factor = 2.5
        fgbg = cv2.createBackgroundSubtractorMOG2()

        for x in range(0,120):
            ret, frame, f = cap.get_frame()
            if ret == 0:
                break
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = Tkinter.NW)
            self.canvas.update() 
            fgmask = fgbg.apply(f)
            cv2.imshow('frame',fgmask)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break


        print("Stand still for a little bit")
        threshold = 0
        for x in range(0,30):
            ret, frame, f = cap.get_frame()
            if ret == 0:
                break
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = Tkinter.NW)
            self.canvas.update() 
            fgmask = fgbg.apply(f)
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
            ret, frame, f = cap.get_frame()
            if ret == 0:
                break
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = Tkinter.NW)
            self.canvas.update() 
            fgmask = fgbg.apply(f)
            currentsum = fgmask.sum()
            #print(currentsum)
            if(currentsum < factor*threshold):
                show = "ESTA QUIET"
            else:
                show = "ESTA EN MOVIMENT"
            cv2.putText(f, show, (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv2.LINE_AA)
            cv2.imshow('frame',f)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

###
        
    def select(self, v):
        if(self.var.get() == "Archer"):
            self.source = "../OpenPose/images/archery.jpg"
            self.points_1 = archery
        elif(self.var.get() == "Vrkasana"):
            self.source = "../OpenPose/images/vrkasana.jpg"
            self.points_1 = vrksasana
        elif(self.var.get() == "Squats"):
            self.source = "../OpenPose/images/squats.jpg"
            self.points_1 = squats
        self.image2 = PIL.Image.open(self.source)
        self.image = self.image2.resize((320, self.vid.getH() - 30), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(self.image)

        self.label.configure(image=self.photo)
        self.label.image = self.photo


    def createWidgets(self, window):
        frametop = Tkinter.Frame(window)
        frametop.pack({"side":"top", "fill":"both", "expand":1})

        self.var = Tkinter.StringVar()
        self.var.set("Select your pose") # initial information
        self.option = Tkinter.OptionMenu(frametop, self.var, "Archer", "Vrkasana", "Squats",  command = self.select)
        self.option.pack({"side": "left"})

#        self.QUIT = Tkinter.Button(window)
#        self.QUIT["text"] = "FINISH"
#        self.QUIT["fg"]   = "red"
#        self.QUIT["command"] =  self.quit

#        self.QUIT.pack({"side": "right"})

        self.START = Tkinter.Button(frametop)
        self.START["text"] = "START"
        self.START["command"] = self.start
        
        self.START.pack({"side": "right"})
              
        self.source = "../OpenPose/images/white.jpg"

        self.image = PIL.Image.open(self.source)
        self.image = self.image.resize((320, self.vid.getH() - 30), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(self.image)

        self.label = Tkinter.Label(image=self.photo)
        self.label.image = self.photo
        self.label.pack({"side": "right"})

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        self.vid = MyVideoCapture(video_source)
                # Create a canvas that can fit the above video source size
        self.canvas = Tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack({"side": "right"})
        #Frame.__init__(self, master)
        #self.pack()
        self.createWidgets(window)

                # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()


    def snapshot(self):
        # Get a frame from the video source
        ret, frame, _ = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame, _ = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = Tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)   

    def getH(self):
        return int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), frame)
            else:
                return (ret, None, None)
        else:
            return (ret, None, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
Application(Tkinter.Tk(), "Tkinter and OpenCV")
