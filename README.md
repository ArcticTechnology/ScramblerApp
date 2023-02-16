# Scrambler App
The Scrambler is a simple, modern, Python encryption tool that makes it easy to secure and/or obfuscate messages, files, and data. It leverages OpenSSL AES-256 with PBKDF2 to encrypt contents. See the "Documentation" section below for more details.
* Github repo: https://github.com/ArcticTechnology/ScramblerApp
* PyPi: https://pypi.org/project/ScramblerApp/

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/main/doc/scrambler-preview.gif?raw=true)

## Prerequisites
For Windows, it is recommended to run this app on a Linux emulation layer such as the Git Bash terminal. See the "Instructions for Git Bash" section for details. In addition to Git Bash, make sure you also have Python3, Pip3, and OpenSSL as described below.

For Mac, this app should work on the Mac terminal. Mac typically comes with LibreSSL by default and this app is compatible with LibreSSL. However, LibreSSL is missing the key derivation: pbkdf2. It is recommended that you install and use OpenSSL instead. Make sure you also have Python3 and Pip3 as described below.

For Linux, this app should work out of the box on the Linux terminal, but make sure you also have Python3, Pip3, and OpenSSL as described below.

Requirements:
* Python3 (version 3.10 or greater) - Install Python3 here: [https://www.python.org/downloads/]. Check version with: ```python3 --version```.
* Pip3 (version 23.0 or greater) - Make sure to install python3-pip in order to use pip install. Check version with: ```pip3 --version```.
* OpenSSL (version 3.0.2 or greater) - See wiki for details: [https://en.wikipedia.org/wiki/OpenSSL]. Check version with: ```openssl version```.

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
The Scrambler app utilizes OpenSSL AES-256-CBC specification with PBKDF2 to encrypt content. OpenSSL is an open-source software library that allows applications that secure communications over computer networks. Its available for most Unix-like operating systems such as Linux and macOS as well as Microsoft Windows. See this wiki to learn more about OpenSSL: [https://en.wikipedia.org/wiki/OpenSSL]. The AES-256-CBC specification with PBKDF2 is the encryption standard for using a password to encrypt and decrypt data. For more detail on AES see this wiki: [https://en.wikipedia.org/wiki/Advanced_Encryption_Standard]. See this wiki for documentation on encrypting with OpenSSL: [https://wiki.openssl.org/index.php/Enc]. See this wiki to learn more about PBKDF2: [https://en.wikipedia.org/wiki/PBKDF2]. The following will describe the different content that the Scrambler can encrypt and decrypt.

1. A Message - The scrambler has the ability perform a simple password encrypt / decrypt on messages. Here is an example below. Try decrypting the following encrypted message with the Scrambler app.
```
cipher: U2FsdGVkX1/2GRhgqsfjLUTxNpCrhe724CFnSydrrtM=
```
* The password is: ```abcdef1234567890```

2. A File - The Scrambler can also password encrypt/decrypt a file. Simply specify the name of a file in your working directory and a password. You can also provide Scrambler with full path of a file if you would like to action a file not in your working directory.
* Encrypt will add a "-c" to the end of the file name before the file extension (if any); for example: ```example-c.txt```.
* Decrypting an encrypted file will add a "-NAKED" at the end: ```example-NAKED.txt```.

3. All Files - You can also encrypt/decrypt all files in a specified directory and its subdirectories. To do this, set a working directory, then select Encrypt or Decrypt > All Files. The Scrambler will crawl through your working directory and its subdirectory and attempt to encrypt every file it finds. You also have the option to specify a file type to encrypt. This will restrain the app to only action files of that specific type. The Scrambler default to the .txt file type. Use * to encrypt all files regardless of type.

3. Columns in a Dataframe - Lastly, you can encrypt specific pieces of data in a dataframe. Oftentimes you may have a data frame where only specific columns have sensitive information. This app allows you to encrypt those columns without altering the rest of the data set. Currently, this feature is not available.

### Timetravel
Timetravel is an obfuscation feature of the Scrambler app. Timetravel alter the metadata of all files and folders in a directory and subdirectories. Specifically it forces their date and time metadatas to be scrambled to some time in the past. This makes it so that you will not be able to determine when a file or folder was last touched or altered. To do this, simply set a working directory and run timetravel. The Scrambler will crawl through the working directory and its subdirectory and attempt to scramble the metadata of every file and folder it finds.

### Conclusion
With the Scrambler, you can now secure your messages, files, and data. Easily password encrypt all of your sensitive information. Hope you enjoy.

## Troubleshooting
This section goes over some of the common issues found and how to resolve them.

### "Command Not Found" Error When Running the App
On Linux, if you are getting a ```command not found``` error when trying to run the app, you may need to add ```~/.local/bin/``` to PATH. See this thread for details: [https://stackoverflow.com/a/34947489]. To add ```~/.local/bin/``` to PATH do the following:

1. Add ```export PATH=~/.local/bin:$PATH``` to ```~/.bash_profile```.
```
echo export PATH=~/.local/bin:$PATH > ~/.bash_profile
```
2. Execute command.
```
source ~/.bash_profile
```

### Instructions for Git Bash
For Windows, it is recommended to run this app on a linux emulation layer like the Git Bash terminal. Here are the instructions for installing and setting up Git Bash:
1. Go to https://git-scm.com/downloads and click download.
```
Version >= 2.34.1
```
2. During the installation setup, make sure to include OpenSSH. Recommenced setting should be fine:
```
Use bundled OpenSSH - This uses ssh.exe that comes with Git.
```
3. Leave the other settings as default, click through, and install.
4. Open ```bash.exe``` and install Python3 https://www.python.org/downloads/
5. Proceed to the "Installation" section to install this app.

IMPORTANT: For Windows, use the ```bash.exe``` terminal rather ```git-bash.exe```. There is a known issue with ```git-bash.exe``` messing up Python ```os``` commands in ```import os```. See this thread for details: [https://stackoverflow.com/a/33623136].
* You can find ```bash.exe``` Git folder in the ```bin/``` directory. For example: If ```git-bash.exe``` is here ```C:\Program Files\Git\git-bash.exe``` then you should find ```bash.exe``` here ```C:\Program Files\Git\bin\bash.exe```.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/main/btcaddr1.png?raw=true)
