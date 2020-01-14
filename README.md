# Comic Downloader
### The last webcomic downloading script you'll want or need.

## About
This is a full-featured python downloader CLI application to download your webcomics. Currently, both CLI-only and CLI-interactive modes exist.

## Installation
This project uses _a lot_ of prerequisites to manage all of the amazing stuff that it does. Install:
```
$ sudo pip3 install pyfiglet urllib3 PyInquirer bs4 colorama
```
Then, download the install script and run it:
```
$ sh install.sh
```
Congrats! The application should be installed.
## Usage
This is one area you have to be careful. Because of limitations imposed by `python`, there is no way to use an absolute path with this script. Therefore: __LEAVE IT IN THE SAME DIRECTORY!__ The install does not add it to `/usr/bin`, but leaves it in the home directory. __ALWAYS RUN IT FROM HERE!__

To run:
```
$ cd ~
$ ./cmx.py
```
The `-h` option will show all options.

## Breakage
The only time this application breaks is when a network change happens during this segment of output:
```
:: Comic downloaded!
==> Downloading website
```
This causes `urllib3` to throw an uncatchable error. All other exceptions are handled gracefully in their respective functions.
