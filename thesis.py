#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title           :thesis.py
# description     :This program displays an interactive menu on CLI
# for controlling Speaker Recognition System
# author          :Bui Chi Dung - Chu Nguyen Duc
# date            :
# version         :0.1
# usage           :python3 thesis.py
# notes           :
# python_version  :3.8.5
# =======================================================================

# Import the modules needed to run the script.
import sys, os
import subprocess
import toml
# Main definition - constants
menu_actions = {}

# Path

# Remember to change this path to your actual path where this file is located
cfg = toml.load("config.toml")
my_path = cfg["path"]


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')
    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Enrollment")
    print("2. Delete Data")
    print("3. Verification")
    print("4. Configuration")
    print("5. Format Data")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Execute Enrollment Menu
def enrollment_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['1']()
    else:
        try:
            # Gia su, trong dir hien hanh cua chuong trinh co folder input, chua cac file enroll 001, 002, 003 ...
            ch_split = ch.split(' ')
            if len(ch_split) == 2:
                exc_extract = ch_split[0]
                voice_id = ch_split[1]
                if exc_extract == 'enr':
                    os.system('./extract.sh '+voice_id)
                    # Successful message
                    # ...
            else:
                menu_actions['1']()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu enrollment
def enrollment():
    print("Enrollment !\n")
    # print("Use command 'enr <id>' to enroll your voice id!\n")
    id = gen_id()
    choice = 'enr {}'.format(id)
    os.system('arecord -r 16000 -d 5 -f S16_LE db/{}/wav/{}.wav'.format(id, id))
    enrollment_menu(choice)
    os.system('clear')
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    if choice.lower() == '9' or choice.lower() == '0':
        exec_menu(choice)
    # else:    
    #     enrollment_menu(choice)
    return


# Execute Verify Menu
def verify_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['3']()
    else:
        try:
            # In case you already know the ID in database, you want to verify this ID with the voice you input right now
            ch_split = ch.split(' ')
            if len(ch_split) == 3:
                exc_verify = ch_split[0]
                voice_id_db = ch_split[1]
                voice_id_input = ch_split[2]
                if exc_verify == 'ver':
                    # os.system('./verify.sh ' + voice_id_db + '  '+ voice_id_input)
                    os.system('./verify.sh ' +  voice_id_input)
            else:
                menu_actions['3']()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return    

# Menu vefify
def verify():
    print("Verification !\n")
    choice = str(input("Your ID: "))
    choice = 'ver input {}'.format(choice)
    print(choice)
    os.system('arecord -r 16000 -d 5 -f S16_LE input/wav/input.wav')
    verify_menu(choice)
    os.system('clear')
    # print("Use command 'ver <id_db> <id_input>' to verify your voice id!\n")
    print(get_result() + '\n')
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    if choice.lower() == '9' or choice.lower() == '0':
        exec_menu(choice)
    # else: 
    #     verify_menu(choice)
    return


# Execute Verify Menu
def delete_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['2']()
    else:
        try:
            # In case you already know the ID in database, you want to verify this ID with the voice you input right now
            ch_split = ch.split(' ')
            if len(ch_split) == 2:
                exc_delete = ch_split[0]
                voice_id_del = ch_split[1]
                if exc_delete == 'del':
                    print('Are you sure to delete ' + voice_id_del + ' ?(Y/N)')
                    confirm = input(" >>  ")
                    cf = confirm.lower()
                    if cf == 'Y' or 'y':
                        os.system('rm -rf ' + my_path + '/db' + '/' + voice_id_del)
                        # output = subprocess.Popen(['echo', '$(find 001)'], stdout=subprocess.PIPE ).communicate()[0]
                        print("Delete successfully! Please wait 2s to get back!")
                        os.system('sleep 2')
                        os.system('clear')
                    # else:
                    menu_actions['2']()
            else:
                menu_actions['2']()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return 

# Menu delete
def delete():
    print("Delete Data !\n")
    print("Use command 'del <id>' to delete your voice id!\n") 
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    if choice.lower() == '9' or choice.lower() == '0':
        exec_menu(choice)
    else:
        delete_menu(choice)
    return

# Execute Format Menu
def format_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['5']()
    else:
        try:
            # In case you already know the ID in database, you want to verify this ID with the voice you input right now
            ch_split = ch.split(' ')
            if len(ch_split) == 1:
                exc_format = ch_split[0]
                if exc_format == 'format':
                    print('Are you sure to format all your data ?(Y/N)')
                    confirm = input(" >>  ")
                    cf = confirm.lower()
                    if cf == 'Y' or 'y':
                        # Format db data enrollment
                        os.system('rm -rf ' + my_path + '/db')
                        os.system('mkdir db')
                        # Format input data (to verify)
                        os.system('rm -rf ' + my_path + '/input')
                        os.system('mkdir input')
                        # output = subprocess.Popen(['echo', '$(find 001)'], stdout=subprocess.PIPE ).communicate()[0]
                        print("Format successfully! Please wait 2s to get back!")
                        os.system('sleep 2')
                        os.system('clear')
                    # else:
                    menu_actions['5']()
            else:
                menu_actions['5']()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return 

# Menu format
def format_data():
    print("Format Data !\n")
    print("Use command 'format' to format all your data!\n") 
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    if choice.lower() == '9' or choice.lower() == '0':
        exec_menu(choice)
    else:
        format_menu(choice)
    return    


# Menu 4
def config():
    print("Configuration !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': enrollment,
    '2': delete,
    '3': verify,
    '4': config,
    '5': format_data,
    '9': back,
    '0': exit,
}

def gen_id():
    path = 'db'
    # num_spkr = len(os.listdir(path))
    list_ids = sorted(os.listdir(path))
    id = int(list_ids[-1])+1
    id = format(id, '03d')
    print(id)
    dest_path = os.path.join(path, id, 'wav')    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    return id

def get_result():
    f = open('results', 'r')
    res = f.readline()
    return res


# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
