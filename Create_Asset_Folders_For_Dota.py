#!/usr/bin/env python3

import os
import sys
import csv
import shutil
import winreg as wrg 
from win32com.client import Dispatch

#-----------------------------------var--------------------------------------------------------

rows = []
slots = []
empty_files = []
path_arrays = [] #Массив для деления на части пути через каждый "/" (путь папки откуда вызвано меню)
pipeline_folders = [] 
additional_slot_folders = []

path = sys.argv[0] #Путь файла питона
call_folder = sys.argv[1] #Путь откуда вызвали меню

path_arrays = call_folder.split(os.sep) #Заполнение массива путем деления пути (call_folder) откуда был вызов из меню
path_arrays = [x.replace(' ','_') for x in path_arrays]

parent_folder_name = os.path.basename(os.path.dirname(call_folder)) #ИМЯ РОДИТЕЛЬСКОЙ ПАПКИ ИЗ ВЫЗОВА (call_folder)

launcher_path = os.path.dirname(path)

pipeline_file = os.path.join(launcher_path,'pipeline_folders.csv')
heroes_file = os.path.join(launcher_path,'hero_and_slots.csv')

#-----------------------------------main-------------------------------------------------------

if sys.argv[1] != "First": #Если запуск из файла Create Asset Folders.bat

    with open(pipeline_file, 'r') as pipeline: #Открываем файл с Папками
        lines = pipeline.readlines()
        pipeline_folders = lines[10].strip().split(',') #Делим строку по запятым и раскидываем в массив (pipeline_folders) Папки пайплайна в папке вызова меню
        additional_slot_folders = lines[2].strip().split(',') #Делим строку по запятым и раскидываем в массив (additional_slot_folders) Папки которые нужно создать в каждом слоте
        empty_files = lines[6].strip().split(',') #Пустые файлы
        if lines[14]:
            test_textures_folder = lines[14].strip() #Папка с текстурами которые нужно скопировать
        if lines[18]:
            dota_folder = lines[18].strip() #Папка dota 2 beta

    with open(heroes_file,'r') as file: #Открываем файл с Героями
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
            for path_array in path_arrays:
                if row[0] == path_array.lower():
                    hero = row[0]
                    slots.append(row[1]) #Добавляем слоты в массив

    if slots: #Если в пути где вызвано меню есть герой, создаем папки слотов
        for slot in slots:
            empty_files = [slot_word.replace('SLOT', slot) for slot_word in empty_files]
            os.mkdir(os.path.join(call_folder, slot)) #MKDIR
            for additional_slot_folder in additional_slot_folders:
                os.mkdir(os.path.join(call_folder, slot, additional_slot_folder)) #MKDIR
            for empty_file in empty_files:
                open(os.path.join(call_folder, slot, empty_file), 'w').close()

    if pipeline_folders:
        for pipeline_folder in pipeline_folders: #Создаем основные папки
            os.mkdir(os.path.join(call_folder, pipeline_folder)) #MKDIR
            if test_textures_folder:
                if any("Test" in pipeline_folder for s in pipeline_folders): #Копируем текстуры если есть папка
                    if any("Texture" in pipeline_folder for s in pipeline_folders):
                        shutil.copytree(test_textures_folder, pipeline_folder, dirs_exist_ok=True)

    dota_bin_folder = os.path.join(dota_folder, "game", "bin", "win64") #Путь dota bin
    workshop_shortcut = os.path.join(call_folder, "Workshop folder shortcut.lnk") #Путь ярлыка
    workshop_shortcut_icon = os.path.join(launcher_path, "icons", hero + ".ico") #Путь иконки
    items_folder = os.path.join(dota_folder, "content", "dota_addons", "workshop_testbed", "materials", "models", "items", hero) #Папка items

    if slots: #Создаем ярлык в папку items
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(workshop_shortcut)
        shortcut.Targetpath = (items_folder)
        shortcut.IconLocation = (workshop_shortcut_icon)
        shortcut.save()

#-----------------------------------regedit----------------------------------------------------

if sys.argv[1] == "First": #Если запуск из файла First setup.bat

    REG_PATH = r"Directory\\Background\\shell\\Create Asset Folders\\" #Путь KEY
    REG_KEY = "command" #KEY
    REG_VALUE = "" #Default Value
    REG_BAT_PATH = os.path.join(launcher_path,'Create Asset Folders.bat "%V"') #Bat file path

    try:
        location = wrg.HKEY_CLASSES_ROOT 
        soft = wrg.OpenKeyEx(location, REG_PATH) 
        key_1 = wrg.CreateKey(soft, REG_KEY) 
        wrg.SetValueEx(key_1, REG_VALUE, 0, wrg.REG_SZ, REG_BAT_PATH) 
        if key_1: 
            wrg.CloseKey(key_1) 
    except:
        print(" Run First setup as Admin \n Run First setup as Admin \n Run First setup as Admin \n Run First setup as Admin \n Run First setup as Admin \n ")