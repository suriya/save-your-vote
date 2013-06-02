
from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import logging
import sys
logger = logging.getLogger(__name__)

FIELDS = [
    None,
    'ac_number',
    'ac_name',
    'part_number',
    'serial_number',
    'voter_first_name',
    'voter_last_name',
    'relative_first_name',
    'relative_last_name',
    'sex',
    'age',
]

KARNATAKA_CEO_URL = 'http://www.ceokarnataka.kar.nic.in/SearchWithEpicNo_New.aspx'
VIEWSTATE = "/wEPDwULLTE1NTEzMjAxODcPZBYCZg9kFgICAw9kFgICAw9kFgYCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQhkaXN0bmFtZR4ORGF0YVZhbHVlRmllbGQFBmRpc3Rubx4LXyFEYXRhQm91bmRnZBAVHwotLVNlbGVjdC0tI+CyrOCyvuCyl+CysuCyleCzi+Cyn+CzhiAvIEJBR0FMS09UJOCyrOCzgy7gsqzgs4Yu4LKuLuCyquCyviAvIEJBTkdBTE9SRUbgsqzgs4bgsoLgspfgsrPgs4LgsrDgs4Eg4LKX4LON4LKw4LK+4LKu4LK+4LKC4LKk4LKwIC8gQkFOR0FMT1JFIFJVUkFMH+CyrOCzhuCys+Cyl+CyvuCyteCyvyAvIEJFTEdBVU0f4LKs4LKz4LON4LKz4LK+4LKw4LK/IC8gQkVMTEFSWRrgsqzgs4DgsqbgsrDgs43igIwgLyBCSURBUh/gsrXgsr/gspzgsr7gsqrgs4LgsrAgLyBCSUpBUFVSK+CymuCyvuCyruCysOCyvuCynOCyqOCyl+CysCAvIENIQU1BUkFKTkFHQVI44LKa4LK/4LKV4LON4LKV4LKs4LKz4LON4LKz4LK+4LKq4LOB4LKwIC8gQ0hJS0tBQkFMTEFQVVIv4LKa4LK/4LKV4LON4LKV4LKu4LKX4LKz4LOC4LKw4LOBIC8gQ0hJS01BR0FMVVIs4LKa4LK/4LKk4LON4LKw4LKm4LOB4LKw4LON4LKXIC8gQ0hJVFJBRFVSR0E14LKm4LKV4LON4LK34LK/4LKjIOCyleCyqOCzjeCyqOCyoSAvIERBS1NISU5BIEtBTk5BREEk4LKm4LK+4LK14LKj4LKX4LOG4LKw4LOGIC8gREFWQU5HRVJFHOCyp+CyvuCysOCyteCyvuCyoSAvIERIQVJXQUQR4LKX4LKm4LKXIC8gR0FEQUcj4LKX4LOB4LKy4LKs4LKw4LON4LKX4LK+IC8gR1VMQkFSR0EV4LK54LK+4LK44LKoIC8gSEFTU0FOG+CyueCyvuCyteCzh+CysOCyvyAvIEhBVkVSSRjgspXgs4rgsqHgspfgs4EgLyBLT0RBR1UX4LKV4LOL4LKy4LK+4LKwIC8gS09MQVIb4LKV4LOK4LKq4LON4LKq4LKzIC8gS09QUEFMGOCyruCyguCyoeCzjeCyryAvIE1BTkRZQRvgsq7gs4jgsrjgs4LgsrDgs4EgLyBNWVNPUkUf4LKw4LK+4LKv4LKa4LOC4LKw4LOBIC8gUkFJQ0hVUiPgsrDgsr7gsq7gsqjgspfgsrDgsoIgLyBSQU1BTkFHQVJBTSLgsrbgsr/gsrXgsq7gs4rgspfgs43gspcgLyBTSElNT0dBHuCypOCzgeCyruCyleCzguCysOCzgSAvIFRVTUtVUhfgsongsqHgs4Hgsqrgsr8gLyBVRFVQSTDgsongsqTgs43gsqTgsrAg4LKV4LKo4LON4LKo4LKhIC8gVVRUQVJBIEtBTk5BREEe4LKv4LK+4LKm4LKX4LK/4LKw4LK/IC8gWUFER0lSFR8CLTEBMgIyMQIyMgExAjEyATUBMwIyOQIxOQIxNwIxMwIyNgIxNAE5ATgBNAIyNQIxMQIyNwIyMAE3AjI0AjI4ATYCMjMCMTUCMTgCMTYCMTACMzUUKwMfZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAg8PPCsADQBkAhUPZBYCAgEPZBYCZg9kFgICAQ88KwAPAGQYAgUhY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRlRGV0YWlsD2dkBSNjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJEdyaWRWaWV3MQ88KwAKAgYVBgVTbG5ObwNzZXgJRmlyc3ROYW1lDVJlbF9GaXJzdE5hbWUEQUNOTwZQYXJ0Tm8IAv////8PZA=="

def getField(td):
    font = td.font
    if not font:
        return None
    else:
        return font.get_text()

def parse_karnataka_response(existing_voter, html):
    """
    Parse Karnataka CEO website's response and return a populated
    'existing_voter'. If parsing fails, return None.

    BeautifulSoup does not parse the Karnataka CEO's website. So, we have
    to resort to all sorts of painful code.
    """
    lines = html.split('\n')
    found = [ i for (i, line) in enumerate(lines) if ('AssemblyConstituency' in line) ]
    if len(found) != 1:
        return None
    idx = found[0]
    table_code = '\n'.join(lines[(idx-2):(idx+7)])
    soup = BeautifulSoup(table_code)
    trs = soup.find_all('tr')
    if len(trs) != 2:
        return None
    tr = trs[1]
    tds = tr.find_all('td')
    if len(tds) != len(FIELDS):
        return None
    for (key, td) in zip(FIELDS, tds):
        if not key: continue
        setattr(existing_voter, key, getField(td))
    existing_voter.save()
    return existing_voter

#     datadict = [ ('__EVENTTARGET', ''),
#             ('__EVENTARGUMENT', ''),
#             ('__VIEWSTATE', VIEWSTATE),
#             ('ctl00%24ContentPlaceHolder1%24ddlDistrict', 21),
#             ('ctl00%24ContentPlaceHolder1%24txtEpic', 'ZBG6433064'),
# #             ('ctl00%24ContentPlaceHolder1%24ddlDistrict', str(district.number))
# #             ('ctl00%24ContentPlaceHolder1%24txtEpic', unicode(epic).encode('ascii', 'ignore')),
#             ('ctl00%24ContentPlaceHolder1%24btnSearch', 'Search')
#            ]

def check_karnataka_epic(existing_voter):
    epic_string = unicode(existing_voter.epic_number).encode('ascii', 'ignore')
    datadict = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': VIEWSTATE,
        'ctl00$ContentPlaceHolder1$ddlDistrict': existing_voter.district.number,
        'ctl00$ContentPlaceHolder1$txtEpic': epic_string,
        'ctl00$ContentPlaceHolder1$btnSearch': 'Search',
    }
    try:
        r = requests.post(KARNATAKA_CEO_URL, datadict, timeout=8)
    except requests.exceptions.ConnectionError as e:
        logger.warning('Error connecting to Karnataka CEO website: %s' % e)
        return None
    except requests.exceptions.HTTPError as e:
        logger.warning('HTTPError: %s' % e)
        return None
    except requests.exceptions.Timeout as e:
        logger.warning('Timeout error: %s' % e)
        return None
    except requests.exceptions.TooManyRedirects as e:
        logger.warning('Too many redirects: %s' % e)
        return None
    except:
        logger.error("Unexpected error: %s" % sys.exc_info()[0])
        raise
    existing_voter = parse_karnataka_response(existing_voter, r.content)
    if existing_voter:
        logger.info('Saved voter details for EPIC: %s' % epic_string)
    return existing_voter
