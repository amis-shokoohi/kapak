# KapaK script
### A simple-to-use file encryption script
![kapak-screenshot](screenshot.png)

### Description
This script encrypts **a file** or **files whithin a directory recursively** by<br>
a given password using _AES_ symmetric encryption method.

> If you are wondering what _kapak_ means, it means _mold_.<br>
> As moldy food is not eatable, kapaky files are not readable.

- [installation](#Installation)
- [usage](#Usage)
- [examples](#Examples)
- [password](#Password)
- [contribute](#Contribute)

### Installation
Make sure Python 3 is installed.
Then run
```
pip install -r requirements.txt
```

#### If you are using _Kali_ Linux then I got you covered.
Just simply run **install.sh** and it will install the script and add it to PATH so you can run it from anywhere in your system.
```sh
$ cd kapak
$ chmod +x ./install.sh
$ ./install.sh
```
> I've only tested this on Kali Linux.
> Read the installation script before running it on other distros.

### Usage
```sh
$ kapak [-e -d] <path> -r
$ kapak -e ./test.txt -r
```
> The positions of **path** argument and **flags** are not important.

For help use `-h` or `--help` flag.<br>
For encryption mode use `-e` or `--encrypt` flag.<br>
For decryption mode use `-d` or `--decrypt` flag.<br>
If you want to remove the target files after the process then use `-r` or `--remove` flag.

### Examples

###### Windows
```sh
C:\> cd kapak
C:\kapak> python kapak.py -e "C:\New folder"
C:\kapak> python kapak.py -e "C:\movie.mp4" -r
```
> There is a problem with Windows that you might face with it.<br>
> Do NOT leave \\" or \\' at the end of the path, like ~~"C:\New folder\\"~~ .

###### Mac
```sh
$ cd kapak
$ python3 kapak.py -e ~/new-dir
$ python3 kapak.py -e ~/movie.mp4 -r
```

###### Linux
```sh
$ cd kapak
$ python3 kapak.py -e ~/new-dir
$ python3 kapak.py -e ~/movie.mp4 -r
```

###### If you installed the script with "install.sh"
```sh
$ kapak -e ~/new-dir
$ kapak -e ~/movie.mp4 -r
```

### Password
Password length:<br> 
- min: 3 characters
- max: 1024 characters


After you run the script, it will prompt you to enter password.
> Make sure to choose a strong password otherwise encryption loses its meaning.

Kapak script uses **Scrypt** key derivation methods.

<br>

#### There is an alternative way to provide the script with a password.
Create a file and name it `password.txt` whithin the `kapak` directory and put your password in it.
```sh
$ cd kapak
$ echo 'My$tr0n9P@ssw0rD' > password.txt
```
After you run the script, it will consume the `password.txt` file and will remove it after the operation is completed.

### Contribute
Feel free to contribute however you want.
