# KapaK: A simple-to-use file encryption script
```
$ kapak

    ▄ •▄  ▄▄▄·  ▄▄▄· ▄▄▄· ▄ •▄
    █▌▄▌▪▐█ ▀█ ▐█ ▄█▐█ ▀█ █▌▄▌▪
    ▐▀▀▄·▄█▀▀█  ██▀·▄█▀▀█ ▐▀▀▄·
    ▐█.█▌▐█ ▪▐▌▐█▪·•▐█ ▪▐▌▐█.█▌    v3.0.0
    ·▀  ▀ ▀  ▀ .▀    ▀  ▀ ·▀  ▀    by Amis Shokoohi

Description: A simple-to-use file encryption script which
             uses AES symmetric encryption methods
Link:        https://github.com/amis-shokoohi/kapak

Help:        kapak [ -h | --help ]
```

## Description
Kapak can encrypt/decrypt **file/folder** by<br>
a given password using _AES_ symmetric encryption methods.

> If you are wondering what _kapak_ means, it means _mold_.<br>
> As moldy food is not eatable, kapaky files are not readable.

- [installation](#Installation)
- [usage](#Usage)
- [examples](#Examples)
- [password](#Password)
- [contribute](#Contribute)

## Installation
### Linux
Make sure Python 3 is installed.
```
$ python3 --version
```
Install requirements:
```
$ pip3 install -r requirements.txt
```
Then run the installation script as **root** user. It will copy files into `/bin/kapak` directory and add it to the `PATH`:
```
$ cd kapak
$ chmod +x ./install.sh
$ sudo ./install.sh
```
> NOTE: I've only tested this on Debian based distros.
### Windows
Download zipfile from [here](https://github.com/amis-shokoohi/kapak/releases/download/v3.0.0/kapak-windows-v3.0.0.zip).<br>
You can use `kapak.exe` now, but if you want to run it from anywhere in your system, follow instruction below:
- Right click on `install.cmd` and click on `Run as administrator`.
- Open Windows search bar and search for `var`. Click on `Edit the system environment variables`. Click on `Environment Variables...`. In `User variables` section look for `Path`, choose it and hit the `Edit...` button. Click on `New` and paste `C:\PROGRA~1\kapak`. Click `OK` `OK` `OK`, and you're done. Open a terminal an type `kapak`, you should be able to see its logo.

## Usage
```
$ kapak -h

Usage: kapak [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] PATH

Global Options:
  -h, --help     Prints help message
  -v, --version  Prints version

Commands:
  encrypt  Encrypts the specified file/directory
  decrypt  Decrypts the specified file/directory
```
```
$ kapak encrypt -h

Usage: kapak encrypt [OPTIONS] PATH

Options:
  -h, --help    Prints help message
  -r, --remove  Removes the target file/directory
  -z, --zip     Zips the directory before encryption
```
```
$ kapak decrypt -h

Usage: kapak decrypt [OPTIONS] PATH

Options:
  -h, --help    Prints help message
  -r, --remove  Removes the target file/directory
```
## Examples

### Linux
```
$ kapak encrypt -z ~/new-dir
$ kapak encrypt -r ~/movie.mp4
$ kapak decrypt ~/movie.kpk
```

### Windows
```
C:\> kapak encrypt -z "C:\New folder"
C:\> kapak encrypt -r "C:\movie.mp4"
C:\> kapak decrypt "C:\movie.kpk"
```
> There is a problem with Windows paths that you might face with it.<br>
> Do NOT leave \\" or \\' at the end of the path, like ~~"C:\New folder\\"~~ .

## Password
Password length:<br> 
- min: 3 characters
- max: 1024 characters

After you run the script, it will prompt you to enter password.<br>

### There is an alternative way to provide the script with a password.
Create a file and name it `password.txt` whithin the `kapak` directory and put your password in it.
```
$ cd kapak
$ echo 'My$tr0n9P@ssw0rD' > password.txt
```
After you run the script, it will consume the `password.txt` file and will remove it after the operation is completed.

## Contribute
Feel free to contribute however you want.
