# Scrambler App
This collection of tools that makes it easy to secure and/or obfuscate messages, files, and data. It leverages encryption tools such as openssl and fernet. This tool is primarily intended for Linux.
* Github repo: https://github.com/ArcticTechnology/ScramblerApp.git
* PyPi: TBD

## Installation
This library is hosted on PyPi and can be installed via ```pip```:
```
pip3 install PythonStarterPackage
```
For manual install, see below.

### Manual Install
To manually install this package, clone this repo to your local system. After you clone the repo, navigate into the package to where the ```setup.py``` file is. Then you can use the ```pip install -e .``` command. This will install the package and all its dependencies editable mode. Then you can use the package locally or use it as the starting point for building out your own package.
```
pip3 install -e .
```

## Usage
You can run the app in your terminal with:
```
./main.py
```
You can also import this module into your own project and incorporate it into your own packages. For example:
```
from scrambler import *
scrambler = Scrambler()
scrambler.run()
```

## Documentation
The purpose of this project is to show you how to create a standard python package from scratch. This project is inspired by Sigma-Coding (https://github.com/areed1192/sigma-coding), it is a great detailed guide on deploying python packages.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/master/btcaddr1.png?raw=true)

