import os
import csv
import mock

from tabulate import tabulate
from project import search_jobs, store_jobs_in_csv, open_jobs_csv


def test_search_jobs():
    # Create a mock jobs variable
    jobs = "Software Engineer"
    # Create a mock jobs_loc variable
    jobs_loc = "Mountain View, CA"
    # Create a mock num_jobs variable
    num_jobs = 10

    # Mock the requests.get() function to return a 404 error
    with mock.patch("requests.get") as mock_get:
        # Determine the expected result
        expected_result = (
            job_results if mock_get.return_value.status_code == 200 else None
        )

        # Call the search_jobs function
        job_results = search_jobs(jobs, jobs_loc, num_jobs)

        # Assert that the job_results variable matches the expected result
        assert job_results == expected_result


def test_store_jobs_in_csv():
    # create a mock job variable
    job = "Software Engineer"
    # Create a mock jobs_loc variable
    jobs_loc = "Mountain View, CA"
    # Create a mock num_jobs variable
    num_jobs = 10

    # Check if the file exists
    file_path = os.path.join("jobs", "Software_Engineer_Mountain_View,_CA.csv")
    if os.path.exists(file_path):
        # The file already exists, so assert that the result is "Job listings appended..."
        result = store_jobs_in_csv(job, jobs_loc, num_jobs)
        assert (
            result
            == "Job listings appended to Software_Engineer_Mountain_View,_CA.csv."
        )
    else:
        # The file does not exist, so assert that the result is "Job listings saved..."
        result = store_jobs_in_csv(job, jobs_loc, num_jobs)
        assert (
            result == "Job listings saved to Software_Engineer_Mountain_View,_CA.csv."
        )

    # Assert that the file exists
    assert os.path.exists(file_path)


def test_open_jobs_csv():
    """Test the open_jobs_csv() function."""

    # Create a mock folder path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "jobs")

    # Create a mock CSV file
    with open(
        os.path.join(folder_path, "Software_Engineer_Mountain_View,_CA.csv"),
        "w",
        encoding="utf8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location"])
        writer.writerow(["Software Engineer", "Google", "Mountain View, CA"])

    # Mock the input() function to return "10"
    with mock.patch("builtins.input", return_value="10"):
        # Call the open_jobs_csv() function
        result = open_jobs_csv()

        # Assert that the result is "Invalid index."
        assert result == "Invalid index."

    # Mock the input() function to return "1"
    with mock.patch("builtins.input", return_value="1"):
        # Call the open_jobs_csv() function
        result = open_jobs_csv()

        # Assert that the result is the expected CSV file contents
        assert result == tabulate(
            [["Software Engineer", "Google", "Mountain View, CA"]],
            headers=["Job Title", "Company", "Location"],
            tablefmt="heavy_grid",
        )