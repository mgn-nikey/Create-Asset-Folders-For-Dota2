#!/usr/bin/env python3
#v1.1

import os
import sys
import csv
import ctypes
import shutil
import winreg as wrg 
from win32com.client import Dispatch

#-----------------------------------var--------------------------------------------------------

rows = []
slots = []
empty_files_slots = []
empty_files_pipeline = []
empty_files_redacted = []
file_path_check = []
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

if sys.argv[1] in ("First", "Uninstall"):
    REG_PATH = r"Directory\\Background\\shell\\" #Путь KEY
    REG_KEY1 = "Create Asset Folders" #KEY
    REG_KEY = "command" #KEY
    REG_VALUE = "" #Default Value
    REG_BAT_PATH = os.path.join(launcher_path,'Create Asset Folders.bat "%V"') #Bat file path

#-----------------------------------functions---------------------------------------------------

def create_files(sl, empty):
    empty_files_redacted = [slot_word.replace('SLOT', slot) for slot_word in empty]
    for empty_file in empty_files_redacted: #Создаем пустые файлы с неймингом
        if os.path.exists(os.path.join(call_folder, sl, empty_file)) == False:
            if '/' in empty_file:
                empty_file = empty_file.replace("/","\\")
            if '\\' in empty_file:
                file_path_check = empty_file.strip().split('\\')
                file_path_check = file_path_check[ : -1]
                if os.path.exists(os.path.join(call_folder, sl, *file_path_check)) == False:
                    os.makedirs(os.path.join(call_folder, sl, *file_path_check)) #MKDIRS
            if os.path.exists(os.path.join(call_folder, sl, empty_file)) == False:
                open(os.path.join(call_folder, sl, empty_file), 'w').close()

#-----------------------------------main-------------------------------------------------------

if sys.argv[1] not in ("First", "Uninstall"): #Если запуск из файла Create Asset Folders.bat

    with open(pipeline_file, 'r') as pipeline: #Открываем файл с Папками
        lines = pipeline.readlines()
        pipeline_folders = lines[10].strip().split(',') #Делим строку по запятым и раскидываем в массив (pipeline_folders) Папки пайплайна в папке вызова меню
        additional_slot_folders = lines[2].strip().split(',') #Делим строку по запятым и раскидываем в массив (additional_slot_folders) Папки которые нужно создать в каждом слоте
        empty_files_slots = lines[6].strip().split(',') #Пустые файлы в папках слотов
        empty_files_pipeline = lines[14].strip().split(',') #Пустые файлы в папках пайплайна
        if lines[18]:
            test_textures_folder = lines[18].strip() #Папка с текстурами которые нужно скопировать
        if lines[22]:
            dota_folder = lines[22].strip() #Папка dota 2 beta
        
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
            if os.path.isdir(os.path.join(call_folder, slot)) == False:
                os.mkdir(os.path.join(call_folder, slot)) #MKDIR
            for additional_slot_folder in additional_slot_folders:
                if os.path.isdir(os.path.join(call_folder, slot, additional_slot_folder)) == False:
                    os.mkdir(os.path.join(call_folder, slot, additional_slot_folder)) #MKDIR
            create_files(slot, empty_files_slots)  

    if pipeline_folders:
        for pipeline_folder in pipeline_folders: #Создаем основные папки
            if '/' in pipeline_folder:
                pipeline_folder = pipeline_folder.replace("/","\\")
            if os.path.isdir(os.path.join(call_folder, pipeline_folder)) == False:       
                os.makedirs(os.path.join(call_folder, pipeline_folder)) #MKDIR
            if test_textures_folder:
                if os.path.exists(test_textures_folder):
                    if any("Test" in pipeline_folder for s in pipeline_folders): #Копируем текстуры если есть папка
                        if any("Texture" in pipeline_folder for s in pipeline_folders):
                            shutil.copytree(test_textures_folder, pipeline_folder, dirs_exist_ok=True)


    if empty_files_pipeline:
        for files_pipeline in empty_files_pipeline:
            if("SLOT" in files_pipeline):
                for slot in slots:
                    create_files("", empty_files_pipeline)
            else:
                create_files("", empty_files_pipeline)    
            

    dota_bin_folder = os.path.join(dota_folder, "game", "bin", "win64") #Путь dota bin
    workshop_shortcut = os.path.join(call_folder, "Workshop folder shortcut.lnk") #Путь ярлыка
    workshop_shortcut_icon = os.path.join(launcher_path, "icons", hero + ".ico") #Путь иконки
    items_folder = os.path.join(dota_folder, "content", "dota_addons", "workshop_testbed", "materials", "models", "items", hero) #Папка items

    if slots: #Создаем ярлык в папку items
        if os.path.exists(dota_folder):
            if os.path.isdir(items_folder) == False:
                os.mkdir(items_folder) #MKDIR
            while os.path.isdir(items_folder):
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(workshop_shortcut)
                shortcut.Targetpath = (items_folder)
                shortcut.IconLocation = (workshop_shortcut_icon)
                shortcut.save()  
                break

#-----------------------------------regedit----------------------------------------------------

if sys.argv[1] == "First": #Если запуск из файла First setup.bat
    try:
        location = wrg.HKEY_CLASSES_ROOT 
        soft = wrg.OpenKeyEx(location, REG_PATH) 
        key_1 = wrg.CreateKey(soft, REG_KEY1) 
        if key_1: 
            wrg.CloseKey(key_1) 
            REG_PATH = REG_PATH + REG_KEY1 + "\\"
        soft = wrg.OpenKeyEx(location, REG_PATH) 
        key_2 = wrg.CreateKey(soft, REG_KEY) 
        if key_2:
            wrg.SetValueEx(key_2, REG_VALUE, 0, wrg.REG_SZ, REG_BAT_PATH) 
            wrg.CloseKey(key_2) 
    except:
        ctypes.windll.user32.MessageBoxW(0, u"Run First setup as Admin", u"Error", 0)

if sys.argv[1] == "Uninstall": #Если запуск из файла Uninstall.bat
    try:
        location = wrg.HKEY_CLASSES_ROOT 
        soft = wrg.OpenKeyEx(location, REG_PATH) 
        key_1 = wrg.CreateKey(soft, REG_KEY1) 
        key_2 = wrg.CreateKey(soft, REG_KEY1) 
        if key_2: 
            REG_PATH = REG_PATH + REG_KEY1 + "\\"
            soft = wrg.OpenKeyEx(location, REG_PATH) 
            key_2 = wrg.CreateKey(soft, REG_KEY) 
            del_key = wrg.DeleteKey(key_2, "") 
            wrg.CloseKey(key_2) 
        if key_1: 
            del_key = wrg.DeleteKey(key_1, "") 
            wrg.CloseKey(key_1) 
    except:
        ctypes.windll.user32.MessageBoxW(0, u"Run First setup as Admin", u"Error", 0)

#-----------------------------------end-------------------------------------------------------