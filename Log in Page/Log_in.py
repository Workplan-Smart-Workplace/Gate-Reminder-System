
from tkinter import *
import firebase_admin
# from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import os
import json
from dotenv import load_dotenv
import requests
import pprint
from PIL import Image, ImageTk
from io import BytesIO


load_dotenv('Log_In.env')
FIREBASE_API_KEY = os.environ['FIREBASE_API_KEY']
credential = credentials.Certificate("workplanKey.json")
default_app = firebase_admin.initialize_app(credential) #{'databaseURL': "https://pi-test-ffbef-default-rtdb.firebaseio.com/"})
db = firestore.client()
# ref = db.reference("/")
doc_ref = db.collection(u'users')
def first_page():
    global home_screen
    home_screen = Tk()
    home_screen.geometry("640x400")
    home_screen.title("Log in Page")
    background_image = Image.open("paul-earle-wVjd0eWNqI8-unsplash.jpg")
    background_image = ImageTk.PhotoImage(background_image)
    canvas = Label(home_screen, image=background_image)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    Label(text = "Select Log in, or register if no account exists", bg = "gainsboro", width="300", height="2", font=("Ariel", 15)).pack()
    Button(text="Login", height="2", width="30", command=LogIn).pack() 
    Button(text="Register", height="2", width="30", command=registerAccount).pack(pady=40)
    Button(text="Weather", height="2", width="30", command=Weather).pack(pady=20)
    Button(text="Sign Out", height="2", width="30", command=signOut).pack(pady=20)
    home_screen.mainloop()

def registerAccount():
    global registration
    registration = Toplevel(home_screen)
    registration.title("Account Creation")
    registration.geometry("300x400")

    global email 
    email = StringVar()
    global password 
    password = StringVar()
    global fname 
    fname = StringVar()
    global lname 
    lname = StringVar()
    global button1
    button1 = BooleanVar()
    Label(registration, text="Enter work email and password.", bg="gainsboro").pack()
    Label(registration, text="").pack()
    Label(registration, text="First Name: ").pack()
    Entry(registration, textvariable=fname).pack()
    Label(registration, text="Last Name: ").pack()
    Entry(registration, textvariable=lname).pack()
    Label(registration, text="Email: ").pack()
    Entry(registration, textvariable=email).pack()
    Label(registration, text="Password: ").pack()
    Entry(registration, textvariable=password, show="*").pack()
    Label(registration, text="").pack()
    Radiobutton(registration, text="Employee", value="false", variable=button1).pack()
    Radiobutton(registration, text="Manager", value="True", variable=button1).pack()
    Button(registration, text="Create Account", width="15", height="1", bg="gainsboro", command=sendRegisterToFirebase).pack()

def sendRegisterToFirebase():
    # ref.child('Users')
    email_reg = email.get()
    pass_reg = password.get()
    auth.create_user(email = email_reg, password = pass_reg)
    fname_reg = fname.get()
    lname_reg = lname.get()
    button1_reg = button1.get() 
    uID = auth.get_user_by_email(email_reg)
    print("User ID ", uID.uid)
    ref_to_register = doc_ref.document(uID.uid)
   # ref_to_register.push().set({"UserData":{"Email":email_reg, "Password":pass_reg}})
    ref_to_register.set({
        u'email':email_reg,
        u'fName': fname_reg,
        u'lName': lname_reg,
        u'manager': button1_reg,
        u'isLoggedIn': False,
        u'userID': uID.uid
    })
    Label(registration, text="Account has been registered.", fg="green", font=("Ariel", 11)).pack(side="bottom")
    

def LogIn():
    global Log_in
    Log_in = Toplevel(home_screen)
    Log_in.title("Log In Page")
    Log_in.geometry("300x400")

    global email_log 
    email_log = StringVar()
    global password_log 
    password_log = StringVar()
    global email_line
    global pass_line

    Label(Log_in, text="Enter work email and password.", bg="gainsboro").pack()
    Label(Log_in, text="").pack()
    Label(Log_in, text="Email: ").pack()
    email_line = Entry(Log_in, textvariable=email_log).pack()
    Label(Log_in, text="Password: ").pack()
    pass_line = Entry(Log_in, textvariable=password_log, show="*").pack()
    Label(Log_in, text="").pack()
    Button(Log_in, text="Log In", width="15", height="1", bg="grey", command=logCheck).pack()

def logCheck():
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    user = auth.get_user_by_email(email_log.get())
    ref_log = db.collection(u'users').document(user.uid)
    return_secure_token: bool=True
    payload = json.dumps({
        "email": email_log.get(),
        "password": password_log.get(),
        "returnSecureToken": return_secure_token
    })
    global token
    r = requests.post(rest_api_url, params={"key": FIREBASE_API_KEY}, data=payload)
    token = r.json()
    pprint.pprint(token)
    
    if ('error' in token and token['error']['message'] == "INVALID_PASSWORD"):
            passwordNotLogged()
    elif(email_log.get() != user.email):
        emailNotLogged()
    else:
        ref_log.update({u'isLoggedIn':True})
        logWorked()
    '''ref_email = db.reference("/Users/" + user + "/UserData/Email")
    ref_pass = db.reference("/Users/" + user + "/UserData/Password")
    print(ref_email.get())
    email_in_firebase = ref_email.get()
    print(ref_pass.get())
    pass_in_firebase = ref_pass.get()
    if email_log.get() == email_in_firebase:
        if password_log.get() == pass_in_firebase:
            logWorked()
    else:
        emailNotLogged() '''

def logWorked():
    global accepted
    accepted = Toplevel(Log_in)
    accepted.title("You have logged in")
    accepted.geometry("150x100")
    Label(accepted, text="Login Success").pack()
    Button(accepted,text="Accept", command=break_log).pack()

def break_log():
    accepted.destroy()
    Log_in.destroy()

def emailNotLogged():
    print("Email Not Found.")
    global declined
    declined = Toplevel(Log_in)
    declined.title("Wrong Email")
    declined.geometry("150x100")

    Label(declined, text="Login Failed Due To Email").pack()
    Button(declined,text="Try Again", command=LogIn)

def passwordNotLogged():
    print("Password Not Found.")
    global declined
    declined = Toplevel(Log_in)
    declined.title("Wrong Password")
    declined.geometry("150x100")
    Label(declined, text="Login Failed Due To Password").pack()
    Button(declined,text="Try Again", command=LogIn)
    
def signOut():
    global email_sign
    global entered_email
    entered_email = StringVar()
    email_sign = Toplevel(home_screen)
    email_sign.title("Sign Out Page")
    email_sign.geometry("300x200")
    Label(email_sign, text="Email: ").pack()
    email_line = Entry(email_sign, textvariable=entered_email).pack()
    Button(email_sign,text="Confirm", command=signOutConfirm).pack(pady=20)

def signOutConfirm():
    user = auth.get_user_by_email(entered_email.get())
    ref_log = db.collection(u'users').document(user.uid)
    ref_log.update({u'isLoggedIn':False})
    Label(email_sign, text="Account has been signed out.", fg="green", font=("Ariel", 11)).pack(side="bottom")
def Weather():
    os.system('python weather_app.py')
if __name__ == "__main__":
    first_page()
    
