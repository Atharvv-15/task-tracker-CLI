# Task Tracker CLI

[Project URL](https://roadmap.sh/projects/task-tracker)

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
python task-cli.py list TODO
python task-cli.py list DONE


### Mark task as done
bash
python task-cli.py mark-done <task-id>


### Delete a task

python task-cli.py delete <task-id>


## Task Statuses
- TODO: Default status for new tasks
- DONE: Completed tasks
- IN-PROGRESS: In Progress tasks

## Examples

bash
Add a new task
python task-cli.py add "Buy groceries"

List all TODO tasks
python task-cli.py list TODO

Mark task as done
python task-cli.py done <id>

Delete task
python task-cli.py delete <id>


## File Storage
Tasks are stored in a local JSON file named `task.json`.
