# Step 1: Take input from the user and convert it to a list of integers
num = list(map(int, input().split()))
in_val=int(input())
# Step 2: Create an empty list to store all generated numbers
gen_num = []

# Step 3: Add the initial numbers to the list
for n in num:
    gen_num.append(n)  # Ensure you're appending 'n', not 'num'

# Step 4: Generate new numbers by adding or subtracting elements from the input list
i = 0
while i < len(gen_num):
    curr = gen_num[i]
    for op in num:
        num_add = curr + op
        num_sub = curr - op
        # Add the new numbers to the list if they are within the range 1 to 125 and not already in the list
        if 1 <= num_add <= in_val and num_add not in gen_num:
            gen_num.append(num_add)
        if 1 <= num_sub <= in_val and num_sub not in gen_num:
            gen_num.append(num_sub)
    i += 1

# Step 5: Sort the list using Python's built-in sort function
gen_num.sort()

# Step 6: Print the sorted list
print(gen_num)

