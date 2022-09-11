# Timetable to Calendar
A Python application that utilises Selenium & Google Calendar's API to log in and scrape my UWE timetable and display it on Google Calendar as well as other services e.g. Apple's Calendar. 

---
## Setup
**Mac OS**
- Clone the repository.
- Run `pip install -r requirements.txt`.
- Create an empty CSV named `schedule.csv` if does not already exist.
- Create a new project on [Google Cloud Console](https://console.cloud.google.com/).
- Create credentials and save as `credentials.json`.
A guide on this process can be found [here](https://developers.google.com/workspace/guides/create-credentials#desktop-app).
- Create a `.env` file with the following layout. 
    ```
    EMAIL=MyUWEemail
    PASSWORD=MyUWEpassword
    ```
**Other OS**
- Follow steps for Mac OS.
- Change the Selenium Webdriver to Chrome, Edge or Firefox. 
    For additional information on this, refer to the [documentation section 1.5](https://selenium-python.readthedocs.io/installation.html).

## Usage
- Ensure `credentials.json`, `schedule.csv` & `.env` are in the same directory as `main.py`.
- Run `main.py`, you'll be prompted to log into your application but this will be saved in a newly generated file, `token.json`.