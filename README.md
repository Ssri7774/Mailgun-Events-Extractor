# Mailgun Events Data Extractor

This Python script extracts email events data from the Mailgun API for a specified domain and time range. It allows users to filter events by subject and convert the output to a CSV format.

## Features

- Retrieve raw event data from Mailgun API.
- Filter events by subject.
- Convert filtered or raw data to CSV format.
- User-friendly prompts with retry options for input validation.

## Requirements

- Python 3.x
- Mailgun account and API key
- `curl` installed on your system

## Installation

1. **Clone the repository (if applicable):**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. **Install required packages (if any):**
   Ensure you have the necessary Python libraries installed. You can create a virtual environment and install any required packages. If you're using only built-in libraries (like `json`, `csv`, etc.), no additional installation is needed.


## Usage
1. Run the script:

```
python3 mailgun_events_extractor.py
```
2. Follow the prompts to enter:
  - Your Mailgun API key (input is hidden for security).
  - Your Mailgun domain (e.g., `mg.yourdomain.com`).
  - Start and end epoch times for the events you want to retrieve.

  ### Converting Epoch Time
  To convert a human-readable date and time to epoch time, you can use various methods:
  
  - **Online Epoch Converters**: You can use online tools like [Epoch Converter](https://www.epochconverter.com) to quickly convert your desired date and time into epoch format.
  - **Using Python**: You can also use Python to convert a date to epoch time:
    ```
    from datetime import datetime
  
    # Replace 'YYYY-MM-DD HH:MM:SS' with your desired date and time
    dt = datetime.strptime('YYYY-MM-DD HH:MM:SS', '%Y-%m-%d %H:%M:%S')
    epoch_time = int(dt.timestamp())
    print(epoch_time)
    ```

3. After retrieving the events, the script will:
 - Save the raw JSON output to a file named `{domain}-report.json`.
 - Ask if you want to filter the events by subject.\
 - If filtering is chosen, enter the desired subject.
 - Save the filtered results to `{domain}-filtered-report.json`.

4. You will then be prompted to convert the JSON data to CSV format:
  - Choose to use either the raw or filtered data.
  - The CSV file will be saved as `{domain}-report.csv` or `{domain}-filtered-report.csv`.

## Example
```
Enter your Mailgun API key: 
Enter your Mailgun domain (e.g., mg.yourdomain.com): mg.yourdomain.com
Enter the start epoch time (e.g., 1729017600): 1729017600
Enter the end epoch time (e.g., 1734431999): 1734431999
```

## Output
- Raw events data will be saved to `mg.yourdomain.com-report.json`.
- Filtered results will be saved to `mg.yourdomain.com-filtered-report.json` if filtering is applied.
- CSV files will be saved as `mg.yourdomain.com-report.csv` or `mg.yourdomain.com-filtered-report.csv`.

## Notes
- Ensure that the epoch time format is correct and that the time range covers the events you wish to retrieve.
- The script will handle invalid inputs and prompt the user accordingly, allowing up to three attempts for each input.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Author
[Sri]

## Changes Made:
- Added a section on converting epoch time under the **Usage** section.
- Provided methods for converting human-readable dates to epoch time, including an online converter and a Python example. 

Feel free to modify any parts to better fit your project or personal preferences!
