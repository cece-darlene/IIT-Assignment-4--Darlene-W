##Author: Darlene Widjaja
##Date created: 11/03/2022
##Date last changed: 24/04/2022
##The purpose of this program is to produce a shell based menu for the user to be able to add in new bank details 
    ##AND to be able to calculate the balance in their account after one year
        ##The calculation will be made using the amount deposited, interest rate of the bank and the compound of the bank
            ##The bankDetails.txt is a shared document between these two programs

from ast import literal_eval
import hmac
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
        input("\nThe data has been stored! :) (Press enter)\n\n")
    except FileNotFoundError: ##The requested file doesn’t exist or is not located where expected.
        print("The file was not found in the database") 
    except ValueError: ##If the user inputs a string the ValueError will ensure that it should be a number 
        print("bankDetails.txt contains an invalid bank detail")
    except Exception as ex: ##This will handle the general 
        print("Unhandled exception: ", ex)

def printMenu(): ##printing the shell based menu 
    while True:
        try: ##My try and except tool to handle invalid input
            print('----------------------------------------')
            print('Calculator Main Menu')
            print('----------------------------------------')
            print("1) Calculate the balance in your account after one year by choosing a specific bank.")
            print("2) Contribute by adding a new bank's details to our database!")
            print("3) Exit")
            userInput = int(input(": "))
            if (userInput <= 0):
                input("You have entered an invalid input. Negative numbers or 0 is not allowed!")
            elif (userInput == 3):
                input("You have chosen to exit")
                exit()
            elif (userInput >= 4):
                input("You have entered an invalid input. Numbers greater than 3 are not allowed!")
            else:
                showSubMenu(userInput) ##asking for user input as a number 
        except ValueError: ##Will handle input dealing with numbers and user inputing a string when it should be a number
            input("You have entered an invalid input. Strings are not allowed!")

def showSubMenu(userRespond): ##function that deals with the user input
    bankList = readFromBankDetails('bankDetails.txt')
    if userRespond == 1: #My if/else statement
        while True:
            print('If you are unsure which bank to pick, these are some options:\n ANZ\n Westpac\n CommonWealthBank')
            bank = input('Which bank would you like to choose to calculate the balance in your account after one year? ') 
            bankDetails = getBankDetails(bank,bankList) ##Only have to call once to get the details
            valid = bankDetails[0]
            interest = bankDetails[1]
            compound = bankDetails[2]
            ##can put while loop here
            if(valid):
                while True:
                    try:
                        deposit = input("How much would you like to deposit? ")
                        depositFloat = float(deposit)
                        if (depositFloat <= 0):
                            input("You have entered an invalid input. Negative numbers or 0 is not allowed! Please Try Again!")
                        else:
                            break
                    except ValueError: ##Will handle input dealing with numbers and user inputing a string when it should be a number
                        print("You have entered an invalid input. Strings are not allowed!")
            if(valid):
                break
        finalBalance(bank, depositFloat, interest, compound)  ##My float and user input
    elif userRespond == 2:
        try:
            bankDetails = [] ##empty list
            bankNum = int(input("How many bank details would you like to enter? (1, 2, 3...): ")) ##My input as an integer 
        except ValueError: ##Will handle input dealing with numbers and user inputing a string when it should be a number
            print("You have entered an invalid input. Strings are not allowed!")
        count = 0
        while count < bankNum: ##my while loop
            bankNameQuest = input(f"Please enter the name for bank {count+1}: ") ##Assuming that some banks can have characters and numbers in the name
            if any(char.isdigit() for char in bankNameQuest):
                input("Please do not include digits in the bank name!")
            else:
                while True:
                    try:
                        interestRateQuest = float(input(f"Please enter the interest rate for bank {count+1}: "))
                        compoundQuest = float(input(f"Please enter the compound for bank {count+1}: "))
                        if (interestRateQuest > 0) and (compoundQuest > 0):
                            bankDetails.append([bankNameQuest, interestRateQuest, compoundQuest])
                            addToBankDetailsFile("bankDetails.txt", bankDetails)
                        else:
                            input("You have entered a negative number. Please try again!")
                        break
                    except ValueError: ##Will handle input dealing with numbers and user inputing a string when it should be a number
                        print("You have entered a string or character that is not allowed. Please try again!")
            count = count + 1   
    else:
        input("You have entered a value out of the range: 1, 2, 3. Press enter to start again")

def getBankDetails(bank2,bankList): ##function that reads ands checks the bank details to see if it is in the database/txt file
    try:
        bankDetails = bankList[bank2] ##checking if the bank matches the key in the list
        interestRate= bankDetails[0]
        compound= bankDetails[1]
    except KeyError: ##There is no such key in dictionary OR there is no key with this name
        input("\nSorry that bank is not in our database :(. Press enter to start again.\n\n") ##My string and input
        return([False, -1, -1])
    return([True, interestRate, compound]) 
        
def main(): ##the main function that will be controlling the program
    createNewTxtFile() 
    printMenu()

def finalBalance(bankChoice, amountDeposited, interestRate, compound): ##function used to calculate the final balance
    try:
        input('The balance in your account after 1 year IN AUD using ' + bankChoice + ' is: $' + str((round(amountDeposited*((1+(interestRate/compound))**compound), 2)))) ##Calculating the balance, INPUT used so when the user presses enter the program will run again
    except KeyError: ##There is no such key in dictionary OR there is no key with this name
        input("\nSorry that bank is not in our database :(. Press enter to start again.\n\n") ##My string and input

main() ##calling the main function
