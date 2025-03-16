# MonitorScraper

This program scapes monitor data from a retail website and finds the best prices for each panel type and resolution.

### Features
---
- scrapes webpage and stores data in a SQLite database.
- categorizes and displays data through a web app with direct links for purchase.
- lets you display monitors by resolution and panel type.
- script is automated using crontab to keep information up to date.

### Output options  
---
- Can print out database contents, create pandas dataframe, or export data to a csv file.
- Can view the best prices for every panel type and resolution by running the web application.

<img width="800"  alt="Web app" src="https://github.com/user-attachments/assets/9bf0dba3-4adf-4c12-8bed-0a744abc4418" />
<img width="800"  alt="CSV file" src = "https://github.com/user-attachments/assets/f596f6f4-0216-4bc4-9160-c60796976955" />


##


### Crontab command  
---
Directions for automating script every 12 hours. 
- Open terminal 
- enter: crontab -e
- enter: 0 */12 * * * [pythonPath] [scriptPath] >> [output_filePath]
- save and quit

Verify by typing crontab -l in the terminal

### How to Run the Project
---
Clone the repository: git clone https://github.com/omar-cardenas/MonitorScraper.git

### Technologies Used
---
- **Language**: Python, HTML, CSS, JavaScript
- **Database**: SQLite

### License
---
This project is licensed under the MIT License.
