# Don't Break the Chain!
Habit tracker, that works by not breaking the chain.

Every day that you complete a habit, a new link is added to the chain.

If you break the streak by forgeting a consecutive day, then the chain breaks, and resets back to zero.


## Required libraries:
- [Pandas](https://pandas.pydata.org/)
- Datetime
- os
- sys

## How it works.
Don't break the chain, works by keeping track of habits in a CSV file called 'habits.csv', using the Pandas library to parse, and write to it.

When you first run the script, it checks if the CSV file 'habits.csv' is in your working directory. If not, then the script will automatically create one for you.

Running the script with no arguments, is equivalent to running the command `chain todo.`

There are 6 commands:
- `chain new [habit-name]` Creates a new habit 
- `chain all` Lists all the habits you currently have, in numerical order from when you created them.`
  - Automatically resets a habit back to zero, if the chain is broken.
- `chain todo` Lists all the habits that are incomplete for today.
- `chain complete` Lists all the habits that you've completed for today.
- `chain delete [habit-number]` Deletes a habit. Referenced by it's numerical order in the list.
- `chain add [habit-number]` Adds a new chain to the habit. Referenced by it's numerical order in the list.
  - Will not add a new chain, if a chain was already added on the current day of running the script.
  - Checks if the chain is broken, and resets it (If the list command, didn't already do so).
