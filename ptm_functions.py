import json
import os


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
            line = line + " Not done"
        else:
            line = line + " Done"
        print(line, "\n")


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


# Creates new task
def new_task(command):
    # Task created as dict
    task_name = command[1]
    dtask = {
        "task_name": task_name,
        "is_done": False
    }

    # Loads file as dict
    with open("tasks.json") as f:
        dtasks = json.loads(f.read())

    # Appends new task to file as dict
    dtasks['tasks'].append(dtask)

    # Writes new file as dict to file
    jtasks = json.dumps(dtasks, indent=2)
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
