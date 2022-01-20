# Scrambler App
The Scrambler is a Python based encryption app that makes it easy to secure and/or obfuscate messages, files, and data. It leverages OpenSSL AES-256 with PBKDF2 to encrypt contents. This tool is primarily intended for Linux, but works on Windows and Mac using Git Bash (https://git-scm.com/downloads) and OpenSSL (comes with Git Bash by default).
* Github repo: https://github.com/ArcticTechnology/ScramblerApp
* PyPi: https://pypi.org/project/ScramblerApp/

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/master/doc/scrambler-preview.gif?raw=true)

## Prerequisites
The Scrambler app is intended for the Linux terminal and should work on it out of the box. However, you may need to add ```~/.local/bin/``` to PATH if you are getting a ```command not found``` error when trying to run the app. See this thread for details: https://stackoverflow.com/a/34947489. To add ```~/.local/bin/``` to PATH do the following:
1. Add ```export PATH=~/.local/bin:$PATH``` to ```~/.bash_profile```.
```
echo export PATH=~/.local/bin:$PATH > ~/.bash_profile
````
2. Execute command.
```
source ~/.bash_profile
```

This app can work for Windows and Mac. It is recommended to run it on the Git Bash terminal. Here are the instructions for installing and setting up Git Bash:

1. Go to https://git-scm.com/downloads and click download.
```
Version >= 2.34.1
```
2. During the installation setup, make sure to include OpenSSH. Recommenced setting should be fine:
```
Use bundled OpenSSH - This uses ssh.exe that comes with Git.
```
3. Leave the other settings as default, click through, and install.

IMPORTANT: For Windows, run this app on the ```bash.exe``` terminal rather ```git-bash.exe```. There is a known issue with ```git-bash.exe``` messing up Python ```os``` commands in ```import os```. See this thread for details: https://stackoverflow.com/questions/33622087/composer-installation-error-output-is-not-a-tty-input-is-not-a-tty/33623136#33623136.
* ```bash.exe``` can be found in your Git folder in the ```bin/``` directory.
* For example: If ```git-bash.exe``` is here ```C:\Program Files\Git\git-bash.exe``` then you should find ```bash.exe``` here ```C:\Program Files\Git\bin\bash.exe```.

## Installation
This library is hosted on PyPi and can be installed via ```pip```:
```
pip3 install ScramblerApp
```

## Usage
After installation, you can run this app in your terminal with this command:
```
scramblerapp
```
You can also run with the python command ```python3 -m```:
```
python3 -m scramblerapp
```
This will bring up the main menu as follows:

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/master/doc/scrambler-mainmenu.png?raw=true)

## Documentation
The purpose of this app is to make it easy to secure messages, files, and data either through encryption and/or through obfuscation. This guide will go over the different functions within the app.

### Set Dir
The Set Dir command allows you to set a working directory. In order to use most of the Scrambler's functions you will need to have a working directory set. This lets the Scrambler know which files and folders to use. For example, when encrypting a file in your working directory, you can simply pass the file name rather than the full path of the file.

The Scrambler works natively for linux paths. However, it should also work for windows and mac paths, as set dir will attempt to convert them to a standard format. Acceptable directory format examples include:
* ```/home/user/documents/myfolder```
* ```/c/user/documents/myfolder```
* ```C:/documents/myfolder```
* ```C:\documents\myfolder```

### Encrypt and Decrypt
The Scrambler app utilizes OpenSSL AES-256-CBC specification with PBKDF2 to encrypt content. OpenSSL is an open-source software library that allows applications that secure communications over computer networks. Its available for most Unix-like operating systems such as Linux and macOS as well as Microsoft Windows. See this wiki for more detail: https://en.wikipedia.org/wiki/OpenSSL. The AES-256-CBC specification with PBKDF2 is the encryption standard for using a password to encrypt and decrypt data. For more detail on AES see this wiki: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard. Also see this wiki for PBKDF2: https://en.wikipedia.org/wiki/PBKDF2. The following will describe the different content that the Scrambler can encrypt and decrypt.

1. A Message - The scrambler has the ability perform a simple password encrypt / decrypt on messages. Here is an example below. Try decrypting the following encrypted message with the Scrambler app.
```
cipher: U2FsdGVkX19/HGbvp3mtaqzuLiqdIEXfpYLCxIhJDf8=
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

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/master/btcaddr1.png?raw=true)
