import sys
import datetime
import uuid
import json

# Define colors
COLORS = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',  # Reset color
}

STATUS_COLORS = {
    'TODO': COLORS['RED'],
    'IN-PROGRESS': COLORS['YELLOW'],
    'DONE': COLORS['GREEN']
}

# Get arguments
arguments = sys.argv

# Add task
def add(arg):
    # Create task
    task = {
        "id":str(uuid.uuid4())[:8],
        "description":arg,
        "status":"TODO",
        "createdAt":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "updatedAt":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    # Read data
    try:
        with open('task.json','r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'tasks':[]}
    except json.JSONDecodeError:
        print('Error: Invalid JSON file')
        data = {'tasks':[]}

    # Add task to data
    data['tasks'].append(task)

    # Write data to file
    with open('task.json','w') as file:
        json.dump(data,file,indent=2)

# Update task
def update(id,new_value,flag):
    task_found = False
    status_values = ['TODO','IN-PROGRESS','DONE']
    flags = ['-s','-d']

    # Check if flag is valid
    if flag not in flags:
        return(False, "INVALID FLAG", None)

    # Check if status is valid
    if flag == '-s' and new_value not in status_values:
        return(False, "INVALID STATUS", None)
    
    # Check if description is valid
    if flag == '-d':
        if len(new_value) == 0:
            return (False, "DESCRIPTION CANNOT BE EMPTY", None)
    
    # Add file operation error handling
    try:
        with open('task.json','r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return (False, "INVALID JSON FILE", None)
    except FileNotFoundError:
        return (False, "FILE NOT FOUND", None)
    except PermissionError:
        return (False, "PERMISSION DENIED", None)
    except Exception as e:
        return (False, f"ERROR READING FILE: {str(e)}", None)

    # Update task
    for task in data['tasks']:
        if task['id'] == id:
            task_found = True
            if flag == "-s":
                task['status'] = new_value
                task['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
            elif flag == '-d':
                task['description'] = new_value
                task['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break

    # Check if task was found
    if not task_found:
        return((False, "NO TASK FOUND", None))

    # Add write operation error handling
    try:
        with open('task.json','w') as file:
            json.dump(data,file,indent=2)
    except PermissionError:
        return (False, "PERMISSION DENIED WHILE SAVING", None)
    except Exception as e:
        return (False, f"ERROR SAVING FILE: {str(e)}", None)

    return ((True, "TASK UPDATED SUCCESSFULLY", task))

# Delete task
def delete(id):
    task_found = False

    # Add file operation error handling
    try:
        with open('task.json','r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return (False, "INVALID JSON FILE", None)
    except FileNotFoundError:
        return (False, "FILE NOT FOUND", None)
    except PermissionError:
        return (False, "PERMISSION DENIED", None)
    except Exception as e:
        return (False, f"ERROR READING FILE: {str(e)}", None)
    
    # Delete task
    for i in range(len(data['tasks'])):
        if data['tasks'][i]['id'] == id:
            task_found = True
            deleted_task = data['tasks'].pop(i)
            break

    # Check if task was found
    if not task_found:
        return (False, "TASK NOT FOUND", None)
        
    # Add write operation error handling
    try:
        with open('task.json','w') as file:
            json.dump(data,file,indent=2)
    except PermissionError:
        return (False, "PERMISSION DENIED WHILE SAVING", None)
    except Exception as e:
        return (False, f"ERROR SAVING FILE: {str(e)}", None)
    
    return (True, "TASK DELETED SUCCESSFULLY", deleted_task)

    
# List tasks
def list_tasks(status=None):
    try:
        with open('task.json', 'r') as file:
            data = json.load(file)

        # Filter tasks if status provided
        if status:
            tasks = [task for task in data['tasks'] if task['status'] == status]
        else:
            tasks = data['tasks']

        # Print header with blue color
        if status:
            print(f"{COLORS['BLUE']}Total {status} tasks: {len(tasks)}{COLORS['RESET']}")
        else:
            print(f"{COLORS['BLUE']}Total tasks: {len(tasks)}{COLORS['RESET']}")

        # Print tasks with color-coded status
        for task in tasks:
            status_color = {
                'TODO': COLORS['RED'],
                'IN-PROGRESS': COLORS['YELLOW'],
                'DONE': COLORS['GREEN']
            }.get(task['status'], COLORS['RESET'])
            
            print(f"{status_color}[{task['status']}]{COLORS['RESET']} "
                  f"{task['description']}, "
                  f"id: {COLORS['BLUE']}{task['id']}{COLORS['RESET']}")

    except FileNotFoundError:
        print(f"{COLORS['RED']}No tasks found. File doesn't exist.{COLORS['RESET']}")
    except json.JSONDecodeError:
        print(f"{COLORS['RED']}Error reading tasks. Invalid JSON file.{COLORS['RESET']}")

# Help
def help(command=False):
    if not command:
        print("""
            help add          - Show add command details
            help update       - Show update command details
            help delete       - Show delete command details
            help list_tasks   - Show list command details
        """)
    else:
        if command == "add":
            print("""
            add <description>     - Add a new task with the given description
            """)
        elif command == "update":
            print("""
            update <id> <value> [-s|-d]  - Update task with given id
                -s    Update status (TODO, IN-PROGRESS, DONE)
                -d    Update description
            """)
        elif command == "delete":
            print("""
            delete <id>          - Delete task with given id
            """)
        elif command == "list_tasks":
            print("""
            list_tasks [status]  - List all tasks, optionally filtered by status
                                  status can be: TODO, IN-PROGRESS, DONE
            """)

# Commands
commands = {
    "add":add,
    "list":list_tasks,
    "delete":delete,
    "mark-done":lambda id:update(id,"DONE","-s"),
    "mark-in-progress":lambda id:update(id,"IN-PROGRESS","-s"), 
    "list_tasks":list_tasks,
    "update":update,
    "delete":delete,
    "help":help,
}

# Check arguments length
if len(arguments) == 3:
    commands[arguments[1]](arguments[2])
elif len(arguments) == 2:
    commands[arguments[1]]()
elif len(arguments) == 4:
    commands[arguments[1]](arguments[2],arguments[3])
elif len(arguments) == 5:
    result = commands[arguments[1]](arguments[2],arguments[3],arguments[4])
    if result:  # If function returns something
        success, message, data = result
        print(message)
        if success and data:  # If operation was successful and has data
            print("Updated Task:", data)
# Need to handle variable length:
elif arguments[-1] in ['-s', '-d']:
    flag = arguments[-1]
    id = arguments[2]
    new_value = ' '.join(arguments[3:-1])  # Join all words between id and flag
    commands[arguments[1]](id, new_value, flag)
elif arguments[1] not in commands:
    print("Invalid command")



