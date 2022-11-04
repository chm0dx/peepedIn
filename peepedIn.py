import argparse
from argparse import RawTextHelpFormatter
import requests
import re
import string
import sys

def scrape(company_url,user,pw):
		li_base_url = "https://www.linkedin.com/"
		li_login_url = li_base_url + "uas/authenticate"

		session = requests.Session()
		session.get(li_login_url)
		session.headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
		session.headers["Accept-Language"] = 'en-US,en;q=0.9'
		session.headers["X-Li-User-Agent"] = "LIAuthLibrary:3.2.4 com.linkedin.LinkedIn:8.8.1 iPhone:8.3"
		session.headers["X-User-Language"] = "en"
		session.headers["X-User-Locale"] = "en_US"
		session.headers["Accept-Language"] = "en-us"
		session.headers["csrf-token"] = session.cookies["JSESSIONID"].strip('"')

		data = {
					"session_key": user,
					"session_password": pw,
					"JSESSIONID": session.cookies["JSESSIONID"],
				}

		r = session.post(li_login_url, data=data)

		if r.json()['login_result'] != "PASS":
				return r.json()

		company_profile = session.get(company_url).text
		company_id = re.findall(r'urn:li:fsd_company:([0-9]*)&',company_profile)[0]
		r = session.get(f"https://www.linkedin.com/voyager/api/search/blended?count=49&filters=List(resultType-%3EPEOPLE,currentCompany-%3E{company_id})&origin=GLOBAL_SEARCH_HEADER&q=all&start=0&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY)")
		results = r.json()["elements"][0]["elements"]
		peeps = []

		for result in results:
			linkedin = result["image"]["attributes"][0]["miniProfile"]["publicIdentifier"]
			if "UNKNOWN" in linkedin:
				continue
			linkedin = f"https://linkedin.com/in/{linkedin}"
			first_name = result["image"]["attributes"][0]["miniProfile"]["firstName"]
			first_name = ''.join([char for char in first_name if char in string.printable])
			last_name = result["image"]["attributes"][0]["miniProfile"]["lastName"]
			last_name = ''.join([char for char in last_name if char in string.printable])
			title = result["image"]["attributes"][0]["miniProfile"]["occupation"]
			
			peeps.append({"first":first_name, "last":last_name, "title":title, "linkedin":linkedin})
			
		return {"results":peeps}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Return a list of employee profiles and info from a company's LinkedIn profile URL.",
        epilog = '''Example: python3 peepedIn.py url email password
        ''',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('url', help="The LinkedIn profile URL of the company you want to peep")
    parser.add_argument('email', help="The account email to use for logging into LinkedIn")
    parser.add_argument('password', help="The account password to use for logging into LinkedIn")
    parser.add_argument('-j','--json', help="Output in json format", action='store_true')
    args = parser.parse_args()

    results = scrape(args.url,args.email,args.password)
    if args.json:
        print(results)
    else:
        if results.get("results"):
            for result in results.get("results"):
                print(f'{result["first"]} {result["last"]},{result["title"]},{result["linkedin"]}')
        else:
            print(results)
            if results.get("challenge_url"):
                print("NOTE: You got a challenge. Use a browser to login into LinkedIn from the same IP you are running the script from and try again.")

# Thanks to https://github.com/nickls/linkedin-unofficial-api for API documentation