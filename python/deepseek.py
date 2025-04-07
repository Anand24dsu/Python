def new_func():
    n=int(input())
    for i in range(n):
        print(" "*(n-i-1)+"*"*(2*i+1))

new_func()