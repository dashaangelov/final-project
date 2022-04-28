import tkinter as tk
from tkinter import messagebox, Checkbutton
from CBACObligationWPermissions import * 
import datetime

eventmanager = EventManager()

eventmanager.addObligationPrincipal(obligation1)
eventmanager.addObligationPrincipal(obligation2)

class App(tk.Tk):
    def __init__(self):
        self.root = tk.Tk.__init__(self)
        self._frame = None
        self.geometry("1000x1000")
        self.title("Access Control With Obligations Simulation")
        self.switch_frame(StartPage)
        self.obligations = ["Message fater", "message moter"]
    
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        if self.needAlertBox(frame_class):
            tk.messagebox.askyesno("askyesno", self.alertUserChangeFrame(frame_class))
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
    def alertUserChangeFrame(self, frame_class):
        if frame_class == PageOne:
            return "You will now play the role of a teacher"
        elif frame_class == PageTwo:
            return "You will now play the role of a teacher"
        else:
            return "Welcome to the game!"

    def needAlertBox(self, frame_class):
        if frame_class == StartPage:
            return False
        return True

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page", font=("Arial", 30)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Teacher Principal",font=("Arial", 20), command=lambda: master.switch_frame(PageOne)).pack(pady=10)
        tk.Button(self, text="Headmaster Principal",font=("Arial", 20), command=lambda: master.switch_frame(PageTwo)).pack(pady=10)

class PageOne(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(
            self, 
            text="You are now a Teacher. \n Try click on \nthe various actions \nyou can perform", 
            font=("Arial", 30),fg='yellow',bg='black' ).pack(side="top",fill='x')
        tk.Button(
            self, text="Read Student Data",font=("Arial", 20), 
            command=lambda: self.handleButonClick(READ, studentdata)
            ).pack(side="top", fill="x", pady=10)
        tk.Button(
            self, text="Write Student Data",font=("Arial", 20), 
            command=lambda: self.handleButonClick(WRITE, studentdata)
            ).pack(side="top", fill="x", pady=10)
        tk.Button(
            self, text="Write Parent Data",font=("Arial", 20), 
            command=lambda: self.handleButonClick(WRITE, parentdata)
            ).pack(side="top", fill="x", pady=10)
        tk.Button(
            self, text="Return to start page",font=("Arial", 20), 
            command=lambda: master.switch_frame(StartPage)
            ).pack(side="bottom", fill="x", pady=10)
        
        self.obligation_log = tk.Text(self, width=60, height=15)
        self.obligation_log.pack(side="bottom", fill="x", pady=10)
        tk.Label(self, text="Obligations You Need to Fufill",font=("Arial", 20),fg='yellow',bg='black' ).pack(side="bottom", fill="x", pady=10)

        self.event_log = tk.Text(self, width=60, height=15)
        self.event_log.pack(side="bottom", fill="x", pady=10)
        tk.Label(self, text="Event History",font=("Arial", 20),fg='yellow',bg='black' ).pack(side="bottom", fill="x", pady=10)
    
    def update(self):
        self.clock.config(text="new text")

    
    def handleButonClick(self,event, resource):
        if teacher.isAuthorised(event, resource):
            #tk.messagebox.askyesno("askyesno", event.obligation.ge1)
            eventmanager.addEvent(principal=teacher, action=event, resource=resource)
            self.event_log.delete('1.0', tk.END)
            for item in eventmanager.eventLog:
                self.event_log.insert(tk.END, "[LOG]" + str(item) + "\n")
            self.obligation_log.delete('1.0', tk.END)
            for key in eventmanager.unfulfilledObligations.keys():
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eventmanager.unfulfilledObligations[key]["timeout"]))
                self.obligation_log.insert(tk.END, 
                str(eventmanager.unfulfilledObligations[key]["principal"]) + " needs to perform " 
                + str(eventmanager.unfulfilledObligations[key]["action"].actionIdentifier) 
                + " on " + str(eventmanager.unfulfilledObligations[key]["resource"]) + " by " 
                + str(date))
            print(eventmanager.unfulfilledObligations)
        else:
            tk.messagebox.showerror("askyesno", "UNAUTHORISED")
    
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="You are now a Teacher. \n Try click on \nthe various actions \nyou can perform", font=("Arial", 30),fg='yellow',bg='black' ).pack(side="top",fill='x')
        tk.Button(self, text="Read Student Data",font=("Arial", 20), command=lambda: self.handleButonClick(READ, studentdata)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Write Student Data",font=("Arial", 20), command=lambda: self.handleButonClick(WRITE, studentdata)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Write Parent Data",font=("Arial", 20), command=lambda: self.handleButonClick(WRITE, parentdata)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",font=("Arial", 20), command=lambda: master.switch_frame(StartPage)).pack(side="bottom", fill="x", pady=10)
        
        self.obligation_log = tk.Text(self, width=60, height=15)
        self.obligation_log.pack(side="bottom", fill="x", pady=10)
        tk.Label(self, text="Obligations You Need to Fufill",font=("Arial", 20),fg='yellow',bg='black' ).pack(side="bottom", fill="x", pady=10)

        self.event_log = tk.Text(self, width=60, height=15)
        self.event_log.pack(side="bottom", fill="x", pady=10)
        tk.Label(self, text="Event History",font=("Arial", 20),fg='yellow',bg='black' ).pack(side="bottom", fill="x", pady=10)
    
    def update(self):
        self.clock.config(text="new text")

    
    def handleButonClick(self,event, resource):
        if teacher.isAuthorised(event, resource):
            #tk.messagebox.askyesno("askyesno", event.obligation.ge1)
            eventmanager.addEvent(principal=teacher, action=event, resource=resource)
            self.event_log.delete('1.0', tk.END)
            for item in eventmanager.eventLog:
                self.event_log.insert(tk.END, "[LOG]" + str(item) + "\n")
            self.obligation_log.delete('1.0', tk.END)
            for key in eventmanager.unfulfilledObligations.keys():
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(eventmanager.unfulfilledObligations[key]["timeout"]))
                self.obligation_log.insert(tk.END, 
                str(eventmanager.unfulfilledObligations[key]["principal"]) + " needs to perform " 
                + str(eventmanager.unfulfilledObligations[key]["action"].actionIdentifier) 
                + " on " + str(eventmanager.unfulfilledObligations[key]["resource"]) + " by " 
                + str(date))
            print(eventmanager.unfulfilledObligations)
        else:
            tk.messagebox.showerror("askyesno", "UNAUTHORISED")

clockRoot = tk.Tk()
clockRoot.title("Clock Interface")
clockRoot.geometry("600x400")

def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    clockLabel.config(text=hour + ":" + minute + ":" + second)
    unfulfilled_obligations.delete('1.0', tk.END)
    for item in eventmanager.uncompletedObligations:
        unfulfilled_obligations.insert(tk.END, item)
    clockLabel.after(1000, clock)

clockLabel = tk.Label(clockRoot, text="Testing", font=("Helvetica", 48), fg="green",bg="black")
clockLabel.pack(pady=10)
unfulfilled_obligations = tk.Text(clockRoot, width=60, height=15)
unfulfilled_obligations.pack(side="bottom", fill="x", pady=10)

clock()