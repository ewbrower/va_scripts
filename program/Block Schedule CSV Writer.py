from tkinter import *
import urllib.request
import base64
import pymysql
import re
import datetime
import calendar

class VAFlow:

    def __init__(self,win):
        self.root = win
        #self.connect()
        self.homePage()

    def homePage(self):
        self.root.title("SPS Inventory Analysis")
        homeFrame = Frame(self.root)
        homeFrame.pack()

        homeTitle = Label(homeFrame, text="Block Schedule Editor",font=40).grid(row=0,columnspan=2,padx=5,pady=5)
        blockButton = Button(self.root,text="Begin",font=30,command=self.blockPage)
        blockButton.pack()

    def blockPage(self):
        self.root.withdraw()
        self.blockWin = Toplevel()
        self.blockWin.title("Block Schedule")
        blockFrame = Frame(self.blockWin)
        blockFrame.pack()

        blockTitle = Label(blockFrame, text="Input a weekly block schedule.", font=40).grid(row=0,columnspan=6,padx=5,pady=5)
        
        blockMondayLabel = Label(blockFrame, text="Monday", width=20, font=20).grid(row=1,column=1,padx=5,pady=5)
        blockTuesdayLabel = Label(blockFrame, text="Tuesday", width=20, font=20).grid(row=1,column=2,padx=5,pady=5)
        blockWednesdayLabel = Label(blockFrame, text="Wednesday", width=20, font=20).grid(row=1,column=3,padx=5,pady=5)
        blockThursdayLabel = Label(blockFrame, text="Thursday", width=20, font=20).grid(row=1,column=4,padx=5,pady=5)
        blockFridayLabel = Label(blockFrame, text="Friday", width=20, font=20).grid(row=1,column=5,padx=5,pady=5)
        
        blockORLabel1 = Label(blockFrame,text="OR 1",font=14).grid(row=2,column=0,padx=5,pady=5)
        blockORLabel2 = Label(blockFrame,text="OR 2",font=14).grid(row=3,column=0,padx=5,pady=5)
        blockORLabel3 = Label(blockFrame,text="OR 3",font=14).grid(row=4,column=0,padx=5,pady=5)
        blockORLabel4 = Label(blockFrame,text="OR 4",font=14).grid(row=5,column=0,padx=5,pady=5)
        blockORLabel5 = Label(blockFrame,text="OR 5",font=14).grid(row=6,column=0,padx=5,pady=5)
        blockORLabel6 = Label(blockFrame,text="OR 6",font=14).grid(row=7,column=0,padx=5,pady=5)
        blockORLabel7 = Label(blockFrame,text="OR 7",font=14).grid(row=8,column=0,padx=5,pady=5)
        blockORLabel8 = Label(blockFrame,text="OR 8",font=14).grid(row=9,column=0,padx=5,pady=5)

        self.blockVarM1 = StringVar()
        self.blockVarM2 = StringVar()
        self.blockVarM3 = StringVar()
        self.blockVarM4 = StringVar()
        self.blockVarM5 = StringVar()
        self.blockVarM6 = StringVar()
        self.blockVarM7 = StringVar()
        self.blockVarM8 = StringVar()

        self.blockVarT1 = StringVar()
        self.blockVarT2 = StringVar()
        self.blockVarT3 = StringVar()
        self.blockVarT4 = StringVar()
        self.blockVarT5 = StringVar()
        self.blockVarT6 = StringVar()
        self.blockVarT7 = StringVar()
        self.blockVarT8 = StringVar()

        self.blockVarW1 = StringVar()
        self.blockVarW2 = StringVar()
        self.blockVarW3 = StringVar()
        self.blockVarW4 = StringVar()
        self.blockVarW5 = StringVar()
        self.blockVarW6 = StringVar()
        self.blockVarW7 = StringVar()
        self.blockVarW8 = StringVar()

        self.blockVarR1 = StringVar()
        self.blockVarR2 = StringVar()
        self.blockVarR3 = StringVar()
        self.blockVarR4 = StringVar()
        self.blockVarR5 = StringVar()
        self.blockVarR6 = StringVar()
        self.blockVarR7 = StringVar()
        self.blockVarR8 = StringVar()
        
        self.blockVarF1 = StringVar()
        self.blockVarF2 = StringVar()
        self.blockVarF3 = StringVar()
        self.blockVarF4 = StringVar()
        self.blockVarF5 = StringVar()
        self.blockVarF6 = StringVar()
        self.blockVarF7 = StringVar()
        self.blockVarF8 = StringVar()
        
        blockDropdownM1 = OptionMenu(blockFrame,self.blockVarM1,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=2,column=1,padx=5,pady=5)
        blockDropdownM2 = OptionMenu(blockFrame,self.blockVarM2,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=3,column=1,padx=5,pady=5)
        blockDropdownM3 = OptionMenu(blockFrame,self.blockVarM3,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=4,column=1,padx=5,pady=5)
        blockDropdownM4 = OptionMenu(blockFrame,self.blockVarM4,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=5,column=1,padx=5,pady=5)
        blockDropdownM5 = OptionMenu(blockFrame,self.blockVarM5,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=6,column=1,padx=5,pady=5)
        blockDropdownM6 = OptionMenu(blockFrame,self.blockVarM6,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=7,column=1,padx=5,pady=5)
        blockDropdownM7 = OptionMenu(blockFrame,self.blockVarM7,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=8,column=1,padx=5,pady=5)
        blockDropdownM8 = OptionMenu(blockFrame,self.blockVarM8,'Cardiac','ENT','General','Genitourinary','Gynecology','Neurology','Ophthalmology','Oral','Ortho Hand','Orthopedics','Other','Plastic','Podiatry','Thoracic','Vascular',"-NONE-").grid(row=9,column=1,padx=5,pady=5)

        blockDropdownT1 = OptionMenu(blockFrame,self.blockVarT1,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=2,column=2,padx=5,pady=5)
        blockDropdownT2 = OptionMenu(blockFrame,self.blockVarT2,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=3,column=2,padx=5,pady=5)
        blockDropdownT3 = OptionMenu(blockFrame,self.blockVarT3,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=4,column=2,padx=5,pady=5)
        blockDropdownT4 = OptionMenu(blockFrame,self.blockVarT4,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=5,column=2,padx=5,pady=5)
        blockDropdownT5 = OptionMenu(blockFrame,self.blockVarT5,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=6,column=2,padx=5,pady=5)
        blockDropdownT6 = OptionMenu(blockFrame,self.blockVarT6,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=7,column=2,padx=5,pady=5)
        blockDropdownT7 = OptionMenu(blockFrame,self.blockVarT7,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=8,column=2,padx=5,pady=5)
        blockDropdownT8 = OptionMenu(blockFrame,self.blockVarT8,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=9,column=2,padx=5,pady=5)

        blockDropdownW1 = OptionMenu(blockFrame,self.blockVarW1,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=2,column=3,padx=5,pady=5)
        blockDropdownW2 = OptionMenu(blockFrame,self.blockVarW2,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=3,column=3,padx=5,pady=5)
        blockDropdownW3 = OptionMenu(blockFrame,self.blockVarW3,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=4,column=3,padx=5,pady=5)
        blockDropdownW4 = OptionMenu(blockFrame,self.blockVarW4,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=5,column=3,padx=5,pady=5)
        blockDropdownW5 = OptionMenu(blockFrame,self.blockVarW5,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=6,column=3,padx=5,pady=5)
        blockDropdownW6 = OptionMenu(blockFrame,self.blockVarW6,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=7,column=3,padx=5,pady=5)
        blockDropdownW7 = OptionMenu(blockFrame,self.blockVarW7,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=8,column=3,padx=5,pady=5)
        blockDropdownW8 = OptionMenu(blockFrame,self.blockVarW8,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=9,column=3,padx=5,pady=5)

        blockDropdownR1 = OptionMenu(blockFrame,self.blockVarR1,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=2,column=4,padx=5,pady=5)
        blockDropdownR2 = OptionMenu(blockFrame,self.blockVarR2,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=3,column=4,padx=5,pady=5)
        blockDropdownR3 = OptionMenu(blockFrame,self.blockVarR3,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=4,column=4,padx=5,pady=5)
        blockDropdownR4 = OptionMenu(blockFrame,self.blockVarR4,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=5,column=4,padx=5,pady=5)
        blockDropdownR5 = OptionMenu(blockFrame,self.blockVarR5,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=6,column=4,padx=5,pady=5)
        blockDropdownR6 = OptionMenu(blockFrame,self.blockVarR6,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=7,column=4,padx=5,pady=5)
        blockDropdownR7 = OptionMenu(blockFrame,self.blockVarR7,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=8,column=4,padx=5,pady=5)
        blockDropdownR8 = OptionMenu(blockFrame,self.blockVarR8,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=9,column=4,padx=5,pady=5)

        blockDropdownF1 = OptionMenu(blockFrame,self.blockVarF1,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=2,column=5,padx=5,pady=5)
        blockDropdownF2 = OptionMenu(blockFrame,self.blockVarF2,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=3,column=5,padx=5,pady=5)
        blockDropdownF3 = OptionMenu(blockFrame,self.blockVarF3,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=4,column=5,padx=5,pady=5)
        blockDropdownF4 = OptionMenu(blockFrame,self.blockVarF4,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=5,column=5,padx=5,pady=5)
        blockDropdownF5 = OptionMenu(blockFrame,self.blockVarF5,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=6,column=5,padx=5,pady=5)
        blockDropdownF6 = OptionMenu(blockFrame,self.blockVarF6,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=7,column=5,padx=5,pady=5)
        blockDropdownF7 = OptionMenu(blockFrame,self.blockVarF7,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=8,column=5,padx=5,pady=5)
        blockDropdownF8 = OptionMenu(blockFrame,self.blockVarF8,"Ophthalmology","Orthopedics","Cardiac","ENT","Genitourinary","Vascular","Ortho Hand","Gynecology","General","Plastic","Oral","Neurology","Podiatry","Thoracic","Other","-NONE-").grid(row=9,column=5,padx=5,pady=5)

        blockBackButton = Button(blockFrame,text="Back",command=self.blockToHome).grid(row=10,column=1,padx=5,pady=5)
        blockContinueButton = Button(blockFrame,text="Continue",command=self.blockDemandPage).grid(row=10,column=4,padx=5,pady=5)

        
    def blockToHome(self):
        self.blockWin.withdraw()
        self.root.deiconify()

    def blockDemandPage(self):
        
        self.blockWin.withdraw()
        self.blockDemandWin = Toplevel()
        self.blockDemandWin.title("Block Schedule Demand Calculations")
        blockDemandFrame = Frame(self.blockDemandWin)
        blockDemandFrame.pack()

        testLabel = Label(blockDemandFrame,text="CSV Generated. Thank you!").grid(row=0,column=0,padx=5,pady=5)

        self.orBlockList = []
        self.orBlockList.append([self.blockVarM1.get(),self.blockVarT1.get(),self.blockVarW1.get(),self.blockVarR1.get(),self.blockVarF1.get()])
        self.orBlockList.append([self.blockVarM2.get(),self.blockVarT2.get(),self.blockVarW2.get(),self.blockVarR2.get(),self.blockVarF2.get()])
        self.orBlockList.append([self.blockVarM3.get(),self.blockVarT3.get(),self.blockVarW3.get(),self.blockVarR3.get(),self.blockVarF3.get()])
        self.orBlockList.append([self.blockVarM4.get(),self.blockVarT4.get(),self.blockVarW4.get(),self.blockVarR4.get(),self.blockVarF4.get()])
        self.orBlockList.append([self.blockVarM5.get(),self.blockVarT5.get(),self.blockVarW5.get(),self.blockVarR5.get(),self.blockVarF5.get()])
        self.orBlockList.append([self.blockVarM6.get(),self.blockVarT6.get(),self.blockVarW6.get(),self.blockVarR6.get(),self.blockVarF6.get()])
        self.orBlockList.append([self.blockVarM7.get(),self.blockVarT7.get(),self.blockVarW7.get(),self.blockVarR7.get(),self.blockVarF7.get()])
        self.orBlockList.append([self.blockVarM8.get(),self.blockVarT8.get(),self.blockVarW8.get(),self.blockVarR8.get(),self.blockVarF8.get()])

        departmentDic = {}
        departmentDic["Ophthalmology"] = ["OPHTHALMOLOGY",8]
        departmentDic["Orthopedics"] = ["ORTHO", 3]
        departmentDic["Cardiac"] =  ["CARDIAC", 1]
        departmentDic["ENT"] = ["ENT",4]
        departmentDic["Genitourinary"] = ["GU",3]
        departmentDic["Vascular"] = ["VASC",3]
        departmentDic["Ortho Hand"] = ["HAND",1]
        departmentDic["Gynecology"] = ["GYN",4]
        departmentDic["General"] = ["GEN",3]
        departmentDic["Plastic"] = ["PLASTIC",5]
        departmentDic["Oral"] = ["ORAL",5]
        departmentDic["Neurology"] = ["NEURO",5]
        departmentDic["Podiatry"] = ["PODIATRY",3]
        departmentDic["Thoracic"] = ["THORACIC",3]
        departmentDic["Other"] = ["GEN",3]
        departmentDic["-NONE-"] = ["GEN",3]
        departmentDic[""] = ["GEN",3]

        self.orScheduleList = [["M","M","T","T","W","W","R","R","F","F"]]

        for room in self.orBlockList:
            subList = []
            for department in room:
                subList.append(departmentDic[department][0])
                subList.append(departmentDic[department][1])
            self.orScheduleList.append(subList)

        print(self.orScheduleList)


win = Tk()
app = VAFlow(win)
win.mainloop()
