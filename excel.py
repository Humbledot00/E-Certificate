import pandas as pd

# Load the Excel file for participants
# Load the CSV file for events
events_df = pd.read_csv('event.csv')
participants_df = pd.read_csv('names.csv')

# Filter rows where 'Checked in' is 'Yes'
checked_in_events_df = events_df[events_df['Checked in'] == 'Yes']

# Create a dictionary from participants_df for quick lookup of names by USN
usn_to_name = dict(zip(participants_df['USN'], participants_df['Name']))

# Prepare a list to hold the rows of the new CSV
output_rows = []

# Iterate over the filtered rows
for index, row in checked_in_events_df.iterrows():
    usns = row[['USN of Team Lead', 'USN of Co-Member 1', 'USN of Co-Member 2', 'USN of Co-Member 3', 'USN of Co-Member 4', 'USN of Co-Member 5']]
    
    # Iterate over each USN in the current row
    for usn in usns:
        if pd.notna(usn):  # Check if the USN is not NaN
            usn_upper = usn.upper()  # Convert USN to uppercase
            name_upper = usn_to_name.get(usn_upper, 'Unknown').upper()  # Convert Name to uppercase
            output_rows.append({
                'Name': name_upper,
                'USN': usn_upper,
                'Event': row['Event']
            })

# Create a DataFrame from the list of rows
output_df = pd.DataFrame(output_rows, columns=['Name', 'USN', 'Event'])

# Write the DataFrame to a new CSV file
output_file_path = 'output.csv'
output_df.to_csv(output_file_path, index=False)

output_file_path
