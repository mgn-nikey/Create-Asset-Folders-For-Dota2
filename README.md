# Create Asset Folders for Dota 2 Workshop, and 3D pipeline
 
 This script creates tree of folders for Dota 2 Workshop, and 3D pipeline.
 
 ![example](https://i.imgur.com/I8dLviU.gif)
 
# First Setup

 Script requires [Python](https://www.python.org/downloads/)
 
 **!!!  IMPORTANT** ***When installing Python, checkbox "Add Python to PATH." must be checked.***
 
 Run [First Setup](First_setup.bat) file **as administrator**. 
 
 It will create reg key that allows script to run from right-click menu, and install 2 python modules to work correctly. 
 
 Now you can use script!

# How it works

 Folders could be created from right-click menu by clicking on 'Create Asset Folders' button.

 **All settings stored in [Pipeline Folders](pipeline_folders.csv).**
 
 Open [Pipeline Folders](pipeline_folders.csv) with notepad and follow instructions in the file.

 1. Creates pipeline folders listed in **row 11** from [Pipeline Folders](pipeline_folders.csv) file.
 
 2. If anything listed in [Pipeline Folders](pipeline_folders.csv) in **row 15**, creates empty files inside folders. 
	+ *The idea is to create empty files, which could be used for clean and consistent naming of files with format, and which will be re-written by working file later.*

 3. If 'Create Asset Folders' was launched from folder, which folder path contains Dota 2 hero name, 
 creates folder for each of his [slots](hero_and_slots.csv).
	+ *Slots of each hero is taken from official [requirements website](https://www.dota2.com/workshop/requirements/).*
	+ *If there's no hero name in folder path, it creates only pipeline folders.*
	
 4. If anything listed in [Pipeline Folders](pipeline_folders.csv) in **row 3**, creates folder inside each slot folder.
 
 5. If anything listed in [Pipeline Folders](pipeline_folders.csv) in **row 7**, creates empty files with needed file format inside each slot folder

 6. If path to "dota 2 beta folder" exists in **row 23** in [Pipeline Folders](pipeline_folders.csv), 
 creates shortcut to the 'dota2/items' folder for easy access. Shortcut uses hero icon from icons folder.

 7. If there's a Test/Texture folder in **row 11** in [Pipeline Folders](pipeline_folders.csv), it copies textures from **row 19** in [Pipeline Folders](pipeline_folders.csv) to that folder.
	+ *For Dota2 Workshop artists, blockout and highpoly tests with placeholder textures in the game.*

# Uninstalling button from right-click menu
	
 Run [Uninstall](Uninstall_button.bat) file **as administrator**. 