# Task Tracker CLI

A simple command-line interface for managing your tasks.

## Installation

1. Ensure you have Python 3.x installed
2. Clone this repository
3. Navigate to the project directory

## Usage

### Add a new task

bash
python task-cli.py add "Your task description"


### List tasks
bash
python task-cli.py list


### List specific status
bash
python task-cli.py list --status TODO
python task-cli.py list --status DONE


### Mark task as done
bash
python task-cli.py done <task-id>


### Delete a task

python task-cli.py delete <task-id>


## Task Statuses
- TODO: Default status for new tasks
- DONE: Completed tasks

## Examples

bash
Add a new task
python task-cli.py add "Buy groceries"

List all TODO tasks
python task-cli.py list --status TODO

Mark task as done
python task-cli.py done 1

Delete task
python task-cli.py delete 1


## File Storage
Tasks are stored in a local JSON file named `task.json`.
