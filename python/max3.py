


num1 = int(input())
num2 = int(input())
num3 = int(input())
#with temp variable
max_num = num1

if num2 > max_num:
    max_num = num2
if num3 > max_num:
    max_num = num3

print(max_num)

num1 = int(input())
num2 = int(input())
num3 = int(input())

max_num = max(num1, num2, num3)

print(max_num)

# with out using the temp Variable
num1 = int(input())
num2 = int(input())
num3 = int(input())
if num2>num1:
    num1=num2
if num3>num1:
    num1=num3
print(num1)

#nested if conditions
num1 = int(input())
num2 = int(input())
num3 = int(input())

if num2 > num1:
    if num3 > num2:
        max_num = num3
    else:
        max_num = num2
else:
    if num3 > num1:
        max_num = num3
    else:
        max_num = num1

print(max_num)

#maxof 3
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
num3 = int(input("Enter the third number: "))

if (num1 >= num2) and (num1 >= num3):
    print(num1, "is the largest number")
elif (num2 >= num1) and (num2 >= num3):
    print(num2, "is the largest number")
else:
    print(num3, "is the largest number")
