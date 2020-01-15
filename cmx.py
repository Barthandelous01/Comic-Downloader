#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
import urllib3
import os.path
from os import path
import os
import tqdm
import colorama
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
from pyfiglet import Figlet
import re
import datetime
import argparse
import sys
import threading


# Directory variables for storage of comics

# main directory
DIRECTORY='comics'

# sub-directories
XKCD=DIRECTORY + '/xkcd'
DILBERT=DIRECTORY + '/dilbert'
FAR_SIDE=DIRECTORY + '/far_side'
GARFIELD=DIRECTORY + '/garfield'
BC=DIRECTORY + '/bc'
BLONDE=DIRECTORY + '/blonde'
BEETLE=DIRECTORY + '/beetle'

# Styling for CLI
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

# List of comics that are downloadable. Expandable, too.
questions = [
    {
        'type': 'checkbox',
        'message':'Select your comic(s)',
        'name': 'Comics',
        'choices': [
            Separator('= Geeky ='),
            {
                'name': 'XKCD'
            },
            {
                'name': 'Dilbert'
            },
            {
                'name': 'The Far Side'
            },
            Separator('= Not Geeky ='),
            {
                'name': 'Garfield'
            },
            {
                'name': 'BC'
             }
         ]
    }
]

# List parsing from the list from the prompt. Runs the get_.*() function for each comic.
def parse_list(list):
    for x in list:
        if x == 'XKCD':
            get_xkcd()
        elif x == 'Dilbert':
            get_dilbert()
        elif x == 'Garfield':
            get_garfield()
        elif x == 'The Far Side':
            get_far_side()
        elif x == 'BC':
            get_bc()

# Directory function check
def check_files():
    if(not path.isdir(XKCD)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' XKCD directory not found, creating')
        os.makedirs(XKCD)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' XKCD directory found')

    if(not path.isdir(DILBERT)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' Dilbert directory not found, creating')
        os.makedirs(DILBERT)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Dilbert directory found')

    if(not path.isdir(GARFIELD)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' Garfield directory nout found, creating')
        os.makedirs(GARFIELD)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Garfield directory found')

    if(not path.isdir(BC)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' BC directory not found, creating')
        os.makedirs(BC)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' BC directory found')

    if(not path.isdir(FAR_SIDE)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' The Far Side directory not found, creating')
        os.makedirs(FAR_SIDE)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Far side directory found')

# return soup object from url
def scrape(url):
    try:
        http = urllib3.PoolManager()
        html = http.request('GET', url)
        return BeautifulSoup(html.data, 'html.parser')
    except:
        print(Fore.RED + '::' + Style.RESET_ALL + ' An error occured. Aborting.')
        exit(1)

# Network test function
def ping(pid):
    result = os.system('ping -c 1 archlinux.org >/dev/null 2>&1')
    if result != 0:
        print(Fore.RED + '::' + Style.RESET_ALL + ' No wifi connection found.')
        os.system('kill ' + str(pid) + ' >/dev/null 2>&1') # I really hate this, but it's the only way at the moment.
                                                           # Ideally, it would raise an exception, but I can't catch it in man
                                                           # So, instead, I pass the PID of the main process to it
                                                           # When there is an error, it kills the main thread
                                                           # and then exits itself anyway.
                                                           # Sorry for the long explanation, but this pice of code is
                                                           # so crappy that I wanted to explain it. At least it's not
                                                           # a security hole.
                                                           #
                                                           # TODO: Find a better way to do this
        exit()
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Wifi connection found!')

# Get XKCD function
def get_xkcd():
    print('==> Downloading website')
    soup = scrape('https://www.xkcd.com')
    print('==> Finding image url')
    regex = re.compile(R'/comics/.*\.png')
    img_url = regex.search(str(soup))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -m 10 -# https://imgs.xkcd.com/' + img_url.group() + ' > ' + XKCD + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.png')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)



# Get dilbert function
def get_dilbert():
    print('==> Downloading website')
    soup = scrape('https://dilbert.com')
    print('==> Finding image url')
    regex = re.compile(R'assets.amuniversal.com/([a-f]|\d){32}')
    img_url = regex.search(str(soup))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# -m 10 https://' + img_url.group() + ' > ' + DILBERT + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.png')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)

# Get garfield function
def get_garfield():
    print('==> Downloading website')
    soup = scrape('https://garfield.com')
    test = soup.find('img', attrs={'class':'img-responsive'})
    print('==> Finding image url')
    regex = re.compile(R'https://.*\.gif')
    img_url = regex.search(str(test))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# -m 10 ' + img_url.group() + ' > ' + GARFIELD + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.gif')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)

# Get the far side function
def get_far_side():
    print('==> Downloading website')
    soup = scrape('https://www.thefarside.com')
    test = soup.find('picture', attrs={'class': 'tfs-splash-image__image'})
    print('==> Finding image url')
    regex = re.compile(R'https://.*\.jpg')
    img_url = regex.search(str(test))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# -m 10 ' + img_url.group() + ' > ' + FAR_SIDE + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.jpg')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)

#get BC comic function
def get_bc():
    print('==> Downloading website')
    soup = scrape('https://johnhartstudios.com/bc/')
    test = soup.find('div', attrs={'class': 'entry-content'})
    print('==> Finding image url')
    regex = re.compile(R'/bcstrips/.*\.jpg')
    img_url = regex.search(str(test))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# -m 10 https://johnhartstudios.com/' + img_url.group() + ' > ' + BC + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.jpg')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)

# CLI comic names list
def list_give():
    print('Options are:\n\tDilbert\n\tGarfield\n\tFarSide\n\tXKCD\n\tBC\n')

# CLI interface comic getting thing
def cli_get(test):
    check_files()
    for x in test:
        if x == 'Dilbert':
            get_dilbert()
        elif x == 'Garfield':
            get_garfield()
        elif x == 'FarSide':
            get_far_side()
        elif x == 'XKCD':
            get_xkcd()
        elif x == 'BC':
            get_bc()
        elif x == 'h' | 'help':
            print('Options are: Dilbert, Garfield, FarSide, XKCD, BC')
        else:
            print(Fore.RED + '::' + Style.RESET_ALL + ' Comic not known: ' + str(x))
    exit()

def main():
    # Initialize colors
    init()

    # Initialize command line args
    my_parser = argparse.ArgumentParser()
    my_parser.version = '1.1'
    my_parser.add_argument('-q', '--quiet', action='store_true', help='Turn off welcome banner') # argument for quiet connection
    my_parser.add_argument('-d', '--download', type=str, help='Download a comic without the fancy GUI. Implies -q', nargs='+')
    my_parser.add_argument('-v', '--version', action='version', help='show version')
    my_parser.add_argument('-l', '--list', action='store_true', help='list CLI args for --download')
    args = my_parser.parse_args()

    # simple handler for the -l option.
    if args.list == True:
        list_give()
        exit()

    # Do CLI download check
    if args.download != None:
        cli_get(args.download)

    # Non-thread bound ping. Increases speed!
    pi = threading.Thread(target=ping, args=(os.getpid(),))

    # Render welcome banner
    if not args.quiet: # check for silent option
        f = Figlet(font='speed')
        print(f.renderText('Download Comics'))

    # Runs prompt code to get comics to download
    answers = prompt(questions, style=style)

    # Start ping process now
    pi.start()
    # Do directory check
    check_files()

    # check for internet thread joins
    pi.join()

    # Run actual download code
    try:
        parse_list(answers['Comics'])
    except KeyboardInterrupt:
        print('==> Aborting')
        exit()


if __name__ == '__main__':
    main()
