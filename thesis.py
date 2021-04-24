#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title           :thesis.py
# description     :This program displays an interactive menu on CLI
# for controlling Speaker Recognition System
# author          :Bui Chi Dung - Chu Nguyen Duc
# date            :
# version         :0.1
# usage           :python menu.py
# notes           :
# python_version  :2.7.6
# =======================================================================

# Import the modules needed to run the script.
import sys, os

# Main definition - constants
menu_actions = {}

# Path

my_path = "D:\Thesis\Speaker-Recognition-Using-Raspberry-PI"


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('cls')

    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Enrollment")
    print("2. Delete Data")
    print("3. Verification")
    print("4. Configuration")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    os.system('cls')
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


# Enrollment menu
def enrollment_menu(choice):
    os.system('cls')
    ch = choice.lower()
    if ch == '':
        menu_actions['1']()
    else:
        try:
            # Gia su, trong dir hien hanh cua chuong trinh co folder input, chua cac file enroll 001, 002, 003 ...
            exc_extract = ch.split(' ')[0]

            if len(exc_extract) == 2 and exc_extract == 'extract.sh':
                os.system(exc_extract)
            else:
                menu_actions['1']()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


# Menu 1
def enrollment():
    print("Enrollment !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    enrollment_menu(choice)
    return


# Menu 2
def delete():
    print("Delete Data !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 3
def verify():
    print("Verification !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
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
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()