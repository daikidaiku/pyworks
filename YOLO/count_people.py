# Define the path to the file
file_path = '/Users/daiki_daiku/Documents/pyworks/YOLO/lab.txt'

# Initialize a counter for the lines where the first column is 0
count = 0

# Open the file and read it line by line
with open(file_path, 'r') as file:
    for line in file:
      # Split the line into columns
      columns = line.split()
      # Check if the first column is 0
      if columns[0] == '0':
        count += 1

# Print the count
print(count)
