
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saveyourvote.settings")

from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.conf import settings
import textwrap

FlatPage.objects.all().delete()

site = Site.objects.get(pk=settings.SITE_ID)
site.domain = 'saveyourvote.in'
site.name = 'Save Your Vote'
site.save()

PAGES = [
('/fp/the-missing-voter/', "The missing voter", textwrap.dedent("""

<div class="page-header"> <h1>The missing voter</h1> </div>

<p>
A major issue ailing India's election process is that genuine registered
Indian voters become disenfranchised and end up unable to vote on election
day. Most Indian voters know someone who goes to vote on election day only to
find their name missing from the electoral roll. News articles about this
issue come up every election, however nothing changes. For example, take a
look
<a href="http://news.oneindia.in/2013/05/05/bangalore-names-go-missing-from-electoral-rolls-1209745.html">here</a>,
<a href="http://m.indianexpress.com/news/no-response-84700-names-deleted-from-electoral-rolls/1119836/">here</a>,
<a href="http://pressclubofindia.co.in/names-go-missing-from-electoral-rolls-in-bangalore/">here</a>,
<a href="http://articles.timesofindia.indiatimes.com/2013-06-08/ranchi/39833960_1_missing-names-revised-electoral-roll-omission">here</a>,
<a href="http://www.hindu.com/2009/04/25/stories/2009042559980400.htm">here</a>,
... Here's a voter showing Voter IDs for his neighbours whose names were
missing in the rolls.
</p>

<p class="text-center">
<img
src="http://www.hindu.com/2009/04/25/images/2009042559980401.jpg"
alt="Unable to Vote" />
</p>

<h2 class="text-center">A simple solution</h2>
<p>
We want to make it easy for voters to ensure that their name does not get
deleted accidentally or otherwise. Once you enter your Voter ID number on
our website, we will monitor the Election Commissioner's database for
changes ensuring that your record does not get deleted.
</p>
""")),
('/fp/faq/', 'Frequently Anticipated Questions (FAQ)', textwrap.dedent("""
<div class="page-header"> <h2>Frequently Anticipated Questions</h2> </div>

<dl class="faq">
<dt> 1. Why should I trust you with my Voter ID number? </dt>
<dd>
Your Voter ID number along with other details such as your name, age, and
street address is public information. You can go look them up on the
Election Commissioner's website. The Election Commission makes PDF copies
of the voter roll available on their website.
</dd>

<dt>
<dt> 2. Will you sell my data? </dt>
<dd>
We care about your privacy and we will not sell your data to anyone. We may
send your notification emails such as the date of election, your polling
booth, etc. In any case, we will let you opt out of any e-mail from us.
</dd>

<!--
<dt> 3. Will you have advertising on the site? </dt>
<dd>
Maybe, in order to pay for our hosting costs.
</dd>
-->

<dt> 3. Why aren't all states supported at the moment? </dt>
<dd>
At the moment, we support Delhi, Karnataka, Tamil Nadu, and Uttar Pradesh.
It is a matter of time before we get to support other states as well.
<strong>Even if your state is not supported, you can add your Voter ID
number and we will notify you once we add support for your state. </strong>
If you are a developer you can contribute to our source code to quickly
support all the states in India.
</dd>
</dl>

If you have more questions, feel free to leave a message below.

""")),
('/', 'Home Page', textwrap.dedent("""
<h2 class="text-center"> Welcome to Save Your Vote </h2>
<dl class="dl-horizontal">
    <dt><button style="cursor: default;" class="btn btn-block btn-danger" type="button">Problem</button></dt>
    <dd>Several voters in India find that they are unable to vote on
    election day because their name has been deleted from the voter roll.
    <br /> <br /> </dd>

    <dt><button style="cursor: default;" class="btn btn-block btn-success" type="button">Solution</button></dt>
    <dd>Save your Voter ID number on our website and we will notify you
    over Facebook and e-mail if your record is deleted by mistake. </dd>
</dl>

<p>
Don't wait until it is too late. It only takes a couple of minutes to add
your Voter ID number. You can also add details of other voters such as your
family members. <br /> <br />
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
