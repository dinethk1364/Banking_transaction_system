import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class BankAccounts:
    def __init__(self,accNo,name,balance):
        self.accNo = accNo
        self.name = name
        self.balance = balance

#####sample accounts#####
accounts = {
    "20050001": BankAccounts("20050001","D. D. K. De Silva",120000),
    "20050002": BankAccounts("20050002","Punsara",150000),
    "20050003": BankAccounts("20050003","Viraj",135000),
    "20050004": BankAccounts("20050004","kavindu",450000)

}

def login(evnt=None):
    global username
    username = userNameVar.get()
    password = passwordVar.get()

    ####add system users####
    systemUsers = {
        "admin":"1234",
        "dinethk":"12456",
        "guest":"0000"
    }

    if username in systemUsers and systemUsers[username] == password:
        messagebox.showinfo("Login Success",f"Welcome {username}")
        entryUser.delete(0, tk.END)
        entryPass.delete(0, tk.END)
        loginWindow.withdraw()
        openNewWindow(username)
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")
        entryUser.focus()
        # trxWin.focus_force()
        entryUser.delete(0, tk.END)
        entryPass.delete(0, tk.END)

def searchAccount(event=None):
    accNo = accNoEntry.get()
    global userAccName,userAccBal,userAccNo
    if accNo in accounts:
        account = accounts[accNo]
        userAccNo=accNo
        userAccName = account.name
        userAccBal = account.balance
    
        # print(f"Account Name : {userAccName}")
        # print(f"Balance : Rs. {userAccBal}")
        main.withdraw()
        openTransactionWindow()
        accNoEntry.delete(0, tk.END)
        
        # main.destroy()
        

    else:
        messagebox.showerror("Error", "Account not found")
        accNoEntry.delete(0, tk.END)


def openNewWindow(user):
    global accNoEntry,main

####main window####
    main = tk.Tk()
    width,height = 700,350
    displayWidth = main.winfo_screenwidth()
    displayHeight = main.winfo_screenheight()
    left = int(displayWidth/2-width/2)
    top = int(displayHeight/2-height/2)
    main.geometry(f'{width}x{height}+{left}+{top}')
    main.title("Banking Transaction System")
    main.resizable(False,False)
    main.iconbitmap('icon/icon.ico')
    main.configure(bg="#FFF9E8")

####main window widgets####


    label1 = tk.Label(main,text="Banking Transaction System",font="arial 20 bold",bg='#FFF9E8')
    label1.pack(pady=(50,20))
    label2 = tk.Label(main,text=f"Logged in as: {user}",font="Arial",bg='#FFF9E8')
    label2.pack()

    label3 = tk.Label(main,text='Enter account no',font="arial 15",bg='#FFF9E8')
    label3.pack(pady=(30,10))

    accNoEntry = ttk.Entry(main, width=40)
    accNoEntry.pack(pady=20,ipadx=5,ipady=2)

    logoutBtn = ttk.Button(main,text='LOGOUT',command=logout)
    logoutBtn.pack(ipadx=10,ipady=5,pady=10,padx=40,anchor='e')

    main.focus_force()
    accNoEntry.focus()

####keybind####
    main.bind("<Return>",searchAccount)
    
    
    main.mainloop()

def exitfunc():
    trxWin.destroy()
    main.deiconify()
    accNoEntry.focus()


def logout():
    # global loginWindow
    main.destroy()  
    loginWindow.deiconify()
    loginWindow.focus_force()
    entryUser.focus()


def withFunc(amount,balLabel):
    global entryAmount, userAccBal
    try:
        amount = int(amount)

        if amount <= 0:
            messagebox.showerror("Error", "Enter valid amount")
            trxWin.focus_force()
            
            return

        if amount > userAccBal:
            messagebox.showerror("Error", "Insufficient balance")
            trxWin.focus_force()

        else:
            userAccBal -= amount

            accounts[userAccNo].balance = userAccBal
            balLabel.config(text=f"LKR {userAccBal}/=")

            # main.destroy()

            if userAccBal<1000:
                result = messagebox.askyesno("Warning","After this transaction, your balance will be below the minimum balance, do you need to continue")
                trxWin.focus_force()

                # print(result)
                if result==True:

                    messagebox.showinfo("Success", f"Withdrawn {amount}")

                    # print(userAccBal)
                    messagebox.showinfo("Balance",f"Available Balance is LKR {userAccBal}")
                else:
                    userAccBal+=amount
                    # print(userAccBal)
                    accounts[userAccNo].balance = userAccBal
                    balLabel.config(text=f"LKR {userAccBal}/=")

            else:
                messagebox.showinfo("Success", f"Withdrawn {amount}")

                    # print(userAccBal)
                messagebox.showinfo("Balance",f"Available Balance is LKR {userAccBal}")

            trxWin.focus_force()
            withAmnt.delete(0, tk.END)
        
        

    except:
        messagebox.showerror("Error", "Invalid input")
        trxWin.focus_force()

    # print(entryAmount)

    

def depFunc(amount,balLabel):
    global entryAmount,userAccBal
    try:
        amount = int(amount)

        if amount <= 0:
            messagebox.showerror("Error", "Enter valid amount")
            trxWin.focus_force()

            return

        userAccBal += amount
        accounts[userAccNo].balance = userAccBal
        balLabel.config(text=f"LKR {userAccBal}/=")
        # main.destroy()

        messagebox.showinfo("Success", f"Deposited {amount}")

        # print(userAccBal)
        messagebox.showinfo("Balance",f"Available Balance is LKR {userAccBal}")
        trxWin.focus_force()
        depAmnt.delete(0,tk.END)

    except:
        messagebox.showerror("Error", "Invalid input")
        trxWin.focus_force()


def openTransactionWindow():
    global trxWin,withAmnt,depAmnt
    trxWin=tk.Toplevel(main)

####transaction window####
    width,height = 1000,700
    displayWidth = trxWin.winfo_screenwidth()
    displayHeight = trxWin.winfo_screenheight()
    left = int(displayWidth/2-width/2)
    top = int(displayHeight/2-height/2)
    trxWin.geometry(f'{width}x{height}+{left}+{top}')
    trxWin.title("Transactions")
    trxWin.resizable(False,False)
    trxWin.iconbitmap('icon/icon.ico')

    trxWin.configure(bg="#FFF9E8")

    
    label1 = tk.Label(trxWin,text=f"Account Holder's Name : {userAccName}" ,font='arial 15',bg="#FFF9E8")
    label1.pack(anchor="w",padx=20,pady=(20))
    

####transactioin tabs####
    style = ttk.Style()
    style.map("TNotebook.Tab",
    background=[("selected", "#E9E9E9")],
    )
    style.configure("TNotebook.Tab", background="#E9E9E9", borderwidth=0)

    trxTabs = ttk.Notebook(trxWin)
    frame1 = tk.Frame(trxTabs, width = 950, height = 500, relief=tk.GROOVE,bg="#E9E9E9")
    frame1.pack_propagate(False)
    frame1.pack()

    frame2 = tk.Frame(trxTabs, width = 950, height = 500, relief=tk.GROOVE,bg='#E9E9E9')
    frame2.pack_propagate(False)
    frame2.pack()

    frame3 = tk.Frame(trxTabs, width = 950, height = 500, relief=tk.GROOVE,bg='#E9E9E9')
    frame3.pack_propagate(False)
    frame3.pack()

    
####withdraw tab####
    trxType = tk.Label(frame1,text='Cash Withdrawal',font='arial 20 bold',bg='#E9E9E9')
    trxType.pack(anchor='w',pady=20,padx=20)
    label3 = tk.Label(frame1,text='Enter Amount',font='arial 12 bold',bg='#E9E9E9')
    label3.pack(pady=(70,20))
    withAmnt = ttk.Entry(frame1,width=50,font='arial 12')
    withAmnt.pack(pady=20,ipady=8,ipadx=10)
    withBtn = ttk.Button(frame1,text='Withdraw',command=lambda:withFunc(withAmnt.get(),amount))
    withBtn.pack(ipady=10,ipadx=10,pady=10)
    # trxWin.bind("<Return>",lambda:withFunc(withAmnt.get(),amount))

####dep tab####
    trxType = tk.Label(frame2,text='Cash Deposit',font='arial 20 bold',bg='#E9E9E9')
    trxType.pack(anchor='w',pady=20,padx=20)
    label4 = tk.Label(frame2,text='Enter Amount',font='arial 12 bold',bg='#E9E9E9')
    label4.pack(pady=(70,20))
    depAmnt = ttk.Entry(frame2,width=50,font='arial 12')
    depAmnt.pack(pady=20,ipady=8,ipadx=10)
    depBtn = ttk.Button(frame2,text='Deposit',command=lambda:depFunc(depAmnt.get(),amount))
    depBtn.pack(ipady=10,ipadx=10,pady=10)
    # frame2.bind("<Return>",depFunc)

####bal check tab####
    availableBal = tk.Label(frame3,text=f"Available Balance" ,font='arial 20 bold',bg='#E9E9E9')
    availableBal.pack(padx=20,pady=(120,20))

    amount = tk.Label(frame3,text=f"LKR {userAccBal}/=",font=("Arial",20,"bold"),fg="#fa4b2c",bg='#E9E9E9')
    amount.pack()


    trxTabs.add(frame1,text='Withdrawals')
    trxTabs.add(frame2,text='Deposits')
    trxTabs.add(frame3,text='Check Balance')

    trxTabs.pack()
    # trxWin.mainloop()

    trxWin.focus_force()
    withAmnt.focus()
    exitBtn = ttk.Button(trxWin,text="EXIT",command=exitfunc)
    exitBtn.pack(pady=30,padx=(0,30),anchor='e',ipadx=5,ipady=5)

    
def startProgram():   
    
    global userNameVar,passwordVar,loginWindow,entryPass,entryUser

#####login window####
    loginWindow = tk.Tk()

    loginWindowWidth = 600
    loginWindowHeight = 250
    displayWidth=loginWindow.winfo_screenwidth()
    displayHeight=loginWindow.winfo_screenheight()
    left = int(displayWidth/2-loginWindowWidth/2)
    top = int(displayHeight/2-loginWindowHeight/2)

    loginWindow.title("Login")
    loginWindow.iconbitmap('icon/icon.ico')
    loginWindow.configure(bg="#FFF9E8")

    loginWindow.geometry(f'{loginWindowWidth}x{loginWindowHeight}+{left}+{top}')

#####login Details####
    userNameVar = tk.StringVar()
    passwordVar = tk.StringVar()

#####Login widgets####


    lebel1 = tk.Label(loginWindow,text='TELLER LOGIN',font='arial 20 bold',bg='#FFF9E8')
    lebel1.pack(pady=20)

    loginFrame = tk.Frame(loginWindow, width=500, height=200,bg='#FFF9E8')
    loginFrame.pack()

    labelUser = tk.Label(loginFrame,text='User Name',bg='#FFF9E8')
    labelUser.pack()

    entryUser = ttk.Entry(loginFrame,textvariable=userNameVar,width=50)
    entryUser.pack(ipadx=5,ipady=2)

    labelPass = tk.Label(loginFrame,text='Password',bg='#FFF9E8')
    labelPass.pack()

    entryPass = ttk.Entry(loginFrame,textvariable=passwordVar,width=50,show='*')
    entryPass.pack(ipadx=5,ipady=2)

    loginBtn = ttk.Button(loginFrame,text='Login',command=login)
    loginBtn.pack(pady=15)

    #key bind
    loginWindow.bind("<Return>",login)
    entryUser.focus()
    
    loginWindow.mainloop()

startProgram()