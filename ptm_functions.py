import json
import os
from calendar_feature import esc


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
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    for index, task in enumerate(dtasks['tasks'], start=1):
        line = "[" + str(index) + "] " + task['task_name'] + " "
        line = line + (75 - len(line))*"."
        if not task['is_done']:
            line = line + esc(91) + " Not done" + esc(0)
        else:
            line = line + esc(92) + " Done" + esc(0)
        print(line, "\n")


# Help information
def cmd_help():
    print("-"*55)
    print("new", "."*7, "Creates new task; Delimit multiple tasks with '\\'\n\t", end="")
    print(r"'new [task 1 name] [\] [task 2 name] ...'", end="\n\n")
    print("edit", "."*6, "Edits existing task\n\t", r"'edit [task index] [new task name]'", end="\n\n")
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


# Creates new tasks
def new_task(command):
    # Tasks created as list of dicts
    task_names = command[1]
    task_names = task_names.split('\\')
    dtasks = []
    for task_name in task_names:
        dtasks.append(
            {
                "task_name": task_name,
                "is_done": False
            }
        )

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
