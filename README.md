# peepedIn

## NOTE: Broken at the moment due to LinkedIn changes. Working on updates soon...

Peep the LinkedIn profiles of a company's employees.

There are other ways to do this kind of thing, but this is simple, targeted to what I need it to do, and easy to integrate into other projects.

Results are limited by the connections of the account used to run the tool. Keep pumping those sock puppets! 

## Install

    git clone https://github.com/chm0dx/peepedIn.git
    cd peepedIn
    pip install -r requirements.txt
    
## Use

    usage: peepedIn.py [-h] [-j] url email password

    Return a list of employee profiles and info from a company's LinkedIn profile URL.

    positional arguments:
      url         The LinkedIn profile URL of the company you want to peep
      email       The account email to use for logging into LinkedIn
      password    The account password to use for logging into LinkedIn

    optional arguments:
      -h, --help  show this help message and exit
      -j, --json  Output in json format

    Example: python3 peepedIn.py url email password
    
## NOTE

LinkedIn doesn't love automated logins. You may be rewarded with a challenge_url before LinkedIn will complete the login. Logging in ahead of time from a browser at the same IP you will run the tool from is a good way to avoid getting hit with the challenge. I'll look to add automated handling of the challenge at some point.

## Credit

Thanks to https://github.com/nickls/linkedin-unofficial-api for API documentation
