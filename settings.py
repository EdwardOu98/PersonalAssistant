import json
import locale
import time
import threading
from tkinter import *
from tkinter import ttk
from contextlib import contextmanager

# {"Theme": "Dark", "Language": "en_US"}

global locale_lock
locale_lock = threading.Lock()
lang = ''


@contextmanager
def makelocale(ui_loc):
    # print(lang)
    with locale_lock:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, ui_loc)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


def main():
    # print(lang)
    root = Tk()
    app = SettingsWindow(root)

    root.mainloop()


class SettingsWindow:
    def __init__(self, master):
        self.fname = 'config.json'
        self.lang_list = ["English", "Chinese (Simplified)", "Japanese"]
        current_settings = {}
        self.master = master
        self.theme_opt = StringVar(self.master)
        self.lang_opt = StringVar(self.master)
        self.master.title("Settings")
        self.master.geometry('480x600+0+0')
        # self.master.maxsize(width=480, height=300)
        # self.master.minsize(width=480, height=300)
        self.clockframe = Frame(self.master)
        self.ThemeLabel = Label(self.master, text='Theme')
        self.ThemeOpt1 = Radiobutton(self.master, text='Dark', variable=self.theme_opt, value='Dark')
        self.ThemeOpt2 = Radiobutton(self.master, text='Color', variable=self.theme_opt, value='Color')
        self.OKButton = Button(self.master, text='OK', command=self.ok)
        self.CancelButton = Button(self.master, text='Cancel', command=self.cancel)
        self.lang_menu = OptionMenu(self.master, self.lang_opt, *self.lang_list)
        file = open(self.fname, 'r')
        current_settings = json.load(file)
        file.close()
        self.theme_opt.set(current_settings['Theme'])
        self.lang_opt.set(current_settings['Language'])
        if current_settings['Theme'] == 'Dark':
            self.master.config(bg='black')
            self.ThemeLabel.config(bg='black', fg='white')
            self.ThemeOpt1.config(bg='black', fg='white')
            self.ThemeOpt2.config(bg='black', fg='white')
            self.OKButton.config(bg='black', fg='white')
            self.CancelButton.config(bg='black', fg='white')
            self.lang_menu.config(bg='black', fg='white')
            self.clockframe.config(bg='black')
        else:
            self.master.config(bg='white')
            self.ThemeLabel.config(bg='white', fg='black')
            self.ThemeOpt1.config(bg='white', fg='black')
            self.ThemeOpt2.config(bg='white', fg='black')
            self.OKButton.config(bg='white', fg='black')
            self.CancelButton.config(bg='white', fg='black')
            self.lang_menu.config(bg='white', fg='black')
            self.clockframe.config(bg='white')
        self.ThemeLabel.pack(anchor=W)
        self.ThemeOpt1.pack(anchor=W)
        self.ThemeOpt2.pack(anchor=W)
        self.OKButton.pack(anchor=S)
        self.CancelButton.pack(anchor=S)
        self.lang_menu.pack(anchor=E)
        self.clockframe.pack(side=TOP, fill=BOTH, expand=True)
        self.clock = ClockModule(self.clockframe, current_settings['Theme'])
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)

    def ok(self):
        fname = 'config.json'
        file = open(fname, 'r')
        settings = json.load(file)
        file = open(fname, 'w')
        lang_opt = self.lang_opt.get()
        global lang
        if lang_opt == 'English':
            lang = 'en_US'
        elif lang_opt == 'Chinese (Simplified)':
            lang = 'zh_CN'
        elif lang_opt == 'Japanese':
            lang = 'ja_JP'
        settings['Language'] = lang_opt
        if self.theme_opt.get() == 'Dark':
            self.master.config(bg='black')
            self.ThemeLabel.config(bg='black', fg='white')
            self.ThemeOpt1.config(bg='black', fg='white')
            self.ThemeOpt2.config(bg='black', fg='white')
            self.OKButton.config(bg='black', fg='white')
            self.CancelButton.config(bg='black', fg='white')
            self.lang_menu.config(bg='black', fg='white')
            settings['Theme'] = 'Dark'
            json.dump(settings, file)
            self.clock.change_theme(self.theme_opt.get())
        elif self.theme_opt.get() == 'Color':
            self.master.config(bg='white')
            self.ThemeLabel.config(bg='white', fg='black')
            self.ThemeOpt1.config(bg='white', fg='black')
            self.ThemeOpt2.config(bg='white', fg='black')
            self.OKButton.config(bg='white', fg='black')
            self.CancelButton.config(bg='white', fg='black')
            self.lang_menu.config(bg='white', fg='black')
            settings['Theme'] = 'Color'
            json.dump(settings, file)
            self.clock.change_theme(self.theme_opt.get())

    def cancel(self):
        self.master.destroy()


class ClockModule(Frame):
    def __init__(self, parent, theme):
        Frame.__init__(self, parent)
        self.theme = theme
        self.time = ''
        self.clockLabel = Label(self, font=('calibri', 12))
        self.day = ''
        self.dayLabel = Label(self, font=('calibri', 12))
        self.date = ''
        self.dateLabel = Label(self, font=('calibri', 12))
        if theme == 'Dark':
            self.config(bg='black')
            self.clockLabel.config(fg='white', bg='black')
            self.dayLabel.config(fg='white', bg='black')
            self.dateLabel.config(fg='white', bg='black')
        else:
            self.config(bg='white')
            self.clockLabel.config(fg='black', bg='white')
            self.dayLabel.config(fg='black', bg='white')
            self.dateLabel.config(fg='black', bg='white')
        self.clockLabel.pack(side=TOP, anchor=E)
        self.dayLabel.pack(side=TOP, anchor=E)
        self.dateLabel.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with makelocale(lang):
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
            self.clockLabel.after(200, self.tick)

    def change_theme(self, theme):
        if theme == 'Dark':
            self.config(bg='black')
            # self.theme = 'Dark'
            self.clockLabel.config(fg='white', bg='black')
            self.dayLabel.config(fg='white', bg='black')
            self.dateLabel.config(fg='white', bg='black')
        else:
            self.config(bg='white')
            # self.theme = 'Color'
            self.clockLabel.config(fg='black', bg='white')
            self.dayLabel.config(fg='black', bg='white')
            self.dateLabel.config(fg='black', bg='white')


if __name__ == '__main__':
    file = open('config.json', 'r')
    current_settings = json.load(file)
    file.close()
    if current_settings['Language'] == 'English':
        lang = 'en_US'
    elif current_settings['Language'] == 'Chinese (Simplified)':
        lang = 'zh_CN'
    elif current_settings['Language'] == 'Japanese':
        lang = 'ja_JP'
    main()
