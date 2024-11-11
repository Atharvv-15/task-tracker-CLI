import sys
import datetime
import uuid
import json

arguments = sys.argv
print(arguments)

def add(arg):
    task = {
        "id":str(uuid.uuid4())[:8],
        "description":arg,
        "status":"todo",
        "createdAt":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "updatedAt":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        with open('task.json','r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'tasks':[]}
    except json.JSONDecodeError:
        print('Error: Invalid JSON file')
        data = {'tasks':[]}

    data['tasks'].append(task)

    with open('task.json','w') as file:
        json.dump(data,file,indent=2)

def list_tasks():
    with open('task.json','r') as file:
        data = json.load(file)
    
    todo_tasks = [task for task in data['tasks'] if task['status'] == 'todo']
    in_progress = [task for task in data['tasks'] if task['status'] == 'in-progress']
    done_tasks = [task for task in data['tasks'] if task['status'] == 'done']

    print("Total tasks:", len(data['tasks']))
    for todo_task in todo_tasks:
        print(f'[TODO] {todo_task["description"]}, id: {todo_task["id"]}')
    for in_progress_task in in_progress:
        print(f'[IN-PROGRESS] {in_progress_task["description"]}, id: {in_progress_task["id"]}')
    for done_task in done_tasks:
        print(f'[DONE] {done_task["description"]}, id: {done_task["id"]}')

        


def update(arg):
    print("Update",arg)

def delete(arg):
    print("Delete",arg)

#commands
commands = {
    "add":add,
    "update":update,
    "delete":delete,
    "list_tasks":list_tasks
}

if len(arguments) == 3:
    commands[arguments[1]](arguments[2])
elif len(arguments) == 2:
    commands[arguments[1]]()
elif arguments[1] not in commands:
    print("Invalid command")



