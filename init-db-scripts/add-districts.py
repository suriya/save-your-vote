
import os
from django.core.exceptions import ObjectDoesNotExist
from voterreg.models import IndianState, IndianDistrict

scriptdir = os.path.dirname(os.path.abspath(__file__))
districtslistfile = os.path.join(scriptdir, 'distlistnew.htm')

import string
import re
from bs4 import BeautifulSoup
soup = BeautifulSoup(open(districtslistfile, 'r').read())

def remove_tags(s):
    output = re.sub(r'<.*?>', '', s, count=0)
    return string.capwords(output)

def clean_district(s):
    s = remove_tags(s)
    s = re.sub(r'\(.*?\)', '', s, count=0)
    return s.strip()

def clean_state(s):
    s = re.sub(r'Districts Of ', '', s)
    s = re.sub(r'&amp;', 'and', s)
    s = re.sub('Lakshdweep', 'Lakshadweep', s)
    return remove_tags(s)

def get_state_object(s):
    try:
        return IndianState.objects.get(name=s)
    except ObjectDoesNotExist:
        pass
    for i in reversed(xrange(5, len(s) + 1)):
        try:
            return IndianState.objects.get(name__istartswith=s[:i])
        except ObjectDoesNotExist:
            pass
    raise ValueError("Could not find state %s" % s)

def get_districts(state):
    districts = state.next_sibling.next_sibling
    for line in repr(districts).split('\n'):
        line = clean_district(line)
        if line:
            yield line

states = soup.findAll('h2')[1:]
for state in states:
    state_name = clean_state(repr(state.u))
    print state_name
    stateobj = get_state_object(state_name)
    print stateobj
    if stateobj.shortcode in [ 'KA', 'UP' ]:
        continue
    districts = get_districts(state)
    for d in sorted(districts):
        districtobj = IndianDistrict(state=stateobj, name=d)
        districtobj.save()
        print '    ', districtobj
    print "====================================="
