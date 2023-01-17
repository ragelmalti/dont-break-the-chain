# 'Don't break the chain' habit tracker
# Made by Julian
# CSV Layout: id, habit, date, chains, record
import pandas as pd
from datetime import date
from datetime import datetime
import os
import sys

HABITS_FILE = 'habits.csv'

def check_for_file():
    fileExist = os.path.isfile(HABITS_FILE)
    if fileExist:
        return True
    else:
        print("Error, 'habits.csv' not found. Creating file now.")
        with open('habits.csv', 'w') as creating_new_file:
            creating_new_file.write('HABIT,DATE,CHAINS,RECORD\n')
        return False

def read_habits():
    df = pd.read_csv(HABITS_FILE)
    rows = df.shape[0]
    if rows == 0:
        print("Error, no habits found")
        return
    else:
        for index in df.index:
            dt = str(df['DATE'][index])
            if dt != "0":
                dt = datetime.strptime(dt, "%Y-%m-%d")
                today_dt = datetime.combine(date.today(), datetime.min.time())
                delta = today_dt - dt
                if delta.days >= 2:
                    reset_chain(index, False)
                    df = pd.read_csv(HABITS_FILE)

            print(f"{index + 1}. {df['HABIT'][index]} | Record: {df['RECORD'][index]}")
            print(f"({df['CHAINS'][index]})", end=" ")
            print(int(df['CHAINS'][index]) * "*")
            print()

def create_new_habit(habit_name):
    # num_of_entries = 0
    # with open(HABITS_FILE, 'r') as csvfile:
    #     num_of_entries = len(csvfile.readlines())

    habit = f"{habit_name},0,0,0\n"

    with open(HABITS_FILE, 'a') as csvfile:
        csvfile.write(habit)

def delete_habit(habit_number):
    df = pd.read_csv(HABITS_FILE)
    while True:
        print(df.loc[habit_number, 'HABIT'])
        print(f"Number of chains: {df.loc[habit_number, 'CHAINS']} | Record: {df.loc[habit_number, 'RECORD']}")
        answer = input("Are you sure you want to delete habit? [Y/n] ")
        if str.upper(answer) == 'Y':
            df = df.drop(habit_number)
            df.to_csv(HABITS_FILE, index=False)
            return
        elif str.upper(answer) == 'N':
            return

def add_to_chain(habit_number : int):
    df = pd.read_csv(HABITS_FILE)
    df.loc[habit_number, "CHAINS"] = int(df.loc[habit_number, "CHAINS"]) + 1
    today = date.today()
    df.loc[habit_number, "DATE"] = str(today)

    if int(df.loc[habit_number, "CHAINS"]) >= int(df.loc[habit_number, "RECORD"]):
        df.loc[habit_number, "RECORD"] = int(df.loc[habit_number, "CHAINS"])
    df.to_csv(HABITS_FILE, index=False)

    print(df.loc[habit_number, 'HABIT'])
    print(f"Number of chains: {df.loc[habit_number, 'CHAINS']} | Record: {df.loc[habit_number, 'RECORD']}")

def reset_chain(habit_number : int, add_to_chain : bool):
    df = pd.read_csv(HABITS_FILE)
    dt = str(df.loc[habit_number, "DATE"])
    today = date.today()
    if add_to_chain == True:
        df.loc[habit_number, "CHAINS"] = 1
        df.loc[habit_number, "DATE"] = str(today)
    else:
        df.loc[habit_number, "CHAINS"] = 0
        df.loc[habit_number, "DATE"] = 0
    df.to_csv(HABITS_FILE, index=False)
    pass

def check_date(habit_number : int):
    df = pd.read_csv(HABITS_FILE)
    dt = str(df.loc[habit_number, "DATE"])
    today = date.today()
    if dt == "0":
        df.loc[habit_number, "DATE"] = str(today)
        df.to_csv(HABITS_FILE, index=False)
        print("Succesfully added to the chain!")
        add_to_chain(habit_number)
        return
    else:
        today_dt = datetime.combine(date.today(), datetime.min.time())
        dt = datetime.strptime(dt, "%Y-%m-%d")
        delta = today_dt - dt
        if delta.days == 0:
            print("Already added to the chain for today!")
            print(df.loc[habit_number, 'HABIT'])
            print(f"Number of chains: {df.loc[habit_number, 'CHAINS']} | Record: {df.loc[habit_number, 'RECORD']}")
        elif delta.days == 1:
            print("Succesfully added to the chain!")
            add_to_chain(habit_number)
        elif delta.days >= 2:
            print("You have broken the chain...")
            print(df.loc[habit_number, 'HABIT'])
            print(f"Number of chains: 1 | Record: {df.loc[habit_number, 'RECORD']}")
            reset_chain(habit_number, True)
        return
    pass

def main():
    if len(sys.argv) == 1:
        read_habits()
    elif len(sys.argv) >= 2:
        if sys.argv[1] == "list":
            read_habits()
        elif sys.argv[1] == "new" and len(sys.argv) == 3:
            create_new_habit(sys.argv[2])
        elif sys.argv[1] == "add" and len(sys.argv) == 3:
            try:
                item = int(sys.argv[2]) - 1
                check_date(item)
            except ValueError: 
                print("Error, argument must be a number")
        elif sys.argv[1] == "delete" and len(sys.argv) == 3:
            try:
                item = int(sys.argv[2]) - 1
                delete_habit(item)
            except ValueError: 
                print("Error, argument must be a number")

        else:
            print("Error, invalid arguments")
    else:
        print("Error, invalid arguments")

if __name__ == "__main__":
    if check_for_file():
        main()
    else:
        pass
    
