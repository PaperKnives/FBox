![FBox_Logo](https://github.com/PaperKnives/FBox/assets/151085561/8335936d-3ee5-42fe-b49d-7712f15fa8fc)
# FBox
FBox is a file encryption, decryption and storage program for those who do not want to pay for apps that store their
sensitive information on an unknown server or cloud service. It's aim is to let the user safely store their personal files
on their own machine locally. It uses pycryptodome for AES encryption and KEY generation as I am currently trying to adhere
to the NIST encryption standards. It also uses everyones favorite, the builtin (as of python 2.5) sqlite3 for database creation
and storage. Currently using customtkinter for a more modern no frills GUI.
## What and Why:
A Pyhton program that will set up a database and store user account info as well as encrypted files under 
a "nickname" with an ugly but functional GUI using customtkinter. Why? Why not, I needed a project and this is what 
came to mind, Falls short to current industry standards? Maybe. Doesn't follow best practices? You bet! But slowly
with a little hard work and some more experience, maybe a few contributions, this could become a cool project 
with alot of potential. 

Built in python version 3.11.4

### List of installs: 
```
pip install customtkinter
pip install pycryptodome
```
The rest of the imports should be part of the standard python library.

## How it works:
When you run the program for the first time you will need to create an account that includes an username and password.

User will then need to login using the newly created account, to do so the user needs to input the username and password,
click the "Submit acc info" button (currently).
Click the Submit button.

With successful login, User will be directed to the main program window.

To input a file for encryption and storage, the user needs to copy and paste the file path into the top entry field.
***Make sure to delete the parentheis from a windows file path (see known issues)***

User then enters a nickname for the file.
Smash that "Encrypt File" button.
To view a list of stored file nicknames crush the "View Files" button.
This will then display the nicknames in the listbox.

To decrypt a file and view it, select the desired file nickname in the listbox and simply hit "Decrypt Selected"
The file will then be able to be viewed with a selected default viewer.

When done simply Smack the "Log Out" button.
"Enjoy your day"

## Known Issues:
- Although all file types are able to be encrypted and stored, the only files currently able to be viewed are text files.
- The "Nickname" list does not refresh when a new file is stored and will create a duplicate nickname to appear in the list.
- Working on a fix for the user to have to remove the parenthesis at the beginning and ond of the file path (on windows).
- Key storage does not currently utilize best practice and is stored in the db with the file.
- the username and password are currently stored as plain text inside the user table.
- Currently all stored data is viewable to anyone who creates a new account, making login useless.
- No option to delete stored files.

## Future Imporvements:
ALOT...
- File deletion.
- Rename a stored file.
- Ability to view all file types (not just txt).
- Account recovery.
- Possibly delete all stored data after a user specified ammount of failed login attempts.
- Account recovery.
- The ability to turn off, or specify the number of accounts able to be created.
- Stored data only viewable to the owner, unless the user specifies otherwise.
- Appropriate username, password, key management.






