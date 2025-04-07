my_list=list(map(int,input().split()))
n=len(my_list)
for i in range(n-1):
    for j in range(n-i-1):
        if my_list[j]>my_list[j+1]:
            my_list[j],my_list[j+1]=my_list[j+1],my_list[j]
print(my_list)