import json
import csv
import subprocess
import getpass
from datetime import datetime

# Function to convert epoch time to human-readable format
def convert_epoch_to_human_readable(epoch_time):
    return datetime.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')

# Function to prompt user with retries (up to 3 attempts)
def prompt_user_input(prompt_message, hidden=False, yes_no=False):
    attempts = 0
    while attempts < 3:
        if hidden:
            user_input = getpass.getpass(prompt_message)
        else:
            user_input = input(prompt_message).strip().lower()
        
        # Check if input is valid for yes/no prompts
        if yes_no:
            if user_input in ['yes', 'no']:
                return user_input
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        elif user_input:
            return user_input

        attempts += 1
        print(f"Input cannot be empty. You have {3 - attempts} attempt(s) remaining.")
    
    print("Exceeded the maximum number of attempts. Exiting.")
    exit(1)

# Prompt the user for inputs with retries and hidden API key input
api_key = prompt_user_input("Enter your Mailgun API key: ", hidden=True)
domain = prompt_user_input("Enter your Mailgun domain (e.g., mg.yourdomain.com): ")
begin_time = prompt_user_input("Enter the start epoch time (e.g., 1729017600): ")
end_time = prompt_user_input("Enter the end epoch time (e.g., 1734431999): ")

# Execute the curl command and capture the output
curl_command = [
    'curl', '-s', '--user', f'api:{api_key}',
    f'https://api.mailgun.net/v3/{domain}/events?begin={begin_time}&end={end_time}'
]
curl_output = subprocess.check_output(curl_command).decode('utf-8')

# Save the raw curl output to {domain}-report.json
report_filename = f"{domain}-report.json"
with open(report_filename, 'w') as report_file:
    report_file.write(curl_output)

print(f"********************************************************************\nRaw events data saved to {report_filename}\n********************************************************************")

# Parse the JSON output from the saved file
with open(report_filename, 'r') as file:
    data = json.load(file)

# Ask whether to proceed with subject filtering or quit
proceed = prompt_user_input("Do you want to filter the events by subject? (yes/no): ", yes_no=True)

filtered_events = data.get('items', [])
if proceed == 'yes':
    # Prompt for the desired subject
    desired_subject = prompt_user_input("Enter the subject to filter events by (e.g., Congratulations on Your Stellar Performance): ").strip()

    # Filter the events by the subject
    filtered_events = []
    for event in data.get('items', []):
        if 'message' in event and 'headers' in event['message']:
            subject = event['message']['headers'].get('subject', '').lower()  # Normalize subject
            print(f"Checking event with subject: {subject}")  # Debugging print
            if desired_subject in subject:
                # Convert the event timestamp (assuming it's in 'timestamp' field)
                if 'timestamp' in event:
                    event['human_readable_time'] = convert_epoch_to_human_readable(event['timestamp'])
                filtered_events.append(event)

    # Save filtered results to a JSON file
    filtered_filename = f"{domain}-filtered-report.json"
    with open(filtered_filename, 'w') as outfile:
        json.dump(filtered_events, outfile, indent=4)

    print(f"********************************************************************\nFiltered results saved to {filtered_filename}\n********************************************************************")
else:
    print("No filtering applied. Exiting.")

# Ask whether to convert the JSON data to CSV
convert_to_csv = prompt_user_input("Do you want to convert the filtered events to a CSV file? (yes/no): ", yes_no=True)

if convert_to_csv == 'yes':
    # Prompt for the file to use: raw or filtered
    file_choice = prompt_user_input(f"Do you want to use the raw JSON data or the filtered data? (raw/filtered): ").lower()
    json_file_to_convert = report_filename if file_choice == 'raw' else filtered_filename

    # Load the selected JSON data
    with open(json_file_to_convert, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Prepare the CSV output file
    csv_file = f"{domain}-report.csv" if file_choice == 'raw' else f"{domain}-filtered-report.csv"
    csv_columns = ['timestamp', 'human_readable_time', 'originating-ip', 'event', 'recipient', 'subject', 'message_id', 'sender']

    # Open the CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        # Loop through each event in the JSON data
        for event in json_data:
            # Convert timestamp to human-readable time
            human_readable_time = convert_epoch_to_human_readable(event['timestamp']) if 'timestamp' in event else ''
            
            # Extract relevant data
            message_headers = event.get('message', {}).get('headers', {})
            row = {
                'timestamp': event.get('timestamp', ''),
                'human_readable_time': human_readable_time,
                'originating-ip': event.get('originating-ip', ''),
                'event': event.get('event', ''),
                'recipient': event.get('recipient', ''),
                'subject': message_headers.get('subject', ''),
                'message_id': message_headers.get('message-id', ''),
                'sender': event.get('envelope', {}).get('sender', '')
            }

            # Write the row to the CSV file
            writer.writerow(row)

    print(f"********************************************************************\nData has been written to {csv_file}\n********************************************************************")
else:
    print("CSV conversion skipped.")