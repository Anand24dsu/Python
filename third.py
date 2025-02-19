# print_pyramid.py
def print_pyramid(n):
    # Loop through each row
    for i in range(n):
        # Calculate number of stars for this row (odd numbers: 1, 3, 5, ...)
        stars = 2 * i + 1
        # Calculate number of spaces to center the stars
        spaces = n - i - 1
        # Print the spaces followed by the stars
        print(" " * spaces + "*" * stars)

# Get the height of the pyramid from the user
n = int(input("Enter the height of the pyramid: "))

# Call the function to print the pyramid
print_pyramid(n)
