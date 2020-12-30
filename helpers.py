import os
import pymongo
import cv2
import datetime
import base64
import shutil

client = pymongo.MongoClient()
db = client['shopifyChallenge']
imageRepo = db['imageRepo']

path = os.path.dirname(__file__)

def createFolder(folderName):
    fName = os.path.join(path, folderName)

    if (not os.path.isdir(fName)):
        os.mkdir(fName)

    return fName

def deleteFolder(folderName):
    fName = os.path.join(path, folderName)

    if (os.path.isdir(fName)):
        shutil.rmtree(fName)

def introTextAndUsername():
    print()
    print('Welcome to Ethan\'s Spotify Backend Challenge Submission!')
    print('As this is a backend challenge, there will be no \'proper\' frontend associated with this project.')
    print()
    print('Images in this repository have the option of being private as well as deleting images requires the correct permission.')
    print('Because of this we will need to validate your identity by asking you for your username.')
    print()

    username = str(input('Please enter your username: '))
    print()

    print('Hi', username + '! Welcome to the image repository!')

    return username

def printHelp():
    print('Here are a list of the commands available in this program:')
    print('add - Opens a new folder where you can drag and drop the images that you would like to add into the repository')
    print('delete - Opens a new folder where you can delete the images that you want to remove from the repository')
    print('list - Opens a new folder where you can view the images in the repository')
    print('search - Allows you to input search parameters and then displays the resulting images in a new folder')
    print('exit - This command will terminate the program')
    print('help - This command will list out the help text')
    print()

def add(username, folderName):
    print('Are these images going to be \'public\' or \'private\'?')
    print('Private - These images will only be visible to you')
    print('Public - These images will be visible to everyone')
    print()

    isPublic = None
    valid = False
    while (not valid):
        command = str(input("Will your images be \'public\' or \'private\': ")).strip().lower()
        print()

        valid = True

        if (command == 'public'):
            isPublic = True
        elif (command == 'private'):
            isPublic = False
        else:
            valid = False
            print('\'' + command + '\'', 'is not a valid input, please enter either \'public\' or \'private\'')
            print()

    fName = createFolder(folderName)

    print('A folder has been created at the location', fName)
    print('Please copy all of the images that you would like to add into this repository and paste them into the input folder.')
    print('Make sure to COPY your files instead of moving them as this folder will be deleted afterwards.')
    print('When you are finished inserting your images into the folder, please enter \'done\' to continue or \'cancel\' to cancel this action.')
    print()

    os.startfile(fName)

    continuing = None
    valid = False
    while (not valid):
        continueInput = input('Enter either \'done\' or \'cancel\': ').strip().lower()
        print()

        valid = True

        if (continueInput == 'done'):
            continuing = True
        elif (continueInput == 'cancel'):
            continuing = False
        else:
            print('\'' + continueInput + '\'', 'is not a valid input, please enter either \'done\' or \'cancel\'')
            print()

    if (continuing):
        date = datetime.date.today().strftime("%d/%m/%Y")

        # Get all images from folder
        imagesToInsert = []
        for filename in os.listdir(fName):
            path = os.path.join(fName,filename)
            if cv2.imread(path) is not None:
                with open(path, 'rb') as imageFile:
                    imagesToInsert.append({
                        'data': base64.b64encode(imageFile.read()),
                        'name': filename,
                        'author': username,
                        'type': filename.split('.')[1].upper(),
                        'public': isPublic,
                        'date': date
                    })

        imageRepo.insert_many(imagesToInsert)

        print('You have inserted', len(imagesToInsert), 'image(s) into the repository.')
        print()
    else:
        print('This action has been cancelled.')
        print()

    deleteFolder(folderName)

def list(username, folderName):
    images = imageRepo.find({ '$or': [ { 'public': { '$eq' : True } }, { 'author': username } ] })

    print('Your images are being loaded')
    print()

    fName = createFolder(folderName)

    for image in images:
        count = 0;
        filename = image.get('name')
        while (os.path.exists(os.path.join(folderName, filename))):
            count += 1
            filename = image.get('name').split('.')[0] + " (" + str(count) + ")." + image.get('name').split('.')[1]

        with open(os.path.join(folderName, filename), 'wb') as imageFile:
            imageFile.write(base64.b64decode(image['data']))

    print('A folder has been created at the location', fName)
    print('This folder contains all of the images in the repository that are either public or owned by you.')
    print('Editing the images in this folder will have no effect on the images stored in the repository.')
    print('When you are done viewing the images in this folder, you may press \'enter\' to continue.')
    print()

    os.startfile(fName)

    input('Press \'enter\' to continue: ')
    print()

    deleteFolder(folderName)

def search(username, folderName):
    print('For each of the following parameter options listed, either enter a value if you would like to search based on that field or leave it blank to not search against it')

    filename = str(input('filename: '))
    author = str(input('author: '))

    queryAnds = []
    queryAnds.append({ '$or': [ { 'public': { '$eq' : True } }, { 'author': username } ] })

    queryOrs = []
    if (len(filename) > 0):
        queryOrs.append({ 'name': { '$regex': '.*' + filename + '.*', '$options': 'si' } })
    if (len(author) > 0):
        queryOrs.append({ 'author': { '$regex': '.*' + author + '.*', '$options': 'si' } })

    if (len(queryOrs) > 0):
        queryAnds.append({ '$or': queryOrs })

    images = imageRepo.find( { '$and': queryAnds } )

    print('Your images are being loaded')
    print()

    fName = createFolder(folderName)

    for image in images:
        count = 0;
        filename = image.get('name')
        while (os.path.exists(os.path.join(folderName, filename))):
            count += 1
            filename = image.get('name').split('.')[0] + " (" + str(count) + ")." + image.get('name').split('.')[1]

        with open(os.path.join(folderName, filename), 'wb') as imageFile:
            imageFile.write(base64.b64decode(image['data']))

    print('A folder has been created at the location', fName)
    print('This folder contains all of the images in the repository that are either public or owned by you.')
    print('Editing the images in this folder will have no effect on the images stored in the repository.')
    print('When you are done viewing the images in this folder, you may press \'enter\' to continue.')
    print()

    os.startfile(fName)

    input('Press \'enter\' to continue: ')
    print()

    deleteFolder(folderName)

def delete(username, folderName):
    images = imageRepo.find({ 'author': username })

    print('Your images are being loaded')
    print()

    fName = createFolder(folderName)

    filenameToMongoId = {}
    for image in images:
        count = 0;
        filename = image.get('name')
        while (os.path.exists(os.path.join(folderName, filename))):
            count += 1
            filename = image.get('name').split('.')[0] + " (" + str(count) + ")." + image.get('name').split('.')[1]

        filenameToMongoId[filename] = image.get('_id')
        with open(os.path.join(folderName, filename), 'wb') as imageFile:
            imageFile.write(base64.b64decode(image.get('data')))

    print('A folder has been created at the location', fName)
    print('This folder contains all of the images in the repository that are owned by you.')
    print('To delete an image from the repository, all you have to do is delete it from the folder.')
    print('When you are done deleting your images, please enter \'done\' to continue or \'cancel\' to cancel this action.')
    print('Once you continue, the changes will go into affect and your images will be removed from the repository.')
    print()

    os.startfile(fName)

    continuing = None
    valid = False
    while (not valid):
        continueInput = input('Enter either \'done\' or \'cancel\': ').strip().lower()
        print()

        valid = True

        if (continueInput == 'done'):
            continuing = True
        elif (continueInput == 'cancel'):
            continuing = False
        else:
            print('\'' + continueInput + '\'', 'is not a valid input, please enter either \'done\' or \'cancel\'')
            print()

    if (continuing):
        for filename in os.listdir(fName):
            filenameToMongoId.pop(filename, None)

        imagesToDelete = [filenameToMongoId[k] for k in filenameToMongoId]

        imageRepo.delete_many({ '_id' : { '$in' : imagesToDelete } })

        print('You have deleted', len(imagesToDelete), 'images from the repository.')
        print()
    else:
        print('This action has been cancelled.')
        print()

    deleteFolder(folderName)
