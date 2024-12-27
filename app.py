import pandas as pd

# Load the two CSV files into DataFrames
events_df = pd.read_csv('error.csv', header=None, names=['Name', 'USN', 'Event'])
participants_df = pd.read_csv('names.csv')

# Create a dictionary from participants_df for quick lookup of names by USN
usn_to_name = dict(zip(participants_df['USN'], participants_df['Name']))

# Replace "UNKNOWN" with the corresponding name from participants_df based on USN
events_df['Name'] = events_df['USN'].apply(lambda usn: usn_to_name.get(usn, 'UNKNOWN'))

# Save the updated DataFrame to a new CSV file
output_file_path = 'output.csv'
events_df.to_csv(output_file_path, index=False, header=False)

print(f"Updated file saved to {output_file_path}")
