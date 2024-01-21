# United States JobSearch

## Project Description
The "United States JobSearch" program is a command-line interface program that allows users to search for and manage job listings in the United States. It provides the following functionalities:

1. **Search for Job Listings:** Users can enter their desired job title, location, and the number of job results they want to retrieve. The program uses the Adzuna jobs platform's API to fetch job listings matching the provided criteria.
2. **View Job List:** Users can view a list of job listings stored in CSV files. The program lists available CSV files in a directory and allows users to select a file to open. It displays job listings in a tabular format using the tabulate library.

This python script employs modular design for code organization, ensures a user-friendly command-line interface with input validation, integrates with the Adzuna API for real-time job listings, stores data in a CSV files with automatic file management, includes robust error handling, securely loads sensitive API credentials from environment variables, and offers an interactive user experience through menu-driven interactions.

### Project Structure:
* project.py
* test_project.py
* README.md
* requirements.txt
* jobs (folder)
    

### Functions
**main_menu** - This function appears as a menu-driven program that takes a user's choice as input and performs different action based on the user choice.

**search_jobs** - This function is designed to search for jobs on the Adzuna Platform using the Adzuna API. It takes parameters for job title, job location, and the number of desired job listing results. The function constructs an API request URL, makes a GET request to the Adzuna API, and returns a list of job results in the form of dictionaries. If the request is successful, it extracts and returns the job results; otherwise, it returns None. 

**store_jobs_in_csv** - This function retrieves job listings based on user-specified criteria and stores them in a CSV file. It first calls the **search_jobs** function to fetch job results. If results are found, it generates a unique CSV file name based on the job title and location, and creates the file if it doesn't exist. The function appends the job listings, including job title, company, and location, to the CSV file. It returns a message indicating whether the job results were added to an existing CSV file or saved in a new one. If no job listings are found, it returns a message indicating the absence of job listings.

**open_jobs_csv** - This function is designed to display job listings stored in CSV files. It checks for the existence of a directory where the CSV files are stored and provides feedback if the directory doesn't exist. It lists available CSV files and allows the user to select a file to open by entering an index or quitting with "q." Upon selecting a file, it attempts to open and read it. If the file contains data, it formats and displays the content in a tabular structure using the **tabulate** library. If the file is empty, it returns a message indicating that the CSV file contains no data. If the user provides an invalid input, it returns an appropriate error message.

### Flaws and Solution:

**Pytesting:**

**test_open_jobs_csv:** A potential flaw for this function is that it relies on a mock input value of '1' to select and open a specific CSV file for testing. The problem with this is if a user creates their own job listing.csv file in the "jobs" directory, it could lead to conflicts and unexpected behavior during testing. If the user-created CSV file becomes the first file in the directory (with an index of 1), the test would mistakenly open the user's file instead of the intended mock data file, potentially causing the test to fail or produce incorrect results.

**Solution:** There are two ways to fix this error, the first one is the hardcoded wherein the index of the mock data should match the index in the **test_open_jobs_csv** function. When it test the function, the pytest will pass all of the test successfully. The second solution is use a controlled environment for testing, such as a dedicated test directory with known CSV files for testing purposes. This would prevent conflicts with user-generated files and ensure consistent test results.

---

## Requirements
Before you can use this program, you'll need to ensure that you have the following requirements installed:
- Python 3.x
- Python Packages:
    - 'requests'
    - 'tabulate'
    - 'python-dotenv'
    - 'mock'

To install the python packages: `pip install -r requirements.txt`

---

## How to use the Program
1. Clone the repository or download the code.
2. Create a *'.env'* file in the same directory as the Python script with your Adzuna API credentials. The *'.env'* file should contain the following:
```
APP_ID=your_adzuna_app_id
API_KEY=your_adzuna_api_key
```
3. Run the program by executing the Python script:

`python your_script_name.py`

replace *'your_script_name.py'* with the name of the Python script that contains the code.

4. Follow the on-screen instructions:
    * Choose option 1 to search for job listings.
    * Enter the job title, location, and the number of job results you want.
    * Choose option 2 to view the job list.
    * Choose option 3 to quit the program.
    
5. When viewing the job list, you can select a CSV file to open by entering the index numeber of the file.

---

## How It Works
The program uses the Adzuna API to search for job listings based on your specific job title, location, and the number of job results. It stores the job listings in CSV file format, one file for each search, within a **'jobs'** folder.

**Option 1: Searching for Jobs**
* Collects user input for job title, location, and number of job results.
* Sends a request to the Adzuna API.
* Store the job listings result in a CSV file.

**Option 2: Viewing the Job lists**
* List available CSV files in the **'jobs'** folder.
* Allows the user to select a file to view.
* Displays the job listings in a tabulated format.

**Option 3: Quitting the Program**
* Allows the user to exit from the program.
___

### Video Demonstration 
Youtube Link: [CS50P Final Project](https://youtu.be/M56x-Lxm9aI)

---

<div style="text-align: center;"> 
<p style="font-size: 14px;">"This was CS50" - David J. Malan </p>
</div>
