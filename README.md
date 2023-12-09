# Create Asset Folders for Dota 2 Workshop, and 3D pipeline
 
 This script creates tree of folders for Dota 2 Workshop, and 3D pipeline.
 
 If folder path, where script was running from right-click menu, contains Dota 2 hero name, it creates folder for each of his [slots](hero_and_slots.csv), and regular 3D pipeline folders.
 Slots of each hero is taken from official [requirements website](https://www.dota2.com/workshop/requirements/).
 
  - There's an option to create folder inside each slot folder. Must be written in row 3 in [Pipeline Folders](pipeline_folders.csv).
  - There's an option to create empty files with needed file format inside each slot folder, which could be used to keep same naming. Must be written in row 7 in [Pipeline Folders](pipeline_folders.csv).
  - List of pipeline folders must be written in row 11 in [Pipeline Folders](pipeline_folders.csv).
  - If there's no hero name in folder path, it creates only pipeline folders.
  - If there's a Test/Texture folder in row 11 in [Pipeline Folders](pipeline_folders.csv), it copies textures from row 15 in [Pipeline Folders](pipeline_folders.csv) to that folder.

 Also creates shortcut to dota2/items folder for easy access, dota 2 beta folder path must be written in row 19 in [Pipeline Folders](pipeline_folders.csv). Shortcut uses hero icon from icons folder.
 
# First Setup

 Script requires [Python](https://www.python.org/downloads/)
 
 Run [First Setup](First_setup.bat) file as administrator. 
 It will create reg key that allows script to run from right-click menu, and install 2 python modules to work correctly.
 
 Then folders could be created from right-click menu by clicking on 'Create Asset Folders' button.

# Pipeline folders setup

 Open [Pipeline Folders](pipeline_folders.csv) with notepad and follow instructions in the file.