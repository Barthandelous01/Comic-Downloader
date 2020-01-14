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


# Directory variables for storage of comics

# main directory
DIRECTORY='comics'

# sub-directories
XKCD=DIRECTORY + '/xkcd'
DILBERT=DIRECTORY + '/dilbert'
FAR_SIDE=DIRECTORY + '/far_side'
GARFIELD=DIRECTORY + '/garfield'

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
            Separator('= Less-Geeky ='),
            {
                'name': 'The Far Side'
            },
            Separator('= Not Geeky ='),
            {
                'name': 'Garfield'
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

    if(not path.isdir(FAR_SIDE)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' The Far Side directory not found, creating')
        os.makedirs(FAR_SIDE)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Far side directory found')


# return soup object from url
def scrape(url):
    http = urllib3.PoolManager()
    html = http.request('GET', url)
    return BeautifulSoup(html.data, 'html.parser')

def ping():
    result = os.system('ping -c 3 archlinux.org >/dev/null')
    return result

# Get XKCD function
def get_xkcd():
    print('==> Downloading website')
    soup = scrape('https://www.xkcd.com')
    print('==> Finding image url')
    regex = re.compile(R'/comics/.*\.png')
    img_url = regex.search(str(soup))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# https://imgs.xkcd.com/' + img_url.group() + ' > ' + XKCD + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.png')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')



# Get dilbert function
def get_dilbert():
    print('==> Downloading website')
    soup = scrape('https://dilbert.com')
    print('==> Finding image url')
    regex = re.compile(R'assets.amuniversal.com/([a-f]|\d){32}')
    img_url = regex.search(str(soup))
    x = datetime.datetime.now()
    print('==> Downloading image')
    result = os.system('curl -# https://' + img_url.group() + ' > ' + DILBERT + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.png')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')

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
    result = os.system('curl -# ' + img_url.group() + ' > ' + GARFIELD + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.gif')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')

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
    result = os.system('curl -# ' + img_url.group() + ' > ' + FAR_SIDE + '/' + str(x.month) + '-' + str(x.day) + '-' + str(x.year) + '.jpg')
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')

def cli_get(test):
    check_files()
    for x in test:
        if x == 'Dilbert':
            get_dilbert()
        elif x == 'Garfield':
            get_garfield()
        elif x == 'FarSide':
            get_far_side()
        elif x == 'XKCD' | 'xkcd':
            get_xkcd()
        elif x == '-h' | '--help':
            print('Options are: Dilbert, Garfield, FarSide, (XKCD | xkcd)')
        else:
            print(Fore.RED + '::' + Style.RESET_ALL + ' Comic not known: ' + str(x))
    exit()

def main():
    # Initialize colors
    init()

    # Initialize command line args
    my_parser = argparse.ArgumentParser()
    my_parser.version = '1.0'
    my_parser.add_argument('-q', '--quiet', action='store_true', help='Turn off welcome banner') # argument for quiet connection
    my_parser.add_argument('-c', '--check', action='store_true', help='Turn off automatic directory checks (may cause errors)') # argument to disregard directory checks
    my_parser.add_argument('-d', '--download', type=str, help='Download a comic without the fancy GUI. Implies -q', nargs='+')
    my_parser.add_argument('-v', '--version', action='version', help='show version')
    args = my_parser.parse_args()


    # Do CLI download check
    if args.download != None:
        cli_get(args.download)

    # Render welcome banner
    if not args.quiet: # check for silent option
        f = Figlet(font='slant')
        print(f.renderText('Download Comics'))

    # Runs prompt code to get comics to download
    answers = prompt(questions, style=style)
    try:
        list = answers['Comics']
    except:
        print('You need to select at least one comic')
        exit()

    # Do directory check
    if not args.check: # allow for lack of directory check
        check_files()

    # check for internet
    if ping() != 0:
        print(Fore.RED + '::' + Style.RESET_ALL + ' No wifi connection. Aborting.')
        exit(1)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Wifi connection found!')
        # Run actual download code
    parse_list(list)


if __name__ == '__main__':
    main()
