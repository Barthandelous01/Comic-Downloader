#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
import urllib3
import os.path
from os import path
import os
import colorama
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
from pyfiglet import Figlet
import re
import datetime
import argparse
import sys
import threading


###############
# DIRECTORIES #
###############

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
CIRCUS=DIRECTORY + '/circus'

################
# PROMPT DICTS #
################

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
            },
            {
                 'name': 'Blondie'
            },
            {
                'name': 'Beetle Bailey'
            },
            {
                'name': 'Family Circus'
            }
         ]
    }
]

# List of options for the main menu
quests = [
    {
        'type': 'checkbox',
        'message': 'Please choose your action.',
        'name': 'Options',
        'choices': [
            {
                'name': '= Display Comics ='
            },
            {
                'name': '= Remove old comics ='
            },
            {
                'name': '= Get comics ='
            }
        ]
    }
]

coms = {
    'Dilbert': DILBERT,
    'Garfield': GARFIELD,
    'The Far Side': FAR_SIDE,
    'XKCD': XKCD,
    'Blondie': BLONDE,
    'Beetle Bailey': BEETLE,
    'BC': BC,
    'Family Circus': CIRCUS
}
##################
# MAIN FUNCTIONS #
##################

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
        elif x == 'Blondie':
            get_blonde()
        elif x == 'Beetle Bailey':
            get_beetle()
        elif x == 'Family Circus':
            get_circus()

# file check function
def check_dir(directory, name):
    if(not path.isdir(directory)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' ' + name + ' directory not found, creating')
        os.makedirs(directory)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' ' + name + ' directory found')

# Directory function check
def check_files():
    for x in coms:
        check_dir(x, coms[x])

# Network test function
def ping(pid):
    result = os.system('ping -c 1 archlinux.org >/dev/null 2>&1')
    if result != 0:
        print(Fore.RED + '::' + Style.RESET_ALL + ' No wifi connection found.')
        os.system('kill ' + str(pid) + ' >/dev/null 2>&1') # I really hate this, but it's the only way at the moment.
                                                           # Ideally, it would raise an exception, but I can't catch it in main
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

################################
# GET COMIC FUNCTION FUNCTIONS #
################################

# return soup object from url
def scrape(url):
    try:
        http = urllib3.PoolManager()
        html = http.request('GET', url)
        return BeautifulSoup(html.data, 'html.parser')
    except:
        print(Fore.RED + '::' + Style.RESET_ALL + ' An error occured. Aborting.')
        exit(1)

# find comic function
def get_url(reg, soup):
    regex = re.compile(reg)
    return regex.search(str(soup))

# download comic function
def curl_comic(url, directory, extention):
    x = datetime.datetime.now()
    result = os.system('curl -# -m 10 ' + '\'' + url + '\'' + ' > ' + directory + '/' +  str(x.month) + '-' + str(x.day) + '-' + str(x.year) + extention)
    if result == 0:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Comic downloaded!')
    else:
        print(Fore.RED + '::' + Style.RESET_ALL + ' Error encountered. Comic not downloaded.')
        exit(1)

#######################
# GET COMIC FUNCTIONS #
#######################

# Get XKCD function
def get_xkcd():
    print('==> Downloading website')
    soup = scrape('https://www.xkcd.com')
    print('==> Finding image url')
    img_url = get_url(R'/comics/.*\.png', soup)
    print('==> Downloading image')
    total = 'https://imgs.xkcd.com/' + img_url.group()
    curl_comic(total, XKCD, '.png')

# Get dilbert function
def get_dilbert():
    print('==> Downloading website')
    soup = scrape('https://dilbert.com')
    print('==> Finding image url')
    img_url = get_url(R'assets.amuniversal.com/([a-f]|\d){32}', soup)
    print('==> Downloading image')
    total = 'https://' + img_url.group()
    curl_comic(total, DILBERT, '.png')

# Get garfield function
def get_garfield():
    print('==> Downloading website')
    soup = scrape('https://garfield.com')
    test = soup.find('img', attrs={'class':'img-responsive'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*\.gif', test)
    print('==> Downloading image')
    curl_comic(img_url.group(), GARFIELD, '.gif')

# Get the far side function
def get_far_side():
    print('==> Downloading website')
    soup = scrape('https://www.thefarside.com')
    test = soup.find('picture', attrs={'class': 'tfs-splash-image__image'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*\.jpg', test)
    print('==> Downloading image')
    curl_comic(img_url.group(), FAR_SIDE, '.jpg')

#get BC comic function
def get_bc():
    print('==> Downloading website')
    soup = scrape('https://johnhartstudios.com/bc/')
    test = soup.find('div', attrs={'class': 'entry-content'})
    print('==> Finding image url')
    img_url = get_url(R'/bcstrips/.*\.jpg', test)
    print('==> Downloading image')
    total = 'https://johnhartstudios.com/' + img_url.group()
    curl_comic(total, BC, '.jpg')

# Get comic from comickingdom function
def get_comic_kingdom(comic_name, directory, extention):
    print('==> Downloading website')
    soup = scrape('https://www.comicskingdom.com/' + comic_name)
    total = soup.find('div', attrs={'id':'comic-slider'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*;file=[a-zA-Z0-9]*=?', total)
    img = re.sub(R'\&amp;', '&', img_url.group())
    print('==> Downloading image')
    curl_comic(img, directory, extention)

def get_blonde():
    get_comic_kingdom('blondie', BLONDE, '.gif')

def get_beetle():
    get_comic_kingdom('beetle-bailey-1', BEETLE, '.gif')

def get_circus():
    get_comic_kingdom('family-circus', CIRCUS, '.gif')

#########################
# CLI COMMAND FUNCTIONS #
#########################

# CLI comic names list
def list_give():
    print('Options are:\n\tDilbert\n\tGarfield\n\tFarSide\n\tXKCD\n\tBC\n\tBlondie\n\tBeetleBailey\n\tFamilyCircus')

# CLI interface comic getting thing
def cli_get(test):
    # Non thread-bound ping. Increases speed!
    pi = threading.Thread(target=ping, args=(os.getpid(),))
    # Start ping
    pi.start()
    # Quick conncurrent directory check and wifi check finish
    check_files()
    pi.join()
    # Iterate over all options and download them
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
        elif x == 'Blondie':
            get_blonde()
        elif x == 'BeetleBailey':
            get_beetle()
        elif x == 'FamilyCircus':
            get_circus()
        else:
            print(Fore.RED + '::' + Style.RESET_ALL + ' Comic not known: ' + str(x))
    exit()

def term_download():
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


def main():
    # Initialize colors
    init()

    # Initialize command line args
    my_parser = argparse.ArgumentParser()
    my_parser.version = '1.3'
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

    term_download()


if __name__ == '__main__':
    main()
