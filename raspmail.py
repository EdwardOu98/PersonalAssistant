from tkinter import *
import tkinter.messagebox
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions
import time
import platform


def main():
    root = Tk()
    app = LoginWin(root)

    root.mainloop()


# Login Window
class LoginWin:
    def __init__(self, master):
        self.master = master
        # Window Title
        self.master.title("Login To Gmail")
        # Window Size = Width * Height
        self.master.geometry('480x300+200+200')
        # Fixed Window Size
        self.master.maxsize(width=480, height=300)
        self.master.minsize(width=480, height=300)
        # Set background color
        self.master.config(bg='black')

        self.service = None
        self.newWin = None
        self.app = None
        self.Exit = None

        # Title Label
        self.titleLabel = Label(self.master, text="Welcome to RaspMail", font=('calibri', 30, 'bold'), bg='black',
                                fg='white')
        self.titleLabel.place(relx=0.175, rely=0.01)

        # Support Label
        self.supLabel = Label(self.master, text="Supported by Gmail API", font=('calibri', 12), bg='black', fg='white')
        self.supLabel.place(relx=0.35, rely=0.2)

        # Login Button, once clicked it will trigger the login procedure
        self.loginBTN = Button(self.master, text='Login', command=lambda: self.login(master), height=5, width=10,
                               font=('calibri', 16, 'bold'))
        self.loginBTN.place(relx=0.15, rely=0.5)

        # Exit Button, once clicked, prompt the user whether they want to exit the program
        self.exitBTN = Button(self.master, text='Exit', command=self.closewindow, height=5, width=10, font=('calibri',
                                                                                                            16, 'bold'))
        self.exitBTN.place(relx=0.6, rely=0.5)

        # Bind the x button on the window with the closewindow function
        self.master.protocol("WM_DELETE_WINDOW", self.closewindow)

    # Login Function, responsible for connecting to the gmail server
    def login(self, master):
        # if modifying these scopes, delete token.pickle
        scopes = ['https://www.googleapis.com/auth/gmail.modify']
        creds = None
        fname1 = 'token.pickle'
        fname2 = 'credentials.json'
        try:
            # The file token.pickles stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists(fname1):
                with open(fname1, 'rb') as token:
                    creds = pickle.load(token)
            # If there are no valid credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(fname2, scopes)
                    creds = flow.run_local_server(port=0)
                # Save the credential for the next run
                with open(fname1, 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('gmail', 'v1', credentials=creds)
            self.newWin = Toplevel(master)
            self.app = MainWin(self.newWin, self.service)
        except google.auth.exceptions.TransportError:
            tkinter.messagebox.showinfo("Network Error", "Connection to Gmail failed! Please check your network")
        except google.auth.exceptions.ClientCertError:
            tkinter.messagebox.showinfo("Certificate Error", "Client certificate is missing or invalid")

    # First prompt the user whether they want to exit the program, if yes terminate the entire program,
    # Otherwise return to the Login Window
    def closewindow(self):
        self.master.destroy()


# Main Window
class MainWin:
    def __init__(self, master, service):
        self.master = master
        self.master.title("RaspMail")
        self.master.geometry('500x500+200+200')
        self.Mailframe = None
        self.canvas = None
        self.scrollframe = None
        self.scrollbar = None
        self.scrollbarX = None
        self.check = None
        messages = None
        try:
            result = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = result.get('messages', [])
        except google.auth.exceptions.TransportError:
            tkinter.messagebox.showinfo("Network Error", "Connection to Gmail failed! Please check your network")

        # Frame to hold the buttons (i.e. Mark all email as read)
        self.BTNframe = Frame(self.master, width=100, bg='black')
        self.BTNframe.pack(side=LEFT, fill=Y)

        # The button connected to the function that marks all unread email as read
        self.MkBTN = Button(self.BTNframe, text="Mark as Read", command=lambda: self.mark_unread(service, messages),
                            height=5, width=11, font=('calibri', 12), wraplength=50)
        self.MkBTN.place(relx=0.025, rely=0.01)

        # This button reloads the email display frame
        self.MkBTN = Button(self.BTNframe, text="Refresh", command=lambda: self.refresh(service, messages),
                            height=5, width=11, font=('calibri', 12))
        self.MkBTN.place(relx=0.025, rely=0.25)

        self.display_email(service, messages)

    def display_email(self, service, messages):
        # This frame will display all the unread emails
        self.Mailframe = Frame(self.master, bg='black')
        self.canvas = Canvas(self.Mailframe, bg='black')
        # Create a scroll bar moving on the vertical and horizontal direction
        self.scrollbar = Scrollbar(self.Mailframe, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbarX = Scrollbar(self.Mailframe, orient=HORIZONTAL, command=self.canvas.xview)
        # Create the scrollable frame
        self.scrollframe = Frame(self.canvas, bg='black')
        # Set the scrollable region
        self.scrollframe.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Bind the scroll bar with the mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)
        self.canvas.create_window((0, 0), window=self.scrollframe, anchor=NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(xscrollcommand=self.scrollbarX.set)
        self.Mailframe.pack(side=RIGHT, fill=BOTH, expand=True)
        self.scrollbar.pack(anchor=E, side=RIGHT, fill=Y)
        self.scrollbarX.pack(anchor=S, side=BOTTOM, fill=X)
        self.canvas.pack(anchor=NW, fill=BOTH, expand=True)
        info = "You don\'t have any unread messages"

        if not messages:
            Label(self.scrollframe, text=info, bg='black', fg='white').pack()
        else:
            msg_count = 0
            for message in messages:
                msg_count = msg_count + 1
            numInfo = "You have " + str(msg_count) + " unread messages"
            numLabel = Label(self.scrollframe, text=numInfo, bg='black', fg='white')
            numLabel.pack(anchor=W)
            if msg_count != 0:
                try:
                    for message in messages:
                        sender = None
                        subject = None
                        msg = service.users().messages().get(userId='me', id=message['id']).execute()
                        data = msg['payload']['headers']
                        for values in data:
                            name = values["name"]
                            if name == "From":
                                sender = values["value"]

                        for values in data:
                            name = values["name"]
                            if name == "Subject":
                                subject = values["value"]

                        body = msg['snippet'][:80] + "..."

                        Label(self.scrollframe, text="From: "+sender, bg='black', fg='white').pack(anchor=W)
                        Label(self.scrollframe, text="Subject: "+subject, bg='black', fg='white').pack(anchor=W)
                        Label(self.scrollframe, text="Body: ", bg='black', fg='white').pack(anchor=W)
                        Label(self.scrollframe, text=body, wraplength=350, justify=LEFT, bg='black', fg='white').pack(
                            anchor=W, padx=25, pady=1)
                        Label(self.scrollframe, text="      ", bg='black').pack(anchor=W)
                        time.sleep(0.01)
                except google.auth.exceptions.TransportError:
                    tkinter.messagebox.showinfo("Network Error",
                                                "Connection to Gmail failed! Please check your network")

    # This function reloads the email display frame
    def refresh(self, service, message):
        self.scrollframe.destroy()
        self.scrollbar.destroy()
        self.canvas.destroy()
        self.Mailframe.destroy()
        result = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = result.get('messages', [])
        self.display_email(service, messages)

    # This function marked all unread messages as read
    def mark_unread(self, service, messages):
        try:
            for message in messages:
                service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ["UNREAD"]}
                                                  ).execute()
            self.scrollframe.destroy()
            self.scrollbar.destroy()
            self.canvas.destroy()
            self.Mailframe.destroy()
            result = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = result.get('messages', [])
            self.display_email(service, messages)
        except google.auth.exceptions.TransportError:
            tkinter.messagebox.showinfo("Network Error", "Connection to Gmail failed! Please check your network")

    # This function binds the mouse wheel event with the scroll bar
    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        if platform.system() == "Darwin":
            if shift:
                self.canvas.xview_scroll(-1 * event.delta, 'units')
            else:
                self.canvas.yview_scroll(-1 * event.delta, 'units')
        else:
            if shift:
                self.canvas.xview_scroll(-1 * (event.delta // 120), 'units')
            else:
                self.canvas.yview_scroll(-1 * (event.delta // 120), 'units')


# Driver function
# if __name__ == '__main__':
#     main()
