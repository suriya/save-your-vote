
"""
Communicate with the Chief Electoral Officer's websites of various states.

>>> import json
>>> d = KA_Client.get_voter_info(21, 'ZBG6433064')
>>> print json.dumps(d, sort_keys=True, indent=2)
{
  "ac_name": "Byatarayanapura", 
  "ac_number": "152", 
  "age": "30", 
  "part_number": "246", 
  "relative_first_name": "Subramanian", 
  "relative_last_name": "Panchapakesan", 
  "serial_number": "1994", 
  "sex": "M", 
  "voter_first_name": "Suriya", 
  "voter_last_name": "Subramanian"
}
>>> d = DL_Client.get_voter_info(0, 'XVX0000075')
>>> print json.dumps(d, sort_keys=True, indent=2)
{
  "ac_number": "1", 
  "age": "37", 
  "part_number": "1", 
  "relative_first_name": "MUKESH", 
  "relative_last_name": "KUMAR", 
  "relative_name": "MUKESH KUMAR", 
  "serial_number": "8", 
  "sex": "Female", 
  "voter_first_name": "SHISHAN", 
  "voter_last_name": "KAUR", 
  "voter_name": "SHISHAN KAUR"
}
>>> d = TN_Client.get_voter_info(0, 'AYR0562041')
>>> print json.dumps(d, sort_keys=True, indent=2)
{
  "ac_name": "1 - Gummidipoondi", 
  "part_number": "1", 
  "relative_first_name": "", 
  "relative_last_name": "Shankar", 
  "relative_name": "Shankar", 
  "serial_number": "13", 
  "sex": "Female", 
  "voter_first_name": "", 
  "voter_last_name": "Sandhiya", 
  "voter_name": "Sandhiya"
}
"""

from bs4 import BeautifulSoup
import re
import urllib
import urllib2
import requests
import logging
import sys
import textwrap
logger = logging.getLogger(__name__)

class CEOClientException(Exception):
    MESSAGE = ''
    def __str__(self):
        return self.MESSAGE

class ConnectionError(CEOClientException):
    MESSAGE = textwrap.dedent(
    """
    Unable to connect to the Chief Election Commissioner's website.
    Probably the site is down. We will try connecting later and updating
    the record.
    """)

class FailedToParseError(CEOClientException):
    MESSAGE = textwrap.dedent(
    """
    Received a response from the Chief Election Commissioner's website, but
    unable to retrive the correct data. It could be that the Voter ID given
    is incorrect. We will look to see if this is an error on our part, and
    if so, update the record.
    """)

class UnsupportedState(CEOClientException):
    MESSAGE = textwrap.dedent(
    """
    Save Your Vote is yet to implement support for your state. We will get
    to it as soon as possible and update this record.
    """)

class CEOClient:
    @classmethod
    def record_voter_info(klass, existing_voter):
        state = existing_voter.district.state.shortcode
        client = CEO_CLIENTS.get(state, None)
        if not client:
            raise UnsupportedState()
        district_number = existing_voter.district.number
        epic_string = unicode(existing_voter.epic_number).encode('ascii', 'ignore')
        info = client.get_voter_info(district_number, epic_string)
        for (key, value) in info.iteritems():
            setattr(existing_voter, key, value)
        existing_voter.save()
        logger.info('Saved voter details for EPIC: %s' % epic_string)
        return existing_voter

    @classmethod
    def get_voter_info(klass, district_number, epic_string):
        html = klass.get_html_data(district_number, epic_string)
        return klass.parse_html_data(html)

    @classmethod
    def request_params(klass, district_number, epic_string):
        raise NotImplementedError("CEOClient.request_params")

    @classmethod
    def get_html_data(klass, district_number, epic_string):
        datadict = klass.request_params(district_number, epic_string)
        try:
            r = requests.post(klass.CEO_URL, datadict, timeout=8)
        except requests.exceptions.ConnectionError as e:
            logger.warning('Error connecting to CEO website: %s' % e)
            raise ConnectionError()
        except requests.exceptions.HTTPError as e:
            logger.warning('HTTPError: %s' % e)
            raise ConnectionError()
        except requests.exceptions.Timeout as e:
            logger.warning('Timeout error: %s' % e)
            raise ConnectionError()
        except requests.exceptions.TooManyRedirects as e:
            logger.warning('Too many redirects: %s' % e)
            raise ConnectionError()
        except:
            logger.error("Unexpected error: %s" % sys.exc_info()[0])
            raise ConnectionError()
        return r.content

    @classmethod
    def parse_html_data(klass, html):
        raise NotImplementedError("CEOClient.parse_html_data")

    @classmethod
    def split_name(klass, name):
        """
        >>> CEOClient.split_name('SHISHAN KAUR')
        ('SHISHAN', 'KAUR')
        """
        if not name:
            return (None, None)
        if not isinstance(name, basestring):
            return (None, None)
        subnames = name.strip().split()
        l = len(subnames)
        first_name = ' '.join(subnames[0:(l/2)])
        last_name = ' '.join(subnames[(l/2):l])
        return (first_name, last_name)

    @classmethod
    def cleanup_names(klass, data):
        """
        Convert the dict from what the website gave us to what our database
        can store.
        >>> import json
        >>> d = { 'voter_name': 'SHISHAN KAUR', 'relative_name': 'MUKESH KUMAR' }
        >>> d = CEOClient.cleanup_names(d)
        >>> print json.dumps(d, sort_keys=True, indent=2)
        {
          "relative_first_name": "MUKESH", 
          "relative_last_name": "KUMAR", 
          "relative_name": "MUKESH KUMAR", 
          "voter_first_name": "SHISHAN", 
          "voter_last_name": "KAUR", 
          "voter_name": "SHISHAN KAUR"
        }
        """
        (voter_first_name, voter_last_name) = klass.split_name(data['voter_name'])
        (relative_first_name, relative_last_name) = klass.split_name(data['relative_name'])
        data['voter_first_name'] = voter_first_name
        data['voter_last_name'] = voter_last_name
        data['relative_first_name'] = relative_first_name
        data['relative_last_name'] = relative_last_name
        return data


class KA_Client(CEOClient):
    CEO_URL = 'http://www.ceokarnataka.kar.nic.in/SearchWithEpicNo_New.aspx'

    VIEWSTATE = "/wEPDwULLTE1NTEzMjAxODcPZBYCZg9kFgICAw9kFgICAw9kFgYCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQhkaXN0bmFtZR4ORGF0YVZhbHVlRmllbGQFBmRpc3Rubx4LXyFEYXRhQm91bmRnZBAVHwotLVNlbGVjdC0tI+CyrOCyvuCyl+CysuCyleCzi+Cyn+CzhiAvIEJBR0FMS09UJOCyrOCzgy7gsqzgs4Yu4LKuLuCyquCyviAvIEJBTkdBTE9SRUbgsqzgs4bgsoLgspfgsrPgs4LgsrDgs4Eg4LKX4LON4LKw4LK+4LKu4LK+4LKC4LKk4LKwIC8gQkFOR0FMT1JFIFJVUkFMH+CyrOCzhuCys+Cyl+CyvuCyteCyvyAvIEJFTEdBVU0f4LKs4LKz4LON4LKz4LK+4LKw4LK/IC8gQkVMTEFSWRrgsqzgs4DgsqbgsrDgs43igIwgLyBCSURBUh/gsrXgsr/gspzgsr7gsqrgs4LgsrAgLyBCSUpBUFVSK+CymuCyvuCyruCysOCyvuCynOCyqOCyl+CysCAvIENIQU1BUkFKTkFHQVI44LKa4LK/4LKV4LON4LKV4LKs4LKz4LON4LKz4LK+4LKq4LOB4LKwIC8gQ0hJS0tBQkFMTEFQVVIv4LKa4LK/4LKV4LON4LKV4LKu4LKX4LKz4LOC4LKw4LOBIC8gQ0hJS01BR0FMVVIs4LKa4LK/4LKk4LON4LKw4LKm4LOB4LKw4LON4LKXIC8gQ0hJVFJBRFVSR0E14LKm4LKV4LON4LK34LK/4LKjIOCyleCyqOCzjeCyqOCyoSAvIERBS1NISU5BIEtBTk5BREEk4LKm4LK+4LK14LKj4LKX4LOG4LKw4LOGIC8gREFWQU5HRVJFHOCyp+CyvuCysOCyteCyvuCyoSAvIERIQVJXQUQR4LKX4LKm4LKXIC8gR0FEQUcj4LKX4LOB4LKy4LKs4LKw4LON4LKX4LK+IC8gR1VMQkFSR0EV4LK54LK+4LK44LKoIC8gSEFTU0FOG+CyueCyvuCyteCzh+CysOCyvyAvIEhBVkVSSRjgspXgs4rgsqHgspfgs4EgLyBLT0RBR1UX4LKV4LOL4LKy4LK+4LKwIC8gS09MQVIb4LKV4LOK4LKq4LON4LKq4LKzIC8gS09QUEFMGOCyruCyguCyoeCzjeCyryAvIE1BTkRZQRvgsq7gs4jgsrjgs4LgsrDgs4EgLyBNWVNPUkUf4LKw4LK+4LKv4LKa4LOC4LKw4LOBIC8gUkFJQ0hVUiPgsrDgsr7gsq7gsqjgspfgsrDgsoIgLyBSQU1BTkFHQVJBTSLgsrbgsr/gsrXgsq7gs4rgspfgs43gspcgLyBTSElNT0dBHuCypOCzgeCyruCyleCzguCysOCzgSAvIFRVTUtVUhfgsongsqHgs4Hgsqrgsr8gLyBVRFVQSTDgsongsqTgs43gsqTgsrAg4LKV4LKo4LON4LKo4LKhIC8gVVRUQVJBIEtBTk5BREEe4LKv4LK+4LKm4LKX4LK/4LKw4LK/IC8gWUFER0lSFR8CLTEBMgIyMQIyMgExAjEyATUBMwIyOQIxOQIxNwIxMwIyNgIxNAE5ATgBNAIyNQIxMQIyNwIyMAE3AjI0AjI4ATYCMjMCMTUCMTgCMTYCMTACMzUUKwMfZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAg8PPCsADQBkAhUPZBYCAgEPZBYCZg9kFgICAQ88KwAPAGQYAgUhY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRlRGV0YWlsD2dkBSNjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJEdyaWRWaWV3MQ88KwAKAgYVBgVTbG5ObwNzZXgJRmlyc3ROYW1lDVJlbF9GaXJzdE5hbWUEQUNOTwZQYXJ0Tm8IAv////8PZA=="

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

    @classmethod
    def request_params(klass, district_number, epic_string):
        return {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': klass.VIEWSTATE,
            'ctl00$ContentPlaceHolder1$ddlDistrict': district_number,
            'ctl00$ContentPlaceHolder1$txtEpic': epic_string,
            'ctl00$ContentPlaceHolder1$btnSearch': 'Search',
        }

    @classmethod
    def getField(klass, td):
        font = td.font
        if not font:
            return None
        else:
            return font.get_text()

    @classmethod
    def parse_html_data(klass, html):
        """
        Parse Karnataka CEO website's response and return a dictionary of
        various fields. If parsing fails, raise exception.

        BeautifulSoup does not parse the Karnataka CEO's website. So, we have
        to resort to all sorts of painful code.
        """
        lines = html.split('\n')
        found = [ i for (i, line) in enumerate(lines) if ('AssemblyConstituency' in line) ]
        if len(found) != 1:
            raise FailedToParseError()
        idx = found[0]
        table_code = '\n'.join(lines[(idx-2):(idx+7)])
        soup = BeautifulSoup(table_code)
        trs = soup.find_all('tr')
        if len(trs) != 2:
            raise FailedToParseError()
        tr = trs[1]
        tds = tr.find_all('td')
        if len(tds) != len(klass.FIELDS):
            raise FailedToParseError()
        return { key: klass.getField(td) for (key, td) in zip(klass.FIELDS, tds) if key }

class DL_Client(CEOClient):
    CEO_URL = 'http://ceodelhi.gov.in/OnlineErms/ElectorSearchIdCard.aspx'
    VIEWSTATE = "/wEPDwULLTEwNTA3NTE4OTcPZBYCZg9kFgICAw9kFgQCBQ88KwANAgAPFgIeC18hRGF0YUJvdW5kZ2QMFCsACAUbMDowLDA6MSwwOjIsMDozLDA6NCwwOjUsMDo2FCsAAhYMHgRUZXh0BR9Lbm93IFlvdXIgQXNzZW1ibHkgQ29uc3RpdHVlbmN5HgtOYXZpZ2F0ZVVybAUVfi9TZWFyY2hMb2NhbGl0eS5hc3B4HgdFbmFibGVkZx4KU2VsZWN0YWJsZWceCERhdGFQYXRoBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0xXR4JRGF0YUJvdW5kZ2QUKwACFgwfAQUjS25vdyBZb3VyIEJvb3RoIExldmVsIE9mZmljZXIgKEJMTykfAgUKfi9CTE8uYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0yXR8GZ2QUKwACFgwfAQU0Q2hlY2sgWW91ciBOYW1lIGluIHRoZSBWb3RlcnMnIExpc3QgKEVsZWN0b3JhbCBSb2xsKR8CBRR+L0VsZWN0b3JTZWFyY2guYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0zXR8GZ2QUKwACFgwfAQUxS25vdyB0aGUgU3RhdHVzIG9mIFlvdXIgQXBwbGljYXRpb24gZm9yIEVucm9sbWVudB8CBR1+L0NoZWNrQXBwbGljYXRpb25TdGF0dXMuYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT00XR8GZ2QUKwACFgwfAQUSQWxsIEZvcm1zIFJlY2VpdmVkHwIFFn4vQWxsUmVjZWl2ZWRGb3JtLmFzcHgfA2cfBGcfBQUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9NV0fBmdkFCsAAhYMHwEFHExpc3Qgb2YgRGVzaWduYXRlZCBMb2NhdGlvbnMfAgUgfi9Lbm93RGVzaWduYXRlZE9mZmljZXJJbmZvLmFzcHgfA2cfBGcfBQUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9Nl0fBmdkFCsAAhYMHwEFJFNlYXJjaCBZb3VyIE5hbWUgSW4gU3VvTW90byBEZWxldGlvbh8CBSZ+L1NlYXJjaFlvdXJOYW1lSW5TdW9Nb3RvRGVsZXRpb24uYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT03XR8GZ2RkAgsPZBYCAgMPZBYCZg9kFgQCCw8PFgIfAWVkZAIPDzwrAA0BAA8WBB8AZx4LXyFJdGVtQ291bnQCAWQWAmYPZBYEAgEPZBYWAgEPDxYCHwEFATFkZAICDw8WAh8BBQExZGQCAw8PFgIfAQUBOGRkAgQPDxYCHwEFATFkZAIFDw8WAh8BBSM3LCBDSEFLS0kgV0FMSSBHQUxJLCBWSUxMQUdFIExBTVBVUmRkAgYPDxYCHwEFDFNISVNIQU4gS0FVUmRkAgcPDxYCHwEFB0h1c2JhbmRkZAIIDw8WAh8BBQxNVUtFU0ggS1VNQVJkZAIJDw8WAh8BBQIzN2RkAgoPDxYCHwEFBkZlbWFsZWRkAgsPDxYCHwEFEVhWWDAwMDAwNzUgICAgICAgZGQCAg8PFgIeB1Zpc2libGVoZGQYAgUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFPWN0bDAwJExvZ2luVmlld01haW5IZWFkZXJQYWdlJExvZ2luU3RhdHVzTWFpbkhlYWRlclBhZ2UkY3RsMDEFPWN0bDAwJExvZ2luVmlld01haW5IZWFkZXJQYWdlJExvZ2luU3RhdHVzTWFpbkhlYWRlclBhZ2UkY3RsMDMFLmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkR3JpZFZpZXdTZWFyY2hSZXN1bHQPPCsACgEIAgFk"

    FIELDS = [
        'ac_number',
        'part_number',
        'serial_number',
        None, # section number
        None, # address
        'voter_name',
        None, # relative's relation (eg. husband)
        'relative_name',
        'age',
        'sex',
        None, # EPIC number
    ]

    @classmethod
    def request_params(klass, district_number, epic_string):
        return {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': klass.VIEWSTATE,
            'ctl00$ContentPlaceHolder1$TextBoxIDCardNo': epic_string,
            'ctl00$ContentPlaceHolder1$ButtonSearch': 'Search',
        }

    @classmethod
    def getField(klass, td):
        font = td.font
        if not font:
            return None
        else:
            return font.get_text()

    @classmethod
    def parse_html_data(klass, html):
        """
        Parse Delhi CEO website's response and return a dictionary of
        various fields. If parsing fails, raise exception
        """
        html = re.sub('";', ';"', html)
        soup = BeautifulSoup(html)
        table = soup.find('table', { 'id': 'ctl00_ContentPlaceHolder1_GridViewSearchResult' })
        tr = table.find('tr', { 'bgcolor': '#FFFBD6' })
        tds = tr.find_all('td')
        if len(tds) != len(klass.FIELDS):
            raise FailedToParseError()
        data = { key: klass.getField(td) for (key, td) in zip(klass.FIELDS, tds) if key }
        data = klass.cleanup_names(data)
        return data

class TN_Client(CEOClient):
    CEO_URL = 'http://www.elections.tn.gov.in/EPICSEARCH/search.aspx'
    VIEWSTATE = "/wEPDwUJNzY1NTc4NzM1D2QWAmYPZBYCAgMPZBYCAgEPZBYEAgkPFgIeB1Zpc2libGVoZAILDxYCHwBoZGRawzntgtPYZn58629+77G0XNHjGw=="
    EVENTVALIDATION = "/wEWAwL93ZhWAo/H6ZoKAve68+cBfBqstOR8C93boB4SCjivxiIr1Ak="

    FIELDS = [
        None, # epic_number
        'ac_name',
        'part_number',
        'serial_number',
        'voter_name',
        'relative_name',
        'sex',
        None, # address
    ]

    @classmethod
    def request_params(klass, district_number, epic_string):
        return {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': klass.VIEWSTATE,
            '__EVENTVALIDATION': klass.EVENTVALIDATION,
            'ctl00$ContentPlaceHolder1$txtEPIC': epic_string,
            'ctl00$ContentPlaceHolder1$btnsearch': '',
        }

    @classmethod
    def getField(klass, td):
        span = td.span
        if not span:
            return None
        else:
            return span.get_text()

    @classmethod
    def parse_html_data(klass, html):
        """
        Parse Tamil Nadu CEO website's response and return a dictionary of
        various fields. If parsing fails, raise exception
        """
        soup = BeautifulSoup(html)
        table = soup.find('table', { 'id' : 'ctl00_ContentPlaceHolder1_tblVD' })
        trs = table.findAll('tr')
        tds = [ tr.findAll('td')[3] for tr in trs ]
        if len(tds) != len(klass.FIELDS):
            return FailedToParseError()
        data = { key: klass.getField(td) for (key, td) in zip(klass.FIELDS, tds) if key }
        data = klass.cleanup_names(data)
        return data

CEO_CLIENTS = {
    'KA': KA_Client,
    'DL': DL_Client,
    'TN': TN_Client,
}
