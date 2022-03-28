# Scrambler App
The Scrambler is a simple, modern, Python encryption tool that makes it easy to secure and/or obfuscate messages, files, and data. It leverages OpenSSL AES-256 to encrypt contents. See the "Documentation" section below for more details.
* Github repo: https://github.com/ArcticTechnology/ScramblerApp
* PyPi: https://pypi.org/project/ScramblerApp/

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/main/doc/scrambler-preview.gif?raw=true)

## Prerequisites
For Windows, it is recommended to run this app on a Linux emulation layer such as the Git Bash terminal. See the "Instructions for Git Bash" section for details. In addition to Git Bash you will also need to install Python3 and Pip3 as described below.

For Mac and Linux, this app should work out of the box on the Linux or Mac terminal, but you must have Python3 and Pip3 as described below.

This app requires the following:
* Python3 (version 3.8 or greater) - Install Python3 here: [https://www.python.org/downloads/]. Check version with: ```python3 --version```.
* Pip3 (version 20.2.1 or greater) - Make sure to install python3-pip in order to use pip install. Check version with: ```pip3 --version```.

## Installation
There are a couple of options to install this app:
* Pip Install - This app is hosted on PyPi and can be installed with the following command:
```
pip3 install ScramblerApp
```
* Local Install - Alternatively, you can download or git clone the Github repo and install it locally with the following:
```
git clone https://github.com/ArcticTechnology/ScramblerApp.git
cd ScramblerApp
pip3 install -e .
```
To uninstall this app:
```
pip3 uninstall ScramblerApp
```
* If you used the local install option, you will also want to delete the ```.egg-info``` file located in the ```src/``` directory of the package. This gets created automatically with ```pip3 install -e .```.

## Usage
After installation, you have a couple ways to run this app.
* Run this app from the terminal with this command:
```
scramblerapp
```
* Run this app with the python command ```python3 -m```:
```
python3 -m scramblerapp
```
Either method should bring up the main menu which looks follows:
![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/main/doc/scrambler-mainmenu.png?raw=true)

## Documentation
The Scrambler is a simple, modern, Python encryption tool that makes it easy to secure and/or obfuscate messages, files, and data. It leverages OpenSSL AES-256 with PBKDF2 to encrypt contents. This guide will go over the different functions within this app.

### Set Dir
The Set Dir command allows you to set a working directory. In order to use most of the Scrambler's functions you will need to have a working directory set. This lets the Scrambler know which files and folders to use. For example, when encrypting a file in your working directory, you can simply pass the file name rather than the full path of the file.

The Scrambler works natively for linux paths. However, it should also work for windows and mac paths, as set dir will attempt to convert them to a standard format. Acceptable directory format examples include:
* ```/home/user/documents/myfolder```
* ```/c/user/documents/myfolder```
* ```C:/documents/myfolder```
* ```C:\documents\myfolder```

### Encrypt and Decrypt
The Scrambler app utilizes OpenSSL AES-256-CBC specification with PBKDF2 to encrypt content. OpenSSL is an open-source software library that allows applications that secure communications over computer networks. Its available for most Unix-like operating systems such as Linux and macOS as well as Microsoft Windows. See this wiki to learn more about OpenSSL: [https://en.wikipedia.org/wiki/OpenSSL]. The AES-256-CBC specification with PBKDF2 is the encryption standard for using a password to encrypt and decrypt data. For more detail on AES see this wiki: [https://en.wikipedia.org/wiki/Advanced_Encryption_Standard]. See also this wiki for documentation on encrypting with OpenSSL: [https://wiki.openssl.org/index.php/Enc]. The following will describe the different content that the Scrambler can encrypt and decrypt.

1. A Message - The scrambler has the ability perform a simple password encrypt / decrypt on messages. Here is an example below. Try decrypting the following encrypted message with the Scrambler app.
```
cipher: U2FsdGVkX193YXQOuyQJZuxxEeR3AJe3lIVBxDMYBLA=
```
* The password is: ```abcdef1234567890```.

2. A File - The Scrambler can also password encrypt/decrypt a file. Simply specify the name of a file in your working directory and a password. You can also provide Scrambler with full path of a file if you would like to action a file not in your working directory.
* Encrypt will add a "-c" to the end of the file name before the file extension (if any); for example: ```example-c.txt```.
* Decrypting an encrypted file will add a "-NAKED" at the end: ```example-NAKED.txt```.

3. All Files - You can also encrypt/decrypt all files in a specified directory and its subdirectories. To do this, set a working directory, then select Encrypt or Decrypt > All Files. The Scrambler will crawl through your working directory and its subdirectory and attempt to encrypt every file it finds. You also have the option to specify a file type to encrypt. This will restrain the app to only action files of that specific type. The Scrambler default to the .txt file type. Use * to encrypt all files regardless of type.

3. Columns in a Dataframe - Lastly, you can encrypt specific pieces of data in a dataframe. Oftentimes you may have a data frame where only specific columns have sensitive information. This app allows you to encrypt those columns without altering the rest of the data set. Currently, this feature is not available.

### Stash
The Scrambler app also allows you to obfuscate files through the stash feature. Stash allows you to map files to alias names and a pre-defined location. Then the Scrambler will alter the name and move it to the pre-defined location, and then scramble the metadata of the files and directories to hide the file. At any time, Scrambler can retrieve the stashed files by providing a password. In order to use stash you have to setup a config file that tells the Scrambler where to send your stashed files to and what their new names will be.

Instructions on creating a config file:
1. Create your .config based off of .config-template in this repository. The .config file follows JSON formatting and should contain these pieces of data:
```
{"origin_dir": "/home/origin_directory/",
"stash_dir": "/home/stash_directory/",
"stash_key": {
"filename1": "stashed_filename1",
"filename2": "stashed_filename2",
"filename3": "stashed_filename3"}}
```
* ```"origin_dir": "/home/origin_directory/"``` - This is the directory where the files you want to stash are located.
* ```"stash_dir": "/home/stash_directory/"``` - This is the directory where you want to stash your files.
* ```"filename1": "stashed_filename1"``` - This is the mapping of the original file name and the name you want the new file name you want the file to be changed to.

2. Save your file as .config and place it into your scrambler app's config folder. Here is an example of what the directory looks like:
```
C:/Users/username/AppData/Local/Python3/ScramblerApp/config
```
3. Highly recommended: Password encrypt this .config file with the Scrambler app. This will create .config-c which is still recognizable by Scrambler.
4. Highly recommended: Once you have the encrypted version (.config-c) you can delete the original .config file as it is no longer needed. You defeat the purpose of an encrypted config file if the unencrypted version is still lying around. Note if stash detects an unencrypted version, you can choose to have stash encrypt it for you which will automatically delete the original.

### Timetravel
Timetravel is another obfuscation feature of the Scrambler app. Timetravel alter the metadata of all files and folders in a directory and subdirectories. Specifically it forces their date and time metadatas to be scrambled to some time in the past. This makes it so that you will not be able to determine when a file or folder was last touched or altered. To do this, simply set a working directory and run timetravel. The Scrambler will crawl through the working directory and its subdirectory and attempt to scramble the metadata of every file and folder it finds.

### Conclusion
With the Scrambler, you can now secure your messages, files, and data. Easily password encrypt sensitive information and obfuscate important files from view. Hope you enjoy.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/main/btcaddr1.png?raw=true)
