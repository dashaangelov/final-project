from GUI import *

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    print("[LOG " + str(starttime) + "] User has initated application start")
    print("[LOG " + str(datetime.datetime.now()) + "] Loading assets")
    app = App()
    endtime = datetime.datetime.now()
    print("[LOG " + str(endtime) + "] Application has finished loading. It took " + str(endtime-starttime) + " seconds")
    app.mainloop()