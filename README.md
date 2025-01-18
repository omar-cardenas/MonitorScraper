# MonitorScraper

This program scapes monitor data from a retail website and finds the best prices for each panel type and resolution.

## Features
- scrapes webpage and store data in a SQLite database
- display data with pandas or through a webpage created with Flask
- script is automated using crontab


### Output options:
- Can display data by printing out the database contents, creating pandas dataframe, or displaying webpage.

### Crontab command:
Directions for automating script every 12 hours
- Open terminal 
- enter: crontab -e
- enter: 0 */12 * * * <python path> <script path> >> <output_file path>
- save and quit

Verify by typing crontab -l in the terminal

## Technologies Used
- **Language**: Python, HTML, CSS
- **Database**: SQLite

## License
This project is licensed under the MIT License.
