import datetime
import mysql.connector as s
dot= datetime.date.today()
from tabulate import tabulate
print("***********************************************")
print(" BANK MANAGEMENT SYSTEM ")
print("***********************************************")

print("===============================")
print(" ----Welcome to National Bank----")
print("***********************************************")
print("=<< 1. Open a new account                >>=")
print("=<< 2. Withdraw Money                    >>=")
print("=<< 3. Deposit Money                     >>=")
print("=<< 4. Balance Enquiry                   >>=")
print("=<< 5. Modify Account                    >>=")
print("=<< 6. Display account                   >>=")
print("=<< 7. Transaction History               >>=")
print("=<< 8. Exit                              >>=")
print("***********************************************")
    
#Creating Table
mydb=s.connect(host="localhost",user="root",password="Arjun")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists bank")
mycursor.execute("use bank")
mycursor.execute("CREATE TABLE if not exists bank_master(acno  int(6) AUTO_INCREMENT primary key , Name varchar(35),\
                                     DOB date,Gender char(1),City varchar(35), Phone_Number varchar(11),Balance int(10) )")
mycursor.execute("create table if not exists banktrans(acno int(6),amount int(6),dot date,ttype char(1),foreign key (acno) references bank_master(acno))")

def Create_Account():
    username=input("Enter the Account holder name: ")
    yob=int(input("Enter year of birth: "))
    mob=int(input("Enter month of birth: "))
    d_ob=int(input("Enter date of birth: "))
    gen=input("Enter Gender M or F: ")
    DOB=datetime.datetime(yob,mob,d_ob)
    city=input("Enter your City: ")
    ph_no=input("Enter Phone Number: ")
    balance=0
    mycursor.execute("INSERT INTO bank_master(Name,DOB,Gender,City,Phone_Number,Balance) VALUES\
                     (%s,%s,%s,%s,%s,%s)",(username,DOB,gen.capitalize(),city, ph_no,balance))
    
    acc_no=int(mycursor.lastrowid)
    mydb.commit()
    print("----New account created successfully !----")
    print("Your Account Number: ",acc_no)
    print("Your Account Balance: ",balance)
    
def Withdraw_Money():
    ttype='W'
    acc_no=int(input("Enter your Account Number: "))
    mon=int(input("Enter the Amount you want to withdraw: "))
    mycursor.execute("select * from bank_master where acno=%s",(acc_no,))
    myrecords=mycursor.fetchall()
    for row in myrecords:
        balance=row[6]
    if mon>balance:
        print ("Not enough Balance")
    else:
        balance-=mon
        print("Amount Withdrawn: ",mon)
        print("Your Account Balance: ",balance)
    mycursor.execute("Update bank_master set Balance=%s where\
                                acno=%s",(balance,acc_no))
    mycursor.execute("insert into banktrans values(%s,%s,%s,%s)",(acc_no,mon,dot,ttype))
    mydb.commit()

def Deposit_Money():
    ttype='D'
    acc_no=int(input("Enter Your Account Number: "))
    mon=int(input("Enter Amount of money you want to Deposit: "))
    mycursor.execute("select * from bank_master where acno=%s",(acc_no,))
    myrecords=mycursor.fetchall()
    for row in myrecords:
        balance=row[6]
    
    mycursor.execute("Update bank_master set Balance=Balance+%s where\
                                     acno=%s",(mon,acc_no))
    mycursor.execute("insert into banktrans values(%s,%s,%s,%s)",(acc_no,mon,dot,ttype))
    mydb.commit()
    balance=balance+mon
    print("Amount deposited: ",mon)
    print("Your Account Balance: ",balance)


def Balance_Enquiry():
    acc_number=int(input('enter your account number'))
    mycursor.execute('select acno,Balance from bank_master where\
                                    acno=%s',(acc_number,))
    record=mycursor.fetchall()
    for row in record:
        print('account number : ',row[0])
        print('current balance: ',row[1])

def Transaction_History():
    a=[['Account No','Amount','Transaction date','Transaction Type']]
    acc_number=int(input('enter your account number'))
    mycursor.execute('select * from banktrans where acno=%s',(acc_number,))
    record=mycursor.fetchall()
    for i in record:
        a.append(list(i))
    table1 = tabulate(a,headers='firstrow',tablefmt='grid')
    print(table1)
     
def Modify_Account():
    acc_number=int(input('Enter your account number:'))
    print('''            1) modifiy yor name
            2) modify your date of birth
            3) modify your city of residence
            4) modify your phone number
            5) modify your gender''')
    x=int(input('enter your choice'))
    if x==1:
         newname=input("Enter the correct Account holder name: ")
         mycursor.execute('update bank_master set Name=%s where\
                                         acno=%s',(newname,acc_number))
         mydb.commit()
    if x==2:
         yob=int(input("Enter year of birth: "))
         mob=int(input("Enter month of birth: "))
         d_ob=int(input("Enter date of birth: "))
         DOB1=datetime.datetime(yob,mob,d_ob)
         mycursor.execute('update bank_master set DOB=%s where\
                                          acno=%s',(DOB1,acc_number))
         mydb.commit()
    if x==3:
         city=input("Enter your City: ")
         mycursor.execute('update bank_master set City=%s where\
                                         acno=%s',(city,acc_number))
         mydb.commit()
    if x==4:
         ph_no=input("Enter Phone Number: ")
         mycursor.execute('update bank_master set Phone_Number=%s where\
                                        acno=%s',(ph_no,acc_number))
         mydb.commit()
    if x==5:
        gen=input("Enter your Gender: ")
        mycursor.execute('update bank_master set Gender=%s where\
                                        acno=%s',(gen,acc_number))
        mydb.commit()
        
    print('account modified')

def Display_account():
    a=[['Account Number','Name','DOB','Gender','City','Phone.no','Balance']]
    acno=str(input("Enter account number:"))
    mycursor.execute('select * from bank_master where\
                                    acno=%s',(acno,))
    
    for i in mycursor:
        a.append(list(i))
    print("Account info table:")
    b=tabulate(a,headers='firstrow',tablefmt='psql')
    print(b)
    
    
ch="y"
while ch=="y":
    choicenumber = input("Select your choice number from the above menu : ")
    if choicenumber == "1":
        print("Choice number 1 is selected by the customer")
        Create_Account()
        
    elif choicenumber =="2":
        print("Choice number 2 is selected by the customer")
        Withdraw_Money()

    elif choicenumber== "3":
        print("Choice number 3 is selected by the customer")
        Deposit_Money()

    elif choicenumber== "4":
        print("Choice number 4 is selected by the customer")
        Balance_Enquiry()

    elif choicenumber== "5":
        print("Choice number 5 is selected by the customer")
        Modify_Account()

    elif choicenumber == "6":
        print("Choice number 6 is selected by the customer")
        Display_account()
        
    elif choicenumber == "7":
        print("Choice number 7 is selected by the customer")
        Transaction_History()

    elif choicenumber == "8":
        print("Choice number 8 is selected by the customer")
        print("Thank you for using our banking system!")
        print("\n")
        print("Come again")
        print("Bye bye")
        
    else:
        print("Invalid option selected by the customer")
        print("Please Try again!")

    ch=input("Do you want to continue or not?(y for yes, n for no)  :").lower()  

