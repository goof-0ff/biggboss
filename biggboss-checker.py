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

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
    import urllib.error as urlerror
else:
    import urllib2
    import urlparse


def notify_user(message=None):
    ''' Notify the user about a particular event with given message
    '''
    if not message:
        message = 'Notification!!!'
    #print('-'*len(message))
    print('-'*int((len(message)-6)/2), 'NOTIFICATION', '-'*int((len(message)-6)/2))
    print(message)

def check_biggboss_episode(new_episode_pattern=None,verbose=False):
    ''' Check for the latest bigg boss episode
    '''
    print('Sending request to servers of Colors . . .')
    full_url = 'http://colors.in.com/in/biggboss'
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
        the_page = response.read().decode('utf-8')
        if verbose:
            print('Page Received:\n', the_page)
        # Parse for success or failure
        print('Checking for new episode')
        if not new_episode_pattern:
            new_episode_pattern = 'october-7th'
        success = re.search(new_episode_pattern, the_page)
        if success:
            msg = 'Found new episode online'
            notify_user(msg)
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
