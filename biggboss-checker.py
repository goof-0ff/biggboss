#!/usr/bin/env python3
#
#   Copyright (c) 2014 Shubham Chaudhary <me@shubhamchaudhary.in>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import os.path
import platform
import random
import re
import sys
import time

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
    import urllib.error as urlerror
else:
    import urllib2
    import urlparse


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split('(\d+)', text)]

def notify_user(message=None):
    ''' Notify the user about a particular event with given message
    '''
    if not message:
        message = 'Notification!!!'
    #print('-'*len(message))
    print('-'*int((len(message)-6)/2), 'NOTIFICATION', '-'*int((len(message)-6)/2))
    print(message)

def get_page_data():
    ''' Get page data as string from server
    '''
    print('Sending request to servers of Colors . . .')
    full_url = 'http://colors.in.com/in/biggboss'
    full_url = 'http://colors.in.com/in/biggboss/videos/episodes'
    # Send request
    try:
        #res.geturl(), .url=str, .status=200, .info=200, .msg=OK,
        response = urllib2.urlopen(full_url)
    except urlerror.HTTPError as exep:
        print('The server couldn\'t fulfill the request.',
              'Error code: ', exep.code)
    except urlerror.URLError as exep:
        print('We failed to reach a server.')
        print('Reason: ', exep.reason)
    else:
        # everything is fine
        #if verbose:
        print('Data received, Decoding . . .')
        web_page = str(response.read()) # More pythonic than .decode('utf-8')
        return web_page

def get_link(web_page):
    ''' Get Latest episode link
    '''
    month = time.strftime('%B')
    new_link_pattern = r'http://colors.in.com/in/biggboss/videos/bigg-boss-8-full-episode\d\d-' + month.lower() + r'-\d+\w\w-2014.*?.html'
    #print('Checking: ', new_link_pattern)
    link_reg = re.findall(new_link_pattern, web_page)
    if link_reg:
        #print(link_reg.group())
        success_set = sorted(set(link_reg), key=natural_keys)
        return success_set[-1]

def get_episode_list(web_page, new_episode_pattern=None):
    ''' Get latest episode list from webpage
    '''
    if not new_episode_pattern:
        ### PATTERN used by colors
        #<li><a title="Bigg Boss 8, Full Episode-8, 29th September, 2014"
        #href="http://colors.in.com/in/biggboss/videos/bigg-boss-8-full-episode8-29th-october-2014-69087-2.html#nav">
        #http://colors.in.com/in/biggboss/videos/bigg-boss-8-full-episode23-november-14th-2014-10101036-2.html#nav
        #Bigg Boss 8, Full Episode-8, 29th September, 2014</a></li>
        #Bigg Boss 8, Full Episode-10, October 1st, 2014</a></li>
        new_episode_pattern = time.strftime(r'%B-\d+\w\w').lower()
        month = time.strftime('%B')
        new_episode_pattern = r'Bigg Boss \d+, Full Episode-\d+, ' + month + r' \d+\w\w, 2014';
        #new_episode_pattern = r'Bigg Boss \d+, Full Episode-\d+'

    print('Checking for new episode with pattern:', new_episode_pattern)
    success = re.findall(new_episode_pattern, web_page)
    success_set = sorted(set(success), key=natural_keys)
    return success_set


def check_biggboss_episode(new_episode_pattern=None, verbose=False):
    ''' Check for the latest bigg boss episode
    '''
    web_page = get_page_data()
    if verbose:
        print('Page Received:\n', web_page)
    success_set = get_episode_list(web_page, new_episode_pattern)
    # Parse for success or failure
    print('Found:')
    for item in success_set:
        print('\t', item)
    current_date = int(time.strftime('%d'))
    current_hour = int(time.strftime('%H'))
    current_month = time.strftime('%B')

    if (current_month.lower() in success_set[-1].lower() and (
                (str(current_date) in success_set[-1] and
                    (current_hour >= 20)) or
                (str(current_date-1) in success_set[-1] and
                    (current_hour >= 0 and current_hour < 20))
                )
            ):
        msg = 'Found new episode online'
        notify_user(msg)
        latest_link = get_link(web_page)
        if latest_link:
            print('Here\'s the link: ', latest_link)
    else:
        print('No new episode right now')

def main():
    ''' Main function - Parse command line arguments
    '''
    from argparse import ArgumentParser
    parser = ArgumentParser(prog='BiggBoss-checker')
    parser.add_argument("-p", "--pattern", type=str, dest="pattern",
                        help="Search for this pattern instead of default")
    parser.add_argument("-v", "--verbose", dest="verbosity",
            action='store_true', default=False, help='Show verbose output')
    args = parser.parse_args()

    # Check input
    try:
        check_biggboss_episode(args.pattern, verbose=args.verbosity)
    except:
        raise
    return 0

if __name__ == '__main__':
    try:
        main()
        if os.name == 'nt' or platform.system() == 'Windows':
            input('Press Enter or Close the window to exit !')
    except KeyboardInterrupt:
        print('\nClosing garacefully :)', sys.exc_info()[1])
    except urlerror.HTTPError:
        print('HTTP Error:', sys.exc_info()[1])
    except SystemExit:
        pass
    except:
        print('Unexpected Error:', sys.exc_info()[0])
        print('Details:', sys.exc_info()[1])
        raise
