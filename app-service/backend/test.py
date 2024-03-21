def count_unique_values(file_path):
    unique_values = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespaces
            line = line.strip()
            # Add the value to the set of unique values
            unique_values.add(line)
    
    # Count the number of unique values
    unique_count = len(unique_values)
    
    return unique_count

# Example usage:
file_path = 'test.txt'  # Adjust the file path accordingly
unique_count = count_unique_values(file_path)
print("Number of unique values in the file:", unique_count)
