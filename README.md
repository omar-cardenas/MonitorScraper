# MonitorScraper

This program scapes monitor data from a retail website and finds the best prices for each panel type and resolution.

## Features
- scrapes webpage and stores data in a SQLite database.
- categorizes and displays data through a web app with direct links for purchase.
- script is automated using crontab to keep information up to date.

### Output options:
- Can display data by printing out the database contents, creating pandas dataframe, or exporting data to a csv file.
- Can view the two best prices for every panel type and resolution in the Flask web application.

### Crontab command:
Directions for automating script every 12 hours. 
- Open terminal 
- enter: crontab -e
- enter: 0 */12 * * * [pythonPath] [scriptPath] >> [output_filePath]
- save and quit

Verify by typing crontab -l in the terminal

### How to Run the Project
Clone the repository: git clone https://github.com/omar-cardenas/MonitorScraper.git

## Technologies Used
- **Language**: Python, HTML, CSS
- **Database**: SQLite

## License
This project is licensed under the MIT License.
