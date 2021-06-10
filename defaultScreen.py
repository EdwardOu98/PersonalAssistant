from tkinter import *
import tkinter.messagebox
import time
import requests
import json
import datetime
import raspmail
import fileExplorer
import MediaPlayer
import os.path
import sys
import threading
# import MedicModule
# import crypt

# Weather api key:
# https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude={part}&appid={API key}


def main():
    root = Tk()
    app = LoginRegister(root)

    root.mainloop()


class LoginRegister():
    def __init__(self, master):
        self.master = master
        self.master.title("Mirrorcle Login/Registration System")
        # Window Size = Width * Height
        self.master.geometry('480x300+200+200')
        # Fixed Window Size
        self.master.maxsize(width=480, height=300)
        self.master.minsize(width=480, height=300)
        # Set background color
        self.master.config(bg='black')
        # Title Label
        self.titleLabel = Label(self.master, text="Please Enter Your Information", font=('calibri', 24, 'bold'),
                                bg='black', fg='white')
        self.titleLabel.place(relx=0.05, rely=0.01)
        self.usrn_label = Label(self.master, text="Username: ", font=('calibri', 16, 'bold'), bg='black', fg='white')
        self.usrn_label.place(relx=0.05, rely=0.2)
        self.usrn_entry = Entry(self.master)
        self.usrn_entry.place(relx=0.32, rely=0.2, width=300)
        self.pw_label = Label(self.master, text="Password: ", font=('calibri', 16, 'bold'), bg='black', fg='white')
        self.pw_label.place(relx=0.05, rely=0.4)
        self.pw_entry = Entry(self.master, show='*')
        self.pw_entry.place(relx=0.32, rely=0.4, width=300)
        self.clearBTN = Button(self.master, text='Clear Entry', command=self.cleartext, height=1, width=10,
                               font=('calibri', 16, 'bold'))
        self.clearBTN.place(relx=0.5, rely=0.6)
        self.loginBTN = Button(self.master, text='Login',
                               command=lambda: self.login(self.usrn_entry.get(), self.pw_entry.get()),
                               height=1, width=10, font=('calibri', 16, 'bold'))
        self.loginBTN.place(relx=0.2, rely=0.6)
        self.RegBTN = Button(self.master, text='Register',
                               command=lambda: self.register(self.usrn_entry.get(), self.pw_entry.get()),
                               height=1, width=10, font=('calibri', 16, 'bold'))
        self.RegBTN.place(relx=0.2, rely=0.8)
        self.exitBTN = Button(self.master, text='Exit', command=self.closewindow, height=1, width=10, font=('calibri',
                                                                                                            16, 'bold'))
        self.exitBTN.place(relx=0.5, rely=0.8)

    def login(self, username, psw):
        fname = 'userinfo.json'
        try:
            file = open(fname, 'r')
            userinfo = json.load(file)
            existFlag = False
            for key in userinfo:
                if key == username:
                    existFlag = True
                    break
            if not existFlag:
                choice = tkinter.messagebox.askyesno("Invalid User", "Username doesn't exist. Do you want to register?")
                if choice > 0:
                    self.register(username, psw)
                else:
                    self.usrn_entry.delete(0, END)
                    self.pw_entry.delete(0, END)
            elif userinfo[username] != psw:
                tkinter.messagebox.showinfo("Invalid Password", "Password is incorrect")
                self.pw_entry.delete(0, END)
            else:
                self.usrn_entry.delete(0, END)
                self.pw_entry.delete(0, END)
                self.newWin = Toplevel(self.master)
                self.app = DefaultWin(self.newWin, username)
        except FileNotFoundError:
            tkinter.messagebox.showinfo("Missing File", "userinfo.json is missing")

    def register(self, username, psw):
        fname = 'userinfo.json'
        existFlag = False
        userinfo = {}
        if os.path.exists(fname):
            file = open(fname, 'r')
            userinfo = json.load(file)
            for key in userinfo:
                if key == username:
                    existFlag = True
                    tkinter.messagebox.showinfo("User existed", "Username already exist. Please try again")
                    break
        if not existFlag:
            file = open(fname, 'w')
            userinfo[username] = psw
            json.dump(userinfo, file)
            choice = tkinter.messagebox.askyesno("Info",
                                                 "Registration completed. Do you want to login with the new account?")
            if choice > 0:
                self.usrn_entry.delete(0, END)
                self.pw_entry.delete(0, END)
                self.newWin = Toplevel(self.master)
                self.app = DefaultWin(self.newWin, username)
            else:
                self.usrn_entry.delete(0, END)
                self.pw_entry.delete(0, END)

    def cleartext(self):
        self.usrn_entry.delete(0, END)
        self.pw_entry.delete(0, END)

    def closewindow(self):
        self.Exit = tkinter.messagebox.askyesno("Confirmation", "Are you sure to exit?")
        if self.Exit > 0:
            self.master.destroy()
            sys.exit()
        else:
            pass


class ClockModule(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.time = ''
        self.clockLabel = Label(self, font=('calibri', 48), fg='white', bg='black')
        self.clockLabel.pack(side=TOP, anchor=E)
        self.day = ''
        self.dayLabel = Label(self, font=('calibri', 18), fg='white', bg='black')
        self.dayLabel.pack(side=TOP, anchor=E)
        self.date = ''
        self.dateLabel = Label(self, font=('calibri', 18), fg='white', bg='black')
        self.dateLabel.pack(side=TOP, anchor=E)
        self.update()

    def update(self):
        time_format = "%r"  # change to %R for 24 hour notation
        date_format = "%D"  # change to %b %d %Y if preferred
        new_time = time.strftime(time_format)
        new_day = time.strftime('%A')
        new_date = time.strftime(date_format)

        if new_time != self.time:
            self.time = new_time
            self.clockLabel.config(text=self.time)
        if new_day != self.day:
            self.day = new_day
            self.dateLabel.config(text=self.day)
        if new_date != self.date:
            self.date = new_date
            self.dayLabel.config(text=self.date)
        # Update itself every 200 ms
        self.after(200, self.update)


class ForecastingModule(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.weather_description = ''
        self.location = ''
        self.temperatureFrame = Frame(self, bg='black')
        self.temperatureFrame.pack(side=TOP, anchor=W)
        self.temperatureLabel = Label(self.temperatureFrame, font=('calibri', 48), fg='white', bg='black')
        self.temperatureLabel.pack(side=LEFT, anchor=N)
        self.descriptionLabel = Label(self, font=('calibri', 28), fg='white', bg='black')
        self.descriptionLabel.pack(side=TOP, anchor=W)
        self.locationLabel = Label(self, font=('calibri', 12), fg='white', bg='black')
        self.locationLabel.pack(side=TOP, anchor=W)
        self.getweather()

    def getweather(self):
        # Get geographic coordinates for weather
        request_url = "http://ip-api.com/json/"
        geo_req = requests.get(request_url)
        geo_json = json.loads(geo_req.text)
        lat = geo_json['lat']
        lon = geo_json['lon']
        city = geo_json['city']
        state = geo_json['regionName']
        nation = geo_json['country']
        new_location = city + ", " + state + ", " + nation
        # get local weather
        # unit can be changed to metric if desired
        weather_key = "Replace with your own key"
        weather_url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+\
                      str(lon)+"&exclude=minutely,hourly&units=imperial&appid="+weather_key
        weather_req = requests.get(weather_url)
        weather_json = json.loads(weather_req.text)

        degree_sign = u'\N{DEGREE SIGN}'
        new_temperature = str(int(weather_json['main']['temp']))+degree_sign+"F"  # change to C for metric unit
        new_weather_description = weather_json['weather'][0]['description']
        if new_location != self.location:
            self.location = new_location
            self.locationLabel.config(text=self.location)
        if new_temperature != self.temperature:
            self.temperature = new_temperature
            self.temperatureLabel.config(text=self.temperature)
        if new_weather_description != self.weather_description:
            self.weather_description = new_weather_description
            self.descriptionLabel.config(text=self.weather_description)

        # Update weather info hourly
        self.after(3600000, self.getweather)


class DefaultWin:
    def __init__(self, master, username):
        email_icon = PhotoImage(file="icon/email_icon.png")
        medic_icon = PhotoImage(file="icon/medic_icon.png")
        file_icon = PhotoImage(file="icon/file_icon.png")
        player_icon = PhotoImage(file="icon/player_icon.png")
        self.master = master
        self.master.title("Mirrorcle")
        self.clockframe = Frame(self.master, bg='black')
        self.clockframe.pack(side=TOP, fill=BOTH, expand=True)
        self.appframe = Frame(self.master, bg='black', height=500)
        self.appframe.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.is_full_screen = False
        self.master.bind("<Return>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.toggle_fullscreen)
        # Greeting tag
        self.greeting = None
        self.t1 = threading.Thread(target=self.greeting_tag(username))
        self.t1.start()
        # self.greeting_tag(username)
        # Heart Rate Display
        # self.HeartRate = None
        # self.t2 = threading.Thread(target=self.heartrate_display(username))
        # self.t2.start()
        # Date and time
        self.clock = None
        self.t3 = threading.Thread(target=self.clock_module)
        self.t3.start()
        # self.clock_module()
        # Weather forecast
        self.forecast = None
        self.t4 = threading.Thread(target=self.forecast_module)
        self.t4.start()
        # self.forecast_module()
        # Button to connect the email module
        self.email_BTN_frame = Frame(self.appframe, width=200, height=200, bg='white')
        self.email_BTN_frame.pack(side=LEFT, anchor=S, padx=25, pady=100)
        self.email_BTN = Button(self.email_BTN_frame, width=100, height=150, bg='black', fg='white')
        # self.email_BTN.config(command=lambda: threading.Thread(target=self.email_module).start())
        self.email_BTN.config(command=lambda: self.email_module())
        self.email_BTN.config(image=email_icon, compound=TOP, text="Email", font=('calibri', 18))
        self.email_BTN.image = email_icon
        self.email_BTN.pack(side=LEFT, fill=BOTH, expand=True)
        # Button to connect the medical module
        self.medic_BTN_frame = Frame(self.appframe, width=200, height=200, bg='black')
        self.medic_BTN_frame.pack(side=LEFT, anchor=S, padx=25, pady=100)
        self.medic_BTN = Button(self.medic_BTN_frame, text='Medical', bg='black', fg='white', width=100, height=150)
        self.medic_BTN.config(font=('calibri', 18), image=medic_icon, compound=TOP)
        # self.medic_BTN.config(command=lambda: threading.Thread(target=self.medic_module).start())
        self.medic_BTN.config(command=lambda: self.medic_module())
        self.medic_BTN.image = medic_icon
        self.medic_BTN.pack(side=LEFT, fill=BOTH, expand=True)
        # Button to connect the file explorer
        self.file_BTN_frame = Frame(self.appframe, width=200, height=200, bg='black')
        self.file_BTN_frame.pack(side=RIGHT, anchor=S, padx=25, pady=100)
        self.file_BTN = Button(self.file_BTN_frame, text='File Explorer', bg='black', fg='white', width=100, height=150)
        self.file_BTN.config(font=('calibri', 18), image=file_icon, compound=TOP)
        # self.file_BTN.config(command=lambda: threading.Thread(target=self.file_explorer_module).start())
        self.file_BTN.config(command=lambda: self.file_explorer_module())
        self.file_BTN.image = file_icon
        self.file_BTN.pack(side=LEFT, fill=BOTH, expand=True)
        # Button to connect the VLC Player
        self.player_BTN_frame = Frame(self.appframe, width=200, height=200, bg='black')
        self.player_BTN_frame.pack(side=RIGHT, anchor=S, padx=25, pady=100)
        self.player_BTN = Button(self.player_BTN_frame, text='VLC Player', bg='black', fg='white', width=100, height=150)
        self.player_BTN.config(font=('calibri', 18), image=player_icon, compound=TOP)
        self.player_BTN.config(command=lambda: threading.Thread(target=self.Media_player_module).start())
        # self.player_BTN.config(command=lambda: self.Media_player_module())
        self.player_BTN.image = player_icon
        self.player_BTN.pack(side=LEFT, fill=BOTH, expand=True)

    def greeting_tag(self, username):
        self.greeting = Label(self.clockframe, font=('calibri', 48), fg='white', bg='black')
        self.greeting.pack(side=BOTTOM)
        self.update_label(username)
        self.greeting.after(200, self.update_label(username))

    def clock_module(self):
        self.clock = ClockModule(self.clockframe)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=100)

    def forecast_module(self):
        self.forecast = ForecastingModule(self.clockframe)
        self.forecast.pack(side=LEFT, anchor=N, padx=100, pady=100)

    def heartrate_display(self, username):
        print('This is the heartrate display')
        # self.HeartRate = MedicModule.MedicModule(self.clockframe, username)
        # self.HeartRate.pack(side=BOTTOM, anchor=W, padx=100)

    def email_module(self):
        raspmail.main()

    def medic_module(self):
        print('This is the medic module')

    def Media_player_module(self):
        MediaPlayer.main()

    def file_explorer_module(self):
        fileExplorer.main()

    def toggle_fullscreen(self, event):
        self.is_full_screen = not self.is_full_screen
        self.master.attributes("-fullscreen", self.is_full_screen)

    def update_label(self, username):
        if (datetime.datetime.now().hour >= 6) and (datetime.datetime.now().hour < 12):
            greeting_text = "Good morning, "+username+"!"
            self.greeting.config(text=greeting_text)
        elif (datetime.datetime.now().hour >= 12) and (datetime.datetime.now().hour < 17):
            greeting_text = "Good afternoon, "+username+"!"
            self.greeting.config(text=greeting_text)
        elif (datetime.datetime.now().hour >= 17) and (datetime.datetime.now().hour < 20):
            greeting_text = "Good evening, "+username+"!"
            self.greeting.config(text=greeting_text)
        elif (datetime.datetime.now().hour >= 20) or (datetime.datetime.now().hour < 6):
            greeting_text = "Good night, "+username+"!"
            self.greeting.config(text=greeting_text)


if __name__ == '__main__':
    main()
