# Shopify Developer Intern Challenge (Image Repository)

### How to run
- Clone the repository
- Make sure you have MongoDB running locally
- Execute the command `$ pip install -r requirements.txt` to install the correct dependencies
- Execute the command `$ python ./imageRepo.py` to start the program

### How it works
Because I am applying for the backend position I have decided to forego a web frontend and instead use the command line and file explorer to interact with my program.

When run, users will be asked to enter their username (Login credentials and validation felt out of scope for this challenge so only a username is to be supplied). This will be used to link images to users. From there the user will be able to choose between several different commands to interact with the repository.

After selecting a command to run, the main way that the user will interact with the program is through their file explorer. Each command will open up a new folder and place the desired images inside. In the case of the **add** command, users will be asked to insert the desired images into the folder. Similarly, the **list** command will place the images from the repository into a new folder where the user can then see them.

### Commands
- Add
    - Opens a new folder where you can drag and drop the images that you would like to add into the repository
- Delete
    - Opens a new folder where you can delete the images that you want to remove from the repository
- List
    - Opens a new folder where you can view the images in the repository
- Search
    - Allows you to input search parameters and then displays the resulting images in a new folder
- Exit
    - This command will terminate the program
- Help
    - This command will list out the help text