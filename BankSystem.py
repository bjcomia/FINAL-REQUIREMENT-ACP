from MainMenuMethods import MainMenuVerifyInfo, MainMenuCustomerDatabase
from CustomerInformationInquiry import customerInfo
import collections
import json

class bankSystem:
    def __init__(self):
        self.bankBalance = 0.0
        self.customerDatabase = collections.defaultdict(dict)
        self.jsonToDict()
        self.customerID = int(self.customerNewID()) 
        self.accountNumber = int(self.customerNewAccNum())
        self.activityLog = []
        self.mintCount = 5
        
    def mintMoney(self):
        print("The minting limit is currently at Php 50,000.00")
        print(f"You have {self.mintCount} mints left.")
        if self.mintCount <= 5 and self.mintCount >= 1:
            addMoney = float(input("Enter amount to be minted: "))
            if addMoney < 0 or addMoney > 50000.00:
                print("Invalid Input. Please try again")
                return
            self.bankBalance = self.bankBalance + addMoney
            self.mintCount = self.mintCount - 1
            print(f"The current balance is {self.bankBalance}") 
        else:
            print("You reached the max limit for minting money today.")
        
    def burnMoney(self):
        if self.bankBalance == 0:
            print("There are no funds to be burned.")
        else:
            burnMoney = float(input("Enter amount to be burned: "))
            self.bankBalance = self.bankBalance - burnMoney
            print(f"The current balance is {self.bankBalance}") 

    def openAccount(self):
        print(f"Enter information for customer {self.customerID}")
        customerObj = customerInfo()
        customerObj.accountNumber = self.accountNumber
        customerObj.customerID = self.customerID
        customerObj.creditLevel = int(self.creditLevel())
        customerObj.creditTier = str(self.creditTierTest(customerObj.creditLevel))
        customerObj.loanLimitAcc = float(self.loanLimit(customerObj.creditLevel))
        customerObj.loan = 0
        
        while True:
            print("\nPlease verify the following information:")
            customerObj.displayInfo()
            
            print("[1] Yes, That is correct")
            print("[2] No, I want to change some information")
            choiceVerify = int(input("Enter your choice: "))
            if choiceVerify == 2:
                MainMenuVerifyInfo()
                while True:
                    choiceChange = int(input("Enter your choice: "))
                    if choiceChange == 1:
                        customerObj.firstName = str(input("Enter first name: "))
                        break
                    elif choiceChange == 2:
                        customerObj.lastName = str(input("Enter last name: "))
                        break
                    elif choiceChange == 3:
                        customerObj. age = int(input("Enter age: "))
                        break
                    elif choiceChange == 4:
                        customerObj.address = str(input("Enter address: "))
                        break
                    elif choiceChange == 5:
                        customerObj.pin = int(input("Enter pin: "))
                        break
                    elif choiceChange == 6:
                        customerObj.username = input("Enter username: ")
                        break
                    elif choiceChange == 7:
                        customerObj.password = input("Enter password: ")
                        break
                    elif choiceChange == 8:
                        customerObj.balance = input("Enter initial deposit: ")
                        break
                    elif choiceChange == 9:
                        break
                    else:
                        print("Invalid Input. Please try again.")
                        
            elif choiceVerify == 1:
                self.customerDatabase[self.customerID] = {}
                self.customerDatabase[self.customerID]["First Name:"] =  customerObj.firstName
                self.customerDatabase[self.customerID]["Last Name:"] = customerObj.lastName
                self.customerDatabase[self.customerID]["Age:"] = customerObj.age
                self.customerDatabase[self.customerID]["Address:"] = customerObj.address
                self.customerDatabase[self.customerID]["Account Number:"] = customerObj.accountNumber
                self.customerDatabase[self.customerID]["Pin:"] = customerObj.pin
                self.customerDatabase[self.customerID]["Username:"] = customerObj.username
                self.customerDatabase[self.customerID]["Password:"] = customerObj.password
                self.customerDatabase[self.customerID]["Balance:"] = customerObj.balance
                self.customerDatabase[self.customerID]["Credit Level:"] = customerObj.creditLevel
                self.customerDatabase[self.customerID]["Loan Limit:"] = customerObj.loanLimitAcc
                self.customerDatabase[self.customerID]["Loan:"] = customerObj.loan
                break
            else:
                print("Invalid Input. Please try again.")
    
        self.bankBalance = self.bankBalance + customerObj.balance
        self.customerID = self.customerID + 1
        self.accountNumber = self.accountNumber + 1
        self.addToCustomerJsonFile()
    
    def loanAssesment(self):
        self.jsonToDict()
        
        choiceCustomer = str(input("Enter ID of customer: "))
        customerExistence = self.checkCustomerExistence(choiceCustomer)
        if customerExistence == False: return
        
        customerCreditLevel = int(self.customerDatabase[choiceCustomer]["Credit Level:"])
        customerLoan =  float(self.customerDatabase[choiceCustomer]["Loan:"])
        customerLoanLimit = float(self.customerDatabase[choiceCustomer]["Loan Limit:"])
        customerLoanInterestRate = self.customerLoanInterestRate(customerCreditLevel)
        print(f"Customer {choiceCustomer} currently has a loan amounting to {customerLoan}.")
        
        if customerCreditLevel == 1:
            print(f"Customer {customerCreditLevel} cannot loan in the bank because he/she has no tier.")
            return
        else:
            loanAmount = float(input("How much money will be loaned: "))
            if loanAmount > customerLoanLimit:
                print(f"You entered an amount that exceeds the loan limit of Customer {choiceCustomer}")
            elif loanAmount <= 0:
                print(f"You entered an invalid amount")
            else:
                loanWithInterest = loanAmount + (customerLoanInterestRate * loanAmount)
                print("\nThe following transactions are made: ")
                print(f"Loan placed: {loanAmount}")
                print(f"Loan to be payed (with annual interest): {loanWithInterest}")
                
                self.customerDatabase[choiceCustomer]["Loan:"] = float(loanWithInterest)
                self.addToCustomerJsonFile()
                
    def accessCustomerDatabase(self):
        while True:
            MainMenuCustomerDatabase()
            choiceCustomerDatabase = int(input("Enter your choice: "))
            if choiceCustomerDatabase == 1:
                self.showCustomerDatabase()
            elif choiceCustomerDatabase == 2:
                choiceCustomer = str(input("Enter ID of customer to be searched: "))
                customerExistence = self.checkCustomerExistence(choiceCustomer)
                if customerExistence == False: return
                print("\nCustomer ID:", choiceCustomer)
                for customerID in self.customerDatabase[choiceCustomer]:
                    print("   ", customerID, self.customerDatabase[choiceCustomer][customerID])
            elif choiceCustomerDatabase == 3:
                break
            else:
                print("Invalid Input. Please try again.")
                    
    def showCustomerDatabase(self):
        for CustomerID, CustomerInformation in self.customerDatabase.items():
            print("Customer ID:", CustomerID)
            for keyInfo in CustomerInformation:
                print("   ", keyInfo, CustomerInformation[keyInfo]) 
                
    def displayTest(self):
        choiceID = str(input("Enter customer ID to be found: "))
        print(self.customerDatabase[choiceID]["Balance:"])
        
    def jsonToDict(self):
        try:
            with open("Database/CustomerDatabase.json") as customerDatabaseJSON:
                self.customerDatabase = json.load(customerDatabaseJSON)
            
            customerDatabaseJSON.close()
        except:
            self.customerDatabase[1001] = {}
            
    def addToCustomerJsonFile(self):
        with open("Database/CustomerDatabase.json", "w") as customerJsonFile:
            json.dump(self.customerDatabase, customerJsonFile)
            
        customerJsonFile.close()
        
    def customerNewID(self):
        if len(self.customerDatabase) - 1 != 0:
            for dictID in reversed(self.customerDatabase.keys()):
                newID = int(dictID)
                return newID + 1
        else:
            return 1001
        
    def customerNewAccNum(self):
        if len(self.customerDatabase) - 1 != 0:
             for dictID in reversed(self.customerDatabase.keys()):
                newAccNum = int(self.customerDatabase[dictID]["Account Number:"])
                return newAccNum + 1  
        else:
            return 69347501   
            
    def creditLevel(self):
        while True:
            creditScore = int(input("Enter credit score(0-100): "))
            if creditScore >= 0 and creditScore <= 25:
                return 1
            elif creditScore >= 26 and creditScore <= 50:
                return 2
            elif creditScore >= 51 and creditScore <= 75:
                return 3
            elif creditScore >= 75 and creditScore <= 100:
                return 4
            else:
                print("Invalid Input. Please try again")
                break
            
    def creditTierTest(self, creditLevelTest = 0):
        tierOfAccount = {
            1: "No Tier",
            2: "Bronze Tier",
            3: "Silver Tier",
            4: "Gold Tier"
        }
        return tierOfAccount.get(creditLevelTest)
    
    def loanLimit(self, creditLevelTest = 0):
        loanLimitOfAccount = {
            1: 0,
            2: 5000,
            3: 10000,
            4: 50000
        }
        return loanLimitOfAccount.get(creditLevelTest)
    
    def customerLoanInterestRate(self, creditLevelTest = 0):
        interestRateOfAccount = {
            2: 0.25,
            3: 0.225,
            4: 0.20
        }
        return interestRateOfAccount.get(creditLevelTest)
    
    def checkCustomerExistence(self, customerTestID = ""):
        if customerTestID in self.customerDatabase.keys():
            return True
        else:
            print(f"Customer {customerTestID} does not exist.")
            return False