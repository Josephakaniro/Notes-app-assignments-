A command line tool for folder and note creation and organization made with the python programming language 

The Tech Stack used in making this CLI tool were:
1. Typer : for creating the cli commands 
2. SQLAlchemy : Object relational mapping of Notes and folders
3. SQLite: Creation of a the database 
4. Tabulate : for analytics presentation
5. Json : Handling Json file input
6. CSV: Handling CSV file input

Features:
1. Create, Read & delete notes
2. Oragnizes notes in folders 
3. import JSON and CSV files
4. Analytics of Notes and folders

Installation:
Step 1:
Clone the repository into your device 
Step 2:
Create a virtual environment 
Step 3:
install the dependencies 

YOU ARE GOOD TO GO!!!!!

USAGE:
The CLI commands were made with the typer module so to run it :
python -m app.cli --help

*create a folder
  python -m app.cli new-folder --folder-name "Work"
*create a new note 
  python -m app.cli new-note --title "Meeting" --folder-name "Work" --body "Project kickoff at 10 AM"
*search for note 
  python -m app.cli search-note --title "Meeting"
*import json or csv 
  python -m app.cli import_json_notes --file-path"    "
  python -m app.cli import_csv_notes --file-path"    "
*analytics
  python -m app.cli folder-analytics
  python -m app.cli note-analytics

 

