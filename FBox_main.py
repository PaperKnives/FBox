import customtkinter as ctk
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import messagebox
import tempfile
import os
import sqlite3
import webbrowser
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


connection = sqlite3.connect('account.db')
connection.execute('''CREATE TABLE IF NOT EXISTS FBox_user(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_name TEXT,
pass_word TEXT
)''')


connection.execute('''CREATE TABLE IF NOT EXISTS personal_files(
file_id INTEGER PRIMARY KEY AUTOINCREMENT,
new_file_name TEXT,
key TEXT,
file BLOB
)''')

# Connect to the sqlite db
cursor = connection.cursor()


class AccountSetUp(ctk.CTkToplevel):
    def __init__(self):
        """
        AccountSetUp appears when the new account button is clicked from the login window,
        username, password data is then stored:
        db = account.db
        Table = (Fbox_user)
        """
        super().__init__()

        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.title("Account Setup")

        # Username input box
        self.new_user_entry = ctk.CTkEntry(self,
                                           width=200,
                                           placeholder_text="Please enter a new username"
                                           )
        self.new_user_entry.grid(row=0,
                                 column=0,
                                 padx=20,
                                 pady=20
                                 )
        # Password input entry box
        self.master_password = ctk.CTkEntry(self,
                                            width=200,
                                            placeholder_text="Please enter a new password"
                                            )
        self.master_password.grid(row=1,
                                  column=0,
                                  padx=20,
                                  pady=20
                                  )
        # 2nd entry box for password confirmation
        self.master_password_check = ctk.CTkEntry(self,
                                                  width=200,
                                                  placeholder_text="Confirm password"
                                                  )
        self.master_password_check.grid(row=2,
                                        column=0,
                                        padx=20,
                                        pady=20
                                        )
        # Submit button for account creation
        self.submit = ctk.CTkButton(self,
                                    width=200,
                                    fg_color="#702963",
                                    hover_color="#D339DB",
                                    text="submit",
                                    command=self.save_profile
                                    )
        self.submit.grid(row=3,
                         column=0,
                         padx=20,
                         pady=20
                         )

        # Save new user data to the db.
    def save_profile(self):
        user_name = self.new_user_entry.get()
        pass_word = self.master_password.get()
        check = self.master_password_check.get()
        try:
            if pass_word == check:
                connection.execute('INSERT INTO FBox_user('
                                   'user_name,'
                                   'pass_word) '
                                   'VALUES(?, ?)',
                                   (user_name, pass_word)
                                   )
                connection.commit()
                # Return to the login page after account creation needed
            else:
                messagebox.showerror('passwords dont match',
                                     "Please try again"
                                     )
            self.withdraw()
        except Exception as e:
            messagebox.showerror("Account set up failed",
                                 f"{e}"
                                 )


class LoginApp(ctk.CTkToplevel):
    user = ''
    passw = ''

    def __init__(self, login_command):
        """Will direct to:
        AccountSetUp(new user)
        Verify credentials(existing user)
        """
        super().__init__()
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.title("Login")
        # Username entry
        self.entry = ctk.CTkEntry(self,
                                  placeholder_text="Username"
                                  )
        self.entry.grid(padx=20, pady=20)
        # Password entry
        self.entry2 = ctk.CTkEntry(self,
                                   show="*",
                                   placeholder_text="Password"
                                   )
        self.entry2.grid(padx=20,
                         pady=20
                         )
        # Button to submit the name and pass because it's how it'll work for now
        self.submit_user_info = ctk.CTkButton(self,
                                              fg_color='#702963',
                                              hover_color="#D339DB",
                                              text='submit acc info',
                                              command=self.get_info
                                              )
        self.submit_user_info.grid(padx=20,
                                   pady=20
                                   )
        # Submit button to actually login
        self.button = ctk.CTkButton(self,
                                    fg_color="#702963",
                                    hover_color="#D339DB",
                                    text="Submit",
                                    command=login_command
                                    )
        self.button.grid(padx=20,
                         pady=20
                         )
        # New User account set up nav button
        self.accButton = ctk.CTkButton(self,
                                       fg_color="#702963",
                                       hover_color="#D339DB",
                                       text="Create new account",
                                       command=self.create_new
                                       )
        self.accButton.grid(padx=20,
                            pady=20
                            )
        # Add text field explaining how to log in, it works but, it is not fluid

    def get_info(self):
        LoginApp.user = self.entry.get()
        LoginApp.passw = self.entry2.get()

    @classmethod
    def account_info(cls):
        print(cls.user)  # debugg
        return [cls.user, cls.passw]

    def create_new(self):
        """Create_new executed when 'Create new account' is clicked,
        user is redirected to the AccountSetUp window
        """
        #self.withdraw()
        AccountSetUp()


class MainWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.geometry("600x450")
        self.title("FBox")
        self.grid_columnconfigure(0, weight=1)
        # Entry for filepath
        self.filepath = ctk.CTkEntry(self,
                                     placeholder_text="Paste File Path and remove double quotes"
                                     )
        self.filepath.grid(row=0,
                           columnspan=5,
                           sticky='ew',
                           padx=5,
                           pady=5
                           )
        # Text entry for the stored file name
        self.FileEntry = ctk.CTkEntry(self,
                                      placeholder_text="Enter new file name"
                                      )
        self.FileEntry.grid(row=1,
                            columnspan=5,
                            sticky='ew',
                            padx=5,
                            pady=5
                            )
        # Encryption button for the file path file
        self.encrypt_button = ctk.CTkButton(self,
                                            fg_color="#702963",
                                            hover_color="#D339DB",
                                            text="Encrypt File",
                                            command=self.file_encrypt
                                            )
        self.encrypt_button.grid(row=2,
                                 column=4,
                                 sticky='n',
                                 padx=5,
                                 pady=5
                                 )
        # Decryption button for an existing file
        self.decrypt_button = ctk.CTkButton(self,
                                            fg_color="#702963",
                                            hover_color="#D339DB",
                                            text="Decrypt Selected",
                                            command=self.decrypt_files
                                            )
        self.decrypt_button.grid(row=3,
                                 column=4,
                                 padx=5,
                                 pady=5
                                 )
        self.view_file = ctk.CTkButton(self,
                                       fg_color="#702963",
                                       hover_color="#D339DB",
                                       text="View Files",
                                       command=self.get_shit
                                       )
        self.view_file.grid(row=4,
                            column=4,
                            padx=5,
                            pady=5
                            )
        # Listbox to display the db contents
        self.listbox = tk.Listbox(self,
                                  bg='#A19FA4',
                                  relief=tk.GROOVE,
                                  selectmode=tk.BROWSE,
                                  exportselection=0
                                  )
        self.listbox.grid(row=2,
                          rowspan=4,
                          columnspan=2,
                          sticky='nsew',
                          padx=5,
                          pady=5
                          )
        # Scrollbar for the listbox
        self.Scrollbar = ttk.Scrollbar(self,
                                       command=self.listbox.yview
                                       )
        self.Scrollbar.grid(row=2,
                            column=3,
                            rowspan=4,
                            sticky='nsew',
                            padx=5,
                            pady=5
                            )

        # Logout button
        self.logout_button = ctk.CTkButton(self,
                                           fg_color='#702963',
                                           hover_color="#D339DB",
                                           text="Log Out",
                                           command=self.logout
                                           )
        self.logout_button.grid(row=5,
                                column=4,
                                sticky='e',
                                padx=5,
                                pady=5
                                )
        # Hide MainWindow
        self.withdraw()
        # Create login window and pass self.login method
        self.account_login = LoginApp(self.login_verify)

    def get_shit(self):
        # Loops over the db for display
        cursor.execute('SELECT new_file_name FROM personal_files')
        connection.commit()
        rows = cursor.fetchall()
        for row in rows:
            self.listbox.insert('end', row[0])

    def login_verify(self):
        """Gets username and password:
        checks them against
        Fbox_user db for verification
        """
        username_text = LoginApp.account_info()[0]
        pass_input_text = LoginApp.account_info()[1]
        print(f"{username_text}")  # debug statement

        try:
            login_cursor = connection.cursor()
            # Query the db for existing username and password
            login_cursor.execute('SELECT user_name, pass_word FROM FBox_user WHERE user_name = ?',
                                 (username_text,))
            row = login_cursor.fetchone()
            if row is not None and username_text == row[0] and pass_input_text == row[1]:
                print("login successful")  # debug statement
                self.login()

            else:
                messagebox.showerror('nope', 'login is incorrect')
                login_cursor.close()

        except Exception as e:
            messagebox.showerror('error', f"{e}")

    def login(self):
        self.account_login.destroy()
        # Makes window visible
        self.deiconify()

    def logout(self):
        """Will log the user out,
        send user to login window
        """
        # Creates infinite login windows when logging in and out multiple times
        tk.messagebox.askquestion(title='Log out',
                                  message='Are you sure you want to logout?'
                                  )
        self.destroy()

    def file_encrypt(self):
        """Retrieves the file via the file path
        encrypts and stores in FBox_user table
        """
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)
        new_file_name = self.FileEntry.get()
        data = self.filepath.get()
        try:
            with open(data, 'rb') as file:
                original = file.read()
                # iv = cipher.iv
                ciphertext = cipher.encrypt(pad(original, AES.block_size))
                with tempfile.NamedTemporaryFile(delete=False) as c_file:
                    c_file.write(cipher.iv)
                    c_file.write(ciphertext)
                    c_file.seek(0)
                    encrypted_content = c_file.read()
                    connection.execute('INSERT INTO personal_files('
                                       'new_file_name,'
                                       'file,'
                                       'key)'
                                       'VALUES(?, ?, ?)',
                                       (new_file_name, encrypted_content, key))
                    connection.commit()

        except FileNotFoundError as g:
            messagebox.showerror("File not found",
                                 f"{g}")

        except Exception as e:
            messagebox.showerror("An error has occurred",
                                 f"{e}")

    def decrypt_files(self):
        """Retrieves selected file decrypts,
        and stores the plaintext file
        in new folder
        """
        # Needs to get the associated file and decrypt it, maybe the c_file?
        selected_index = self.listbox.curselection()
        new_file_name = self.listbox.get(selected_index)

        try:
            # Retrieves selected file from the db
            decrypt_cursor = connection.cursor()
            decrypt_cursor.execute('SELECT file, key FROM personal_files WHERE new_file_name = ?',
                                   (new_file_name,))

            row = decrypt_cursor.fetchone()
            encrypted_content = row[0]
            key = row[1]

            if encrypted_content:
                iv = encrypted_content[:16]
                ciphertext = encrypted_content[16:]
                decipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(plaintext)
                    print(f'{plaintext}')
                    temp_file_path = temp_file.name

                    if os.path.isfile(temp_file_path):
                        webbrowser.open(temp_file_path)

                    else:
                        messagebox.showerror("Its fucked", "an error occurred")

        except Exception as e:
            messagebox.showerror('decryption error', f'an error occurred {e}')
            print(f"{e}")


if __name__ == "__main__":
    App = MainWindow()
    App.mainloop()
