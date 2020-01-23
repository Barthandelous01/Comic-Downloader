#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
import urllib3
import os
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
from pyfiglet import Figlet
import re
import datetime
import argparse
import threading
import webbrowser as wb

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
                'name': '= Remove old comics ='
            },
            {
                'name': '= Get comics ='
            },
            {
                'name': '= Display Comics ='
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

def banner(args):
    """
    Renders welcome banner.
    Uses silent option.
    """
    if not args.quiet: # check for silent option
        f = Figlet(font='speed')
        print(f.renderText('Download Comics'))

def rem_old(list_arg):
    """
    Removes old comics (ones that aren't todays)
    Helps users save disk space.
    """
    for x in list_arg:
        os.system('rm ' + coms[x] + '/* >/dev/null 2>&1')
        print('==> cleaned ' + coms[x])

def get_date():
    """
    Returns a date object in the format used by curl_comic()
    """
    x = datetime.datetime.now()
    date = str(x.month) + '-' + str(x.day) + '-' + str(x.day)
    return date

def show_comics(list_arg):
    """
    Wrapper function for displaying all comics from a list
    """
    for x in list_arg:
        display_comics(coms[x])

def display_comics(comic):
    """
    Displays comics in webbrowser using REGEXES!
    """
    dirs = os.popen('ls ' + str(comic)).read()
    regex = re.compile(R'\d{1,2}-\d{1,2}-\d{4}\.(jpg|gif|png)')
    name = regex.search(dirs)
    wb.open(os.getcwd() + '/' + comic + '/' + name.group())
    # print(os.getcwd() + '/' + comic + '/' + name.group()) This can be un-commented for use in debugging
    print('==> Comic opened!')

def term_download(args):
    """
    Terminal download; 2nd half of main
    """
    # Non-thread bound ping. Increases speed!
    pi = threading.Thread(target=ping, args=(os.getpid(),))

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

# List parsing from the list from the prompt. Runs the get_.*() function for each comic.
def parse_list(list_arg):
    """
    List parses from the prompt for downloading comics.
    Runs the get_.*() function for each comic.
    """
    for x in list_arg:
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
    """
    Checks the individual functions
    """
    if(not os.path.isdir(directory)):
        print(Fore.RED + '::' + Style.RESET_ALL + ' ' + name + ' directory not found, creating')
        os.makedirs(directory)
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' ' + name + ' directory found')

# Directory function check
def check_files():
    """
    Directory check wrapper
    """
    for x in coms:
        check_dir(coms[x], x)

# Network test function
def ping(pid):
    """
    I really hate this, but it's the only way at the moment.
    Ideally, it would raise an exception, but I can't catch it in main
    So, instead, I pass the PID of the main process to it
    When there is an error, it kills the main thread
    and then exits itself anyway.
    Sorry for the long explanation, but this pice of code is
    so crappy that I wanted to explain it. At least it's not
    a security hole.
    TODO: Find a better way to do this
    """
    result = os.system('ping -c 1 archlinux.org >/dev/null 2>&1')
    if result != 0:
        print(Fore.RED + '::' + Style.RESET_ALL + ' No wifi connection found.')
        os.system('kill ' + str(pid) + ' >/dev/null 2>&1')
        exit()
    else:
        print(Fore.GREEN + '::' + Style.RESET_ALL + ' Wifi connection found!')

################################
# GET COMIC FUNCTION FUNCTIONS #
################################

def scrape(url):
    """
    Scrapes the provided uRL and returns a BS4 object.
    """
    try:
        http = urllib3.PoolManager()
        html = http.request('GET', url)
        return BeautifulSoup(html.data, 'html.parser')
    except: # catch *all* errors
        print(Fore.RED + '::' + Style.RESET_ALL + ' An error occured. Aborting.')
        exit(1)

def get_url(reg, soup):
    """
    Shorthand to find comic urls from a BS4 object.
    """
    regex = re.compile(reg)
    return regex.search(str(soup))

def curl_comic(url, directory, extention):
    """
    Takes a url,
    the respective directory,
    and image extention,
    and saves the image.
    """
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

def get_xkcd():
    """
    Get xkcd function
    """
    print('==> Downloading website')
    soup = scrape('https://www.xkcd.com')
    print('==> Finding image url')
    img_url = get_url(R'/comics/.*\.png', soup)
    print('==> Downloading image')
    total = 'https://imgs.xkcd.com/' + img_url.group()
    curl_comic(total, XKCD, '.png')

def get_dilbert():
    """
    Get dilbert function
    """
    print('==> Downloading website')
    soup = scrape('https://dilbert.com')
    print('==> Finding image url')
    img_url = get_url(R'assets.amuniversal.com/([a-f]|\d){32}', soup)
    print('==> Downloading image')
    total = 'https://' + img_url.group()
    curl_comic(total, DILBERT, '.png')

def get_garfield():
    """
    Get garfield function
    """
    print('==> Downloading website')
    soup = scrape('https://garfield.com')
    test = soup.find('img', attrs={'class':'img-responsive'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*\.gif', test)
    print('==> Downloading image')
    curl_comic(img_url.group(), GARFIELD, '.gif')

def get_far_side():
    """
    Get the Far Side function
    """
    print('==> Downloading website')
    soup = scrape('https://www.thefarside.com')
    test = soup.find('picture', attrs={'class': 'tfs-splash-image__image'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*\.jpg', test)
    print('==> Downloading image')
    curl_comic(img_url.group(), FAR_SIDE, '.jpg')

def get_bc():
    """
    Get BC function
    """
    print('==> Downloading website')
    soup = scrape('https://johnhartstudios.com/bc/')
    test = soup.find('div', attrs={'class': 'entry-content'})
    print('==> Finding image url')
    img_url = get_url(R'/bcstrips/.*\.jpg', test)
    print('==> Downloading image')
    total = 'https://johnhartstudios.com/' + img_url.group()
    curl_comic(total, BC, '.jpg')

def get_comic_kingdom(comic_name, directory, extention):
    """
    Wrapper function for comic kingdom sites. Passed arguments and wrapped to different comics.
    """
    print('==> Downloading website')
    soup = scrape('https://www.comicskingdom.com/' + comic_name)
    total = soup.find('div', attrs={'id':'comic-slider'})
    print('==> Finding image url')
    img_url = get_url(R'https://.*;file=[a-zA-Z0-9]*=?', total)
    img = re.sub(R'\&amp;', '&', img_url.group())
    print('==> Downloading image')
    curl_comic(img, directory, extention)

def get_blonde():
    """
    Blondie wrapper for comic kingdom.
    """
    get_comic_kingdom('blondie', BLONDE, '.gif')

def get_beetle():
    """
    Beetle wrapper for comic kingdom.
    """
    get_comic_kingdom('beetle-bailey-1', BEETLE, '.gif')

def get_circus():
    """
    Family Circus wrapper for comic kingdom.
    """
    get_comic_kingdom('family-circus', CIRCUS, '.gif')

#########################
# CLI COMMAND FUNCTIONS #
#########################

def list_give():
    """
    Lists options for CLI download.
    """
    print('Options are:\n\tDilbert\n\tGarfield\n\tFarSide\n\tXKCD\n\tBC\n\tBlondie\n\tBeetleBailey\n\tFamilyCircus')

def cli_get(test):
    """
    ClI 'main' function.
    Does everything term_download does, but without the GUI part.
    """
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

########
# MAIN #
########

def main():
    """
    It's main. Doesn't really need a docstring.
    """
    # Initialize command line args
    my_parser = argparse.ArgumentParser()
    my_parser.version = '1.4'
    my_parser.add_argument('-q', '--quiet', action='store_true', help='Turn off welcome banner') # argument for quiet connection
    my_parser.add_argument('-d', '--download', type=str, help='Download a comic without the fancy GUI. Implies -q', nargs='+')
    my_parser.add_argument('-v', '--version', action='version', help='show version')
    my_parser.add_argument('-l', '--list', action='store_true', help='list CLI args for --download')
    args = my_parser.parse_args()

    # Initialize colors
    init()

    # simple handler for the -l option.
    if args.list is True:
        list_give()
        exit()

    # Do CLI download check
    if args.download is not None:
        cli_get(args.download)

    # render banner
    banner(args)

    # Do main menu choice
    ans = prompt(quests, style=style)

    # Iterate over all available menu options
    try:
        for pos in ans['Options']:
            if pos == '= Remove old comics =':
                try:
                    ans2 = prompt(questions, style=style)
                except KeyError:
                    exit()
                rem_old(ans2['Comics'])
            elif pos == '= Get comics =':
                term_download(args)
            elif pos == '= Display Comics =':
                li = prompt(questions, style=style)
                print('[WIP] This function is a Work-In-Progress. Unfortunately, the webbrwser.open() may not function on your machine.\
                Sorry for the inconvenience this may cause.')
                show_comics(li['Comics'])
                exit()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
