# personal-task-manager
A simple Python CLI that helps you keep track of the tasks in your life.
## Release Notes
### 0.1.0
* Bare-bones personal task manager than runs in your command line.
### 0.2.0
* Multiple tasks can now be added in one command
  * Each task should be delimted by '\'
* Tasks can now be reverted to 'Not done'
  * The 'done' key just reverts a task's completion status
* Added a "help" key for command guide
### 0.2.1
* Added a calendar to the main display of the CLI
  * Only displays current month and highlights current day
  * Due date functionality coming in 0.3.0
* Minor update to the help command
* Added color to the Done/Not done indicators
### 0.3.0
* Due date functionality has been added
  * new_task function allows for date input
  * edit_task function allows for date editing
  * help command provides proper syntax
* Calendar now displays color-coded days according to the tasks
* Fixed error when passing invalid number of arguments
## Future Plans
* Add folder and subtask functionality
* Improve styling
* Allow for different date formats
## Resources
* .md editing:
  * https://guides.github.com/features/mastering-markdown/
* Handling releases:
  * https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository
