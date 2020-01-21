# Comic Downloader
## The last webcomic downloading script you'll want or need

## About
This is a full-featured python downloader CLI application to download your webcomics. Currently, both CLI-only and CLI-interactive modes exist.

## Installation
This project uses _a lot_ of prerequisites to manage all of the amazing stuff that it does. Install:
```
$ sudo pip3 install pyfiglet urllib3 PyInquirer bs4 colorama
```
Then, download the script and put it in the directory you want.
Congrats! The application should be installed.
## Usage
This is one area you have to be careful. Because of limitations imposed by `python`, there is no way to use an absolute path with this script. Therefore: __LEAVE IT IN THE SAME DIRECTORY!__ The install does not add it to `/usr/bin`, but leaves it in the home directory, or wherever else you put it. __ALWAYS RUN IT FROM HERE!__

To run:
```sh
$ cd /path/to/cmx.py
$ ./cmx.py
```
The `-h` option will show all options.

## Breakage
All errors and exceptions that can be raised, whether they be `KeyboardInterrupt`s, `gaisocket.error`s, or what have you-s, have been handled elegantly and gracefully. 
The only thing that is inelegant (though its effects are beautiful) is the termination of the code through a lack of internet. Read the extensive comment in the function `ping(pid)` for more information..
