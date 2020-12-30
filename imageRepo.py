import helpers as Helpers

INPUT_FOLDER_NAME = 'inputFolder'
OUTPUT_FOLDER_NAME = 'outputFolder'

running = True

username = Helpers.introTextAndUsername()
Helpers.printHelp()

while (running):
    command = str(input("Please Enter a command: ")).strip().lower()
    print()

    if (command == 'add'):
        Helpers.add(username, INPUT_FOLDER_NAME)
    elif (command == 'delete'):
        Helpers.delete(username, OUTPUT_FOLDER_NAME)
    elif (command == 'list'):
        Helpers.list(username, OUTPUT_FOLDER_NAME)
    elif (command == 'search'):
        Helpers.search(username, OUTPUT_FOLDER_NAME)
    elif (command == 'exit'):
        running = False
        break
    elif (command == 'help'):
        Helpers.printHelp()
    else:
        print('\'' + command + '\'', 'is not a valid command, please enter a new command')
        print()

print('Thank you for using my image repository!')