# Scrambler App
The Scrambler is a terminal based encryption app that makes it easy to secure and/or obfuscate messages, files, and data. It leverages OpenSSL AES-256 with PBKDF2 to encrypt contents. This tool is primarily intended for Linux, but works on Windows and Mac using the Git Bash (https://git-scm.com/downloads).
* Github repo: https://github.com/ArcticTechnology/ScramblerApp
* PyPi: https://pypi.org/project/ScramblerApp/

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/master/doc/scrambler-preview.gif?raw=true)

## Installation
This library is hosted on PyPi and can be installed via ```pip```:
```
pip3 install ScramblerApp
```

## Usage
This app is designed for Linux, but can work on Windows and Mac, via the Git Bash terminal: ```https://git-scm.com/downloads```. Run the app in your terminal with: 
```
./main.py
```
Or run it with ```python3```:
```
python3 main.py
```

This will bring up the main menu as follows:

![alt text](https://github.com/ArcticTechnology/ScramblerApp/blob/master/doc/scrambler-mainmenu.png?raw=true)

## Documentation

The idea is the have an easy way to encrypt and decrypt stuff.

### Set Dir
Lets you set the workind directory works for natively for linux paths. Should work for windows and mac as well. Acceptable directory format examples: TBD

### Encrypt and Decrypt

Encryption standard explained: TBD

#### A Messages

Encrypt and decrypt messages. Try this:
```
U2FsdGVkX19/HGbvp3mtaqzuLiqdIEXfpYLCxIhJDf8=
```
Password is:
```
abcdef1234567890
```

#### A File

You can specify a file in your working directory to encrypt or decrypt. This app will add a -c to the end of the file name after encryption, before the extension if the file has an extension ```example-c.txt```. Decrypting an encrypted file will add a NAKED at the end. ```example-NAKED.txt```.

#### All Files

You can choose to encrypt all files in a directory. Will encrypt all files in the directory and all its sub directories. You can specify a file type.

#### Columns in a Dataframe
You can encrypt specific pieces of data in a dataframe. That way specific columns are encrypted. This feature is not yet available.

### Stash
Stash allows you to obfiscate files by stashing the file into a prespecified location and altering the name and metadata of the file. At any time can retrieve the files with this app when you need the files.

#### Setting up Stash
JSON standard. Example: TBD

#### Stash files
Explain what it does: TBD

#### Retrieve stashed files
Explain what it does: TBD

#### Encrypt config file
Explain what it does: TBD

### Timetravel
Timetravel will alter the metadata of files and folders in a directory and its subdirectories so that they are scrambled to a date/time in the past. You can specify a file type.

### Conclusion
App allows you to encrypt messages, files, data.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/master/btcaddr1.png?raw=true)

