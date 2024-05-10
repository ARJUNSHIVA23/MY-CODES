import csv
f=open('Emp.csv','w')
mywriter=csv.writer(f,delimiter=',')
ans='y'
while ans.lower()=='y':
    no=int(input("Enter empo no"))
    name=input('enter name')
    Salary=int(input('enter employee salary'))
    mywriter.writerow([no,name,Salary])
    ans=input("Add more y or n")


