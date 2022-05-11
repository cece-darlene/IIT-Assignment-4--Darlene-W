##Author: Darlene Widjaja
##Date created: 11/03/2022
##Date last changed: 24/04/2022
##The purpose of this program is to produce GUI menu for the user to be able to add in new bank details 
    ## AND to be able to calculate the balance in their account after one year
        ##The calculation will be made using the amount deposited, interest rate of the bank and the compound of the bank
            ##The bankDetails.txt is a shared document between these two programs

from pickle import READONLY_BUFFER
from tkinter import *

window = Tk()
window.title('Calculator')
window.minsize(height=800, width= 1200) ##Determining the size of the window

window['background']='#A3B7E1' ##Changing the background colour

from ast import literal_eval
from os.path import exists

##Multiple strings throughout the whole code
##Multiple variables throughout the whole code 

def createNewTxtFile(): ##function that creates a new file with banks in it
    ##Storing a list into a dictionary
    if not exists("bankDetails.txt"):
        outfile = open("bankDetails.txt", 'w') 
        Dictionary = "{\n\t'ANZ': [0.03, 4],\n\t'Westpac': [0.04, 2],\n\t'CommonWealthBank': [0.02, 3],\n}" ##My dictionary, integers, constant and floats
        outfile.writelines(Dictionary)
        outfile.close()

createNewTxtFile() ##Calling this function first

def readFromBankDetails(fileName): ##function that reads the file
    with open(fileName, "r") as bankdetails:
        return literal_eval("".join([line for line in bankdetails.readlines()]))

def addToBankDetailsFile(fileName, nBankDetails : list[list]): ##function to add a new line/new bank details to the existing txt file
    try: ##My try and except 
        with open(fileName, "r") as bankDetails:
            oldBankDetails = bankDetails.readlines()[:-1]
        if (len(oldBankDetails) == 0):
            oldBankDetails = "{\n1" ##this includes the formatting for the list to show/add it line by line to the txt file
        for i in range(len(nBankDetails)): ##my for loop
            oldBankDetails += f"\t'{nBankDetails[i][0]}' : [{nBankDetails[i][1]}, {nBankDetails[i][2]}],\n"
        newBankDetails = "".join(oldBankDetails) + "}"
        with open(fileName, "w") as bankDetails:
            bankDetails.write(newBankDetails)
    except FileNotFoundError: ##The requested file doesn’t exist or is not located where expected.
        print("The file was not found in the database") 
    except ValueError: ##If the user inputs a string the ValueError will ensure that it should be a number 
        print("bankDetails.txt contains an invalid bank detail")
    except Exception as ex: ##This will handle the general 
        print("Unhandled exception: ", ex)

def leaveProgam(): ##This function is to leave the program and is connected to the exit button 
    exit()

def changeEntry(entry : Entry, text): ##using rhis function to show the output using an entry box
    entry.configure(state="normal")
    entry.delete(0, END)
    entry.insert(0, text)
    entry.configure(state="readonly") ##The user cannot enter anything in this entry box as it is read only

## Making GUI menu
Title= Label(window, text='Calculator Main Menu', font=('Arial', 20, 'bold'))
Title.grid(row=0, column=0, sticky='w', padx=5)
Title.config(bg="#6B5CA5")

## CALCULATE BALANCE PAGE -------------------

##adding labels
Title1 = Label(window, text='Calculate the balance in your account.', font=('Arial', 15, 'bold'))
Title1.grid(row=1, column=0, padx=5)
Title1.config(bg="#9EBD6E")

Label1 = Label(window, text="Which bank would you like to choose?", font=('Arial', 13))
Label1.grid(row=2, column=0, sticky='w', padx=5)
Label1.config(bg="#9EBD6E")

Label2 = Label(window, text="How much would you like to deposit?", font=('Arial', 13))
Label2.grid(row=3, column=0, sticky='w', padx=5)
Label2.config(bg="#9EBD6E")

Label3 = Label(window, text="The balance in your account after one year is: ", font=('Arial', 13))
Label3.grid(row=6, column=0, sticky='w', padx=5)
Label3.config(bg="#9EBD6E")

##adding a list box
myList = StringVar()
listOfBanks = Listbox(window, width=10, listvariable=myList)
listOfBanks.grid(row=2, column=1, padx=100, pady=15)
myList.set(tuple(readFromBankDetails('bankDetails.txt').keys()))

##adding entries
depositEntry = Entry(window, width=20, font=('Arial', 13))
depositEntry.grid(row=3, column=1)

def finalBalance(amountDeposited, interestRate, compound): ##function used to calculate the final balance
    if (amountDeposited > 0):
        balanceResult =(str((round(amountDeposited*((1+((interestRate)/(compound)))**(compound)), 2)))) ##Calculating the balance
        changeEntry(balance, balanceResult) ##this prints the result
    else:
        changeEntry(balance, "Deposit must be an positive number")

balance = Entry(window, width=30, state="readonly", font=('Arial', 13), text="")
balance.grid(row=6, column=1)

## adding buttons
def showResult():
    name = listOfBanks.get(ACTIVE)
    try:
        deposit = eval(depositEntry.get())
        finalBalance(deposit, readFromBankDetails('bankDetails.txt')[name][0], readFromBankDetails('bankDetails.txt')[name][1])
    except:
        changeEntry(balance, "Deposit must be a number")
        #balance.config(text="Deposit must be a number", width=30)

calcBalanceBtn = Button(window, text='Calculate', width=20, font=13, command=showResult)
calcBalanceBtn.grid(row=5, column=1, padx=5)

## ADD NEW BANK DETAILS PAGE---------------------

## adding more labels
Title2 = Label(window, text='Add a new bank', font=('Arial', 15, 'bold'))
Title2.grid(row=1, column=2, pady=10)
Title2.config(bg="#FFB997")

Label5 = Label(window, text="Enter the bank name: ", font=('Arial', 13))
Label5.grid(row=2, column=2, sticky='w', padx=5)
Label5.config(bg="#FFB997")

Label6 = Label(window, text="Enter the interest rate: ", font=('Arial', 13))
Label6.grid(row=3, column=2, sticky='w', padx=5)
Label6.config(bg="#FFB997")

Label7 = Label(window, text="Enter the compound: ", font=('Arial', 13))
Label7.grid(row=4, column=2, sticky='w', padx=5)
Label7.config(bg="#FFB997")

## adding entries
bankEntry = Entry(window, width=20, font=('Arial', 13))
bankEntry.grid(row=2, column=3)

interestEntry = Entry(window, width=20, font=('Arial', 13))
interestEntry.grid(row=3, column=3)

compoundEntry = Entry(window, width=20, font=('Arial', 13))
compoundEntry.grid(row=4, column=3)

def addToFile(): ## function that does the validation when a user enters an incorrect entry
    try:
        bankName = bankEntry.get()
    except:
        changeEntry(msg, "Must give a valid bank name")
        return
    try:
        interestRate = eval(interestEntry.get())
    except:
        changeEntry(msg, "Interest rate must be a number")
        return
    try:
        compounding = eval(compoundEntry.get())
    except:
        changeEntry(msg, "Compounding must be a number")
        return

    if interestRate <= 0:
        changeEntry(msg, "Interest rate must be a positive number")
    elif compounding <= 0:
        changeEntry(msg, "Compounding must be a positive number")
    else:
        changeEntry(msg, "Bank added successfully")
        addToBankDetailsFile('bankDetails.txt', [[bankName, interestRate, compounding]])
    
## adding buttons
addBank = Button(window, text='Add', width=20, font=13, command=addToFile)
addBank.grid(row=5, column=3, padx=5)

msg = Entry(window, width=40, state = "readonly", font=('Arial', 13), text="") ## this is a readonly entry box, just to show the output/error msgs
msg.grid(row=6, column=3)

exitProg = Button(window, text='Exit', width=20, font=13, command=leaveProgam)
exitProg.grid(row=8, column=0, padx=5, pady=100)

window.mainloop()
