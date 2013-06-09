
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saveyourvote.settings")

from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.conf import settings
import textwrap

FlatPage.objects.all().delete()

site = Site.objects.get(pk=settings.SITE_ID)
PAGES = [
('/', 'Home Page', textwrap.dedent("""
<h2 class="text-center"> Welcome to Save Your Vote </h2>
<dl class="dl-horizontal">
    <dt><button class="btn btn-block btn-danger" type="button">Problem</button></dt>
    <dd>Several voters in India find that they are unable to vote on
    election day because their name has been deleted from the voter roll.
    <br /> <br /> </dd>

    <dt><button class="btn btn-block btn-success" type="button">Solution</button></dt>
    <dd>Save your Voter ID number on our website and we will notify you
    over Facebook and e-mail if your record is deleted by mistake. </dd>
</dl>

<p>
Don't hesitate. It only takes a couple of minutes to add your Voter ID
number. You can also add details of other voters such as your family
members. <br /> <br />
</p>


<p class="text-center">
<a href="/voterreg/epic/new/"><button class="btn btn-large btn-primary"
type="button">Add Voter Information</button></a>
</p>

""")),
]

for (url, title, content) in PAGES:
    fp = FlatPage(url=url, title=title, content=content)
    fp.save()
    fp.sites.add(site)
    print fp

# Save Your Vote is an initiative to ensure that genuine registered Indian
# voters are not disenfranchised and end up unable to vote on election day.
# Most Indian voters know someone who goes to vote on election day only to
# find their name missing from the electoral role. News articles about this
# issue come up every election, however nothing changes.
# 
# On the Save Your Vote website, you will be able to add your Voter ID
# information (and that of your family members who are not internet-savvy).
# We will monitor the Chief Election Commissioner's database to ensure that
# your record does not get deleted. In case your record gets deleted, we will
# notify you through Facebook and e-mail so that you can restore it.
# 
# In case you are hesitant to enter your Voter ID information, please note
# that your voter details are public information and can already be found on
# the Election Commissioner's website. Save Your Vote merely allows you to
# prevent government officials from deleting your name by mistake.
# 
# Don't hesitate. Go ahead and save your vote.
