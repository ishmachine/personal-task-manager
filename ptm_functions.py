# FIXME: The first line is still fucked up during the very first iteration of the while loop
import json
import os
import time
from datetime import date
os.system("")


# For ANSI escape sequences
# Refer to https://en.wikipedia.org/wiki/ANSI_escape_code
def esc(code):
    return f'\033[{code}m'


# For use in main
def sleep():
    time.sleep(3)


# Clears the screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Returns task indices
def task_indices():
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())
    tasks = []
    for task in dtasks["tasks"]:
        tasks.append(task["task_name"])
    return list(list(zip(*list(enumerate(tasks, start=1))))[0])


# Displays tasks
def display():
    # The task part of the line
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    current_date = date.today()
    task_lines = []
    for index, task in enumerate(dtasks['tasks'], start=1):
        task_line = "[" + str(index) + "] " + task['task_name'] + " "
        if task["due_date"] is None:
            task_line = task_line + (75 - len(task_line))*"."
        else:
            task_line = task_line + (62 - len(task_line))*"."
            if date.fromisoformat(task["due_date"]) > current_date or task["is_done"]:
                task_line = task_line + esc(92)
            elif date.fromisoformat(task["due_date"]) == current_date:
                task_line = task_line + esc(93)
            elif date.fromisoformat(task["due_date"]) < current_date:
                task_line = task_line + esc(91)
            task_line = task_line + " " + task["due_date"] + esc(0) + ", "
        if not task['is_done']:
            task_line = task_line + esc(91) + " Not done" + esc(0) + " | "
        else:
            task_line = task_line + esc(92) + " Done" + esc(0) + " "*4 + " | "                    # Length of 96
        task_lines.append(task_line)

    # The calendar part of the line
    def feb_days(year):
        if year % 4 == 0:
            return list(range(1, 30))
        else:
            return list(range(1, 29))

    due_dates = []
    for task in dtasks["tasks"]:
        if task["due_date"] is not None:
            due_dates.append(date.fromisoformat(task["due_date"]))

    # For strftime guide, go to https://strftime.org/
    current_month_str = time.strftime("%B")
    current_day = time.strftime("%d")
    current_year = time.strftime("%Y")
    calendar_year_struct = {
        "January": (list(range(1, 32)), 1),
        "February": (feb_days(int(current_year)), 2),
        "March": (list(range(1, 32)), 3),
        "April": (list(range(1, 31)), 4),
        "May": (list(range(1, 32)), 5),
        "June": (list(range(1, 31)), 6),
        "July": (list(range(1, 32)), 7),
        "August": (list(range(1, 32)), 8),
        "September": (list(range(1, 31)), 9),
        "October": (list(range(1, 32)), 10),
        "November": (list(range(1, 31)), 11),
        "December": (list(range(1, 32)), 12)
    }
    weekdays = "Su\tM\tT\tW\tTh\tF\tS"

    calendar_head = []

    spaces = int(len(weekdays) - len(current_month_str))
    calendar_head.append(str(" "*spaces + esc(1) + current_month_str + esc(0)))
    calendar_head.append(str(esc(94) + weekdays + esc(0)))
    # Creation of the 7x6 2D list which will contain days
    calendar_body = []
    for i in range(0, 6):
        temp = []
        for j in range(0, 7):
            temp.append(' ')
        calendar_body.append(temp)

    i = 1
    initial_pos = (0, date(int(current_year), calendar_year_struct[current_month_str][1], 1).isoweekday())
    begin_replace = False   # Sets the start and end of the for loop
    for row_index, row in enumerate(calendar_body):
        for col_index, col in enumerate(row):
            if (row_index, col_index) == initial_pos:
                begin_replace = True
            if i == calendar_year_struct[current_month_str][0][-1] + 1:
                begin_replace = False
            if begin_replace:
                if i == int(current_day):
                    calendar_body[row_index][col_index] = esc(47) + esc(30) + str(i) + esc(0)
                else:
                    day_to_add = date(int(current_year), calendar_year_struct[current_month_str][1], i)
                    if day_to_add in due_dates:
                        if day_to_add < date.today():
                            calendar_body[row_index][col_index] = esc(101) + esc(30) + str(i) + esc(0)
                        elif day_to_add > date.today():
                            calendar_body[row_index][col_index] = esc(102) + esc(30) + str(i) + esc(0)
                    else:
                        calendar_body[row_index][col_index] = str(i)
                i += 1

    calendar = [calendar_head[0], calendar_head[1]]
    for week in calendar_body:
        calendar.append("\t".join(week))

    # Now to fill the empty space underneath the tasks if there are less task rows than calendar rows
    if len(task_lines) < len(calendar):
        for i in range(len(task_lines), len(calendar)):
            task_lines.append(str(" "*85 + "| "))

    # Now to put it all together
    for i in range(0, len(calendar)):
        print(task_lines[i], calendar[i], sep="")
    if len(task_lines) > len(calendar):
        for j in range(i + 1, len(task_lines)):
            print(task_lines[j])
    print("-"*85)


# Help information
def cmd_help():
    print("-"*55)
    print("new", "."*7, "Creates new task; Delimit multiple tasks with '\\' and dates with '**'\n\t", end="")
    print(r"'new [task 1 name]**[yyyy-mm-dd][\][task 2 name]**[yyyy-mm-dd] ...'", end="\n\n")
    print("edit", "."*6, "Edits existing task name or date\n\t", end="")
    print(r"'edit [task index] [new task name]'", end="\n", sep="")
    print("\t\tor:\n\t'edit [task index] ** [new date]'", end="\n\n")
    print("del", "."*7, "Deletes existing task(s)\n\t", r"'del [task index]' or 'del all'", end="\n\n")
    print("done", "."*6, "Marks existing task as done or not done\n\t", r"'done [task index]'", end="\n\n")
    print("help", "."*6, "Displays command help dialog\n\t", r"'help'")
    print("-"*55)


# Collects command and continues to prompt until valid command is given,
# returns valid command in list form
def valid_command():
    # Collects command from user
    command = input("ptm > ")
    command = command.split(" ")

    # Parses and validates command
    valid_keys = [
        "new",
        "edit",
        "del",
        "done",
        "help",
        "exit"
    ]
    try:
        if command[0] in valid_keys:
            if command[0] == "new":
                if len(command) == 1:
                    print("Invalid number of arguments.", "\n")
                    return valid_command()
                else:
                    return [command[0], " ".join(command[1:])]
            elif command[0] == "edit":
                try:
                    if int(command[1]) in task_indices():
                        if command[2] == "**" and len(command) == 4:
                            return command
                        else:
                            return [command[0], command[1], " ".join(command[2:])]
                    else:
                        print("Invalid index.", "\n")
                        return valid_command()
                except ValueError:
                    print("Invalid index.", "\n")
                    return valid_command()
            elif command[0] == "del" or "done":
                if len(command) > 2:
                    print("Invalid number of arguments.", "\n")
                    return valid_command()
                else:
                    if command[1] == "all":
                        return command
                    else:
                        try:
                            if int(command[1]) in task_indices():
                                return command
                            else:
                                print("Invalid index.", "\n")
                                return valid_command()
                        except ValueError:
                            print("Invalid index.", "\n")
                            return valid_command()
        else:
            print("Invalid key.", "\n")
            return valid_command()
    except IndexError:
        if command[0] == "exit":
            exit()
        elif command[0] == "help":
            cmd_help()
            return valid_command()


def date_parser(date_string):
    try:
        return str(date.fromisoformat(date_string))
    except ValueError:
        print("Invalid due date was skipped.")
        time.sleep(3)
        return None


# Creates new tasks
def new_task(command):
    # Tasks created as list of dicts
    task_names = command[1]
    task_names = task_names.split('\\')
    dtasks = []
    over_char_limit = False
    for task_name in task_names:
        if len(task_name.split("**")[0]) > 50:
            over_char_limit = True
        else:
            if len(task_name.split("**")) == 2:
                due_date = date_parser(task_name.split("**")[1])
            elif len(task_name.split("**")) == 1:
                due_date = None
            else:
                print("Too many delimiters. A due date was skipped.")
                due_date = None
            dtasks.append(
                {
                    "task_name": task_name.split("**")[0],
                    "is_done": False,
                    "due_date": due_date
                }
            )
    if over_char_limit:
        print("One or more of your tasks were skipped because they exceeded the 50 character limit.")
        time.sleep(3)

    # Loads file as dict
    with open("tasks.json") as f:
        file_dtasks = json.loads(f.read())

    # Appends new tasks to file as dict
    for dtask in dtasks:
        file_dtasks['tasks'].append(dtask)

    # Writes new file as dict to file
    jtasks = json.dumps(file_dtasks, indent=2)
    with open("tasks.json", "w") as f:
        f.write(jtasks)


# Edits task name
def edit_task(command):
    # Loads file as dict
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    # Edits tasks as dict
    if command[2] == "**" and len(command) == 4 and command[-1] != '':
        due_date = date_parser(command[3])
        if due_date is not None:
            dtasks['tasks'][int(command[1]) - 1]['due_date'] = due_date
        else:
            pass
    elif command[2] == "**" and len(command) == 4 and command[-1] == '':
        dtasks['tasks'][int(command[1]) - 1]['due_date'] = None
    else:
        if len(command[2]) > 50:
            print("Your edit exceeds the 50 character limit.")
            time.sleep(3)
        else:
            dtasks['tasks'][int(command[1]) - 1]['task_name'] = command[2]

    # Writes new file as dict to file
    jtasks = json.dumps(dtasks, indent=2)
    with open("tasks.json", "w") as f:
        f.write(jtasks)


# Deletes task
def del_task(command):
    # Loads file as dict
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    # Removes task from task as dict
    if command[1] == "all":
        dtasks['tasks'] = []
    else:
        dtasks['tasks'].remove(dtasks['tasks'][int(command[1]) - 1])

    # Writes new file as dict to file
    jtasks = json.dumps(dtasks, indent=2)
    with open("tasks.json", "w") as f:
        f.write(jtasks)


# Marks task as done or not done
# If task is marked done, it will change to not done
# If task is marked not done, it will change to done
def mark_done(command):
    # Loads file as dict
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    # Edits tasks as dict
    if dtasks['tasks'][int(command[1]) - 1]['is_done'] is False:
        dtasks['tasks'][int(command[1]) - 1]['is_done'] = True
    elif dtasks['tasks'][int(command[1]) - 1]['is_done'] is True:
        dtasks['tasks'][int(command[1]) - 1]['is_done'] = False

    # Writes new file as dict to file
    jtasks = json.dumps(dtasks, indent=2)
    with open("tasks.json", "w") as f:
        f.write(jtasks)
