#swapped condition
arr=list(map(int,input().split()))
n=len(arr)
for i in range(n-1):
    swapped=False
    for j in range(n-i-1):
        if arr[j]>arr[j+1]:
            arr[j],arr[j+1]=arr[j+1],arr[j]
            swapped=True
    if not swapped:
        break
print(arr)