import os
import csv
import sys
import requests

from dotenv import load_dotenv
from tabulate import tabulate


def main():
    # Print the welcome screen
    print("\n\t\tUnited States JobSearch")
    print("==============================================================")
    print("  [1] Search Jobs")
    print("  [2] View Job List")
    print("  [3] Quit")
    print("--------------------------------------------------------------")

    # Get the user's choice
    try:
        user_choice = int(input(" Choose your desired option: "))
    except ValueError:
        # If the user enters an invalid input, print an error message and exit the program
        print("--------------------------------------------------------------")
        sys.exit("\n Invalid Input!")

    # Call the main_menu() function with the user's choice
    main_menu(user_choice)


def main_menu(user_choice):
    # Use a match statement to handle the user's choice
    match (user_choice):
        # Case 1: Search for jobs
        case 1:
            # Get the job title, location, and number of job results from the user
            jobs = input(" Search Jobs: ").strip().title()
            jobs_loc = input(" Location: ").strip().title()
            num_jobs = int(input(" Number of Job Results: "))

            # Print a separator
            print("--------------------------------------------------------------")

            # Call the store_jobs_in_csv() function to store the job results in a CSV file
            print(f"\n {store_jobs_in_csv(jobs, jobs_loc, num_jobs)}")

        # Case 2: View the job list
        case 2:
            # Print a separator
            print("--------------------------------------------------------------")

            # Call the open_jobs_csv() function to open and display the job list CSV file
            print(open_jobs_csv())

        # Case 3: Quit the program
        case 3:
            # Print a separator
            print("--------------------------------------------------------------")

            # Print a goodbye message and exit the program
            sys.exit("\n Program exited successfully.")


def search_jobs(jobs, jobs_loc, num_jobs):
    """Searches for jobs on the Adzuna jobs platform.

    Args:
        jobs (str): The job title to search for.
        jobs_loc (str): The location to search for jobs in.
        num_jobs (int): The number of job results to return.

    Returns:
        list: A list of job results, where each job result is a dictionary containing information about the job.
    """

    # Load the Adzuna API credentials from the .env file
    load_dotenv()

    APP_ID = os.getenv("APP_ID")
    API_KEY = os.getenv("API_KEY")

    # Construct the Adzuna API URL
    API_URL = f"http://api.adzuna.com/v1/api/jobs/us/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page={num_jobs}&what={jobs}&where={jobs_loc}"

    # Make a GET request to the Adzuna API
    response = requests.get(API_URL)

    # Check the response status code
    if response.status_code == 200:
        # If the response status code is 200, then the request was successful
        # Get the JSON data from the response
        job_data = response.json()

        # Return the list of job results
        return job_data["results"]

    else:
        # If the response status code is not 200, then the request failed
        # Return None
        return None


def store_jobs_in_csv(jobs, jobs_loc, num_jobs):
    """Stores the job results in a CSV file.

    Args:
        jobs (str): The job title to search for.
        jobs_loc (str): The location to search for jobs in.
        num_jobs (int): The number of job results to return.

    Returns:
        str: A message indicating whether the job results were successfully
            appended to the CSV file, or if the CSV file was created and the
            job results were saved to it. If no job results were found, then
            a message indicating this is returned.
    """

    job_results = search_jobs(jobs, jobs_loc, num_jobs)

    if job_results:
        # Get the script directory and the jobs folder path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, "jobs")

        # Create the jobs folder if it does not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Construct the base filename for the CSV file
        base_filename = f"{jobs}_{jobs_loc}.csv"
        base_filename = base_filename.replace(" ", "_")

        # Construct the full path to the CSV file
        file_path = os.path.join(folder_path, base_filename)

        # Check if the CSV file exists
        file_exists = os.path.exists(file_path)

        # If the CSV file does not exist, create it and write the header row
        if not file_exists:
            with open(file_path, "w", newline="", encoding="utf8") as file:
                writer = csv.writer(file)
                writer.writerow(["Job Title", "Company", "Location"])

        # Append the job results to the CSV file
        with open(file_path, "a", newline="", encoding="utf8") as file:
            writer = csv.writer(file)
            for job in job_results:
                writer.writerow(
                    [
                        job["title"],
                        job["company"]["display_name"],
                        job["location"]["display_name"],
                    ]
                )

        # Determine the appropriate message to return based on whether the
        # CSV file existed before the function was called
        if file_exists:
            return f"Job listings appended to {base_filename}."
        else:
            return f"Job listings saved to {base_filename}."

    else:
        # If no job results were found, return a message indicating this
        return f"No job listings found."


def open_jobs_csv():
    """Opens the job listings CSV file specified by the user.

    Returns:
        str: The contents of the job listings CSV file, or a message indicating
            that the file does not exist or is empty.
    """

    # Get the script directory and the jobs folder path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "jobs")

    if not os.path.exists(folder_path):
        return 'No jobs folder found'
    
    else:
        # Get a list of all the files in the jobs folder
        files = os.listdir(folder_path)

        # Initialize a counter to track the index of each file in the list
        counter = 1

        # Check if there are any files in the jobs folder
        if not files:
            # If there are no files in the jobs folder, return a message indicating this
            return "No files in the folder"

        else:
            # Iterate over the list of files in the jobs folder
            for file in files:
                # Check if the file is a regular file
                if os.path.isfile(os.path.join(folder_path, file)):
                    # Get the file name and extension
                    file_name, file_extension = os.path.splitext(file)

                    # Print a list of all the job listings CSV files, with the index number of each file
                    print(f"  [{counter}] {file_name}")
                    counter += 1

            # Print a separator
            print("==============================================================")

            # Prompt the user to enter the index of the file to open
            user_choice = input(" Enter the index of the file to open (or 'q' to quit): ")

            # If the user enters "q", exit the program
            if user_choice.lower() == "q":
                sys.exit("\n Program exited successfully.")

            else:
                # Try to convert the user's choice to an integer
                try:
                    index = int(user_choice)

                    # Check if the index is within the range of valid indices
                    if 1 <= index <= len(files):
                        # Get the full path to the selected file
                        selected_file = os.path.join(
                            folder_path, files[index - 1]
                        )  # Adjusted index

                        # Open the selected file in read mode
                        with open(selected_file, "r", encoding="utf8") as file:
                            # Create a CSV reader object
                            reader = csv.reader(file)

                            # Read the entire contents of the CSV file into a list
                            table_data = list(reader)

                        # Check if the CSV file is empty
                        if table_data:
                            # Get the headers and data from the CSV file
                            headers = table_data[0]
                            data = table_data[1:]

                            # Return the tabulate() formatted contents of the CSV file
                            return tabulate(data, headers=headers, tablefmt="heavy_grid")

                        else:
                            # If the CSV file is empty, return a message indicating this
                            return "The CSV file is empty"

                    else:
                        # If the index is not within the range of valid indices, return a message indicating this
                        return "Invalid index."

                except ValueError:
                    # If the user's choice is not an integer, return a message indicating this
                    return "Invalid input. Please enter a valid index or 'q' to quit."


if __name__ == "__main__":
    main()