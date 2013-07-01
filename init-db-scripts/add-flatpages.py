
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
('/fp/terms-and-conditions/', 'Terms and Conditions, and Privacy Policy', textwrap.dedent("""

<h2>
    Web Site Terms and Conditions of Use
</h2>

<h3>
    1. Terms
</h3>

<p>
    By accessing this web site, you are agreeing to be bound by these
    web site Terms and Conditions of Use, all applicable laws and regulations,
    and agree that you are responsible for compliance with any applicable local
    laws. If you do not agree with any of these terms, you are prohibited from
    using or accessing this site. The materials contained in this web site are
    protected by applicable copyright and trade mark law.
</p>

<h3>
    2. Use License
</h3>

<ol type="a">
    <li>
        Permission is granted to temporarily download one copy of the materials
        (information or software) on Save Your Vote's web site for personal,
        non-commercial transitory viewing only. This is the grant of a license,
        not a transfer of title, and under this license you may not:

        <ol type="i">
            <li>modify or copy the materials;</li>
            <li>use the materials for any commercial purpose, or for any public display (commercial or non-commercial);</li>
            <li>attempt to decompile or reverse engineer any software contained on Save Your Vote's web site;</li>
            <li>remove any copyright or other proprietary notations from the materials; or</li>
            <li>transfer the materials to another person or "mirror" the materials on any other server.</li>
        </ol>
    </li>
    <li>
        This license shall automatically terminate if you violate any of these restrictions and may be terminated by Save Your Vote at any time. Upon terminating your viewing of these materials or upon the termination of this license, you must destroy any downloaded materials in your possession whether in electronic or printed format.
    </li>
</ol>

<h3>
    3. Disclaimer
</h3>

<ol type="a">
    <li>
        The materials on Save Your Vote's web site are provided "as is". Save Your Vote makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties, including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights. Further, Save Your Vote does not warrant or make any representations concerning the accuracy, likely results, or reliability of the use of the materials on its Internet web site or otherwise relating to such materials or on any sites linked to this site.
    </li>
</ol>

<h3>
    4. Limitations
</h3>

<p>
    In no event shall Save Your Vote or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption,) arising out of the use or inability to use the materials on Save Your Vote's Internet site, even if Save Your Vote or a Save Your Vote authorized representative has been notified orally or in writing of the possibility of such damage. Because some jurisdictions do not allow limitations on implied warranties, or limitations of liability for consequential or incidental damages, these limitations may not apply to you.
</p>

<h3>
    5. Revisions and Errata
</h3>

<p>
    The materials appearing on Save Your Vote's web site could include technical, typographical, or photographic errors. Save Your Vote does not warrant that any of the materials on its web site are accurate, complete, or current. Save Your Vote may make changes to the materials contained on its web site at any time without notice. Save Your Vote does not, however, make any commitment to update the materials.
</p>

<h3>
    6. Links
</h3>

<p>
    Save Your Vote has not reviewed all of the sites linked to its Internet web site and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by Save Your Vote of the site. Use of any such linked web site is at the user's own risk.
</p>

<h3>
    7. Site Terms of Use Modifications
</h3>

<p>
    Save Your Vote may revise these terms of use for its web site at any time without notice. By using this web site you are agreeing to be bound by the then current version of these Terms and Conditions of Use.
</p>

<h3>
    8. Governing Law
</h3>

<p>
    Any claim relating to Save Your Vote's web site shall be governed by the laws of the State of Karnataka, India without regard to its conflict of law provisions.
</p>

<p>
    General Terms and Conditions applicable to Use of a Web Site.
</p>



<h2>
    Privacy Policy
</h2>

<p>
    Your privacy is very important to us. Accordingly, we have developed this Policy in order for you to understand how we collect, use, communicate and disclose and make use of personal information. The following outlines our privacy policy.
</p>

<ul>
    <li>
        Before or at the time of collecting personal information, we will identify the purposes for which information is being collected.
    </li>
    <li>
        We will collect and use of personal information solely with the objective of fulfilling those purposes specified by us and for other compatible purposes, unless we obtain the consent of the individual concerned or as required by law.
    </li>
    <li>
        We will only retain personal information as long as necessary for the fulfillment of those purposes.
    </li>
    <li>
        We will collect personal information by lawful and fair means and, where appropriate, with the knowledge or consent of the individual concerned.
    </li>
    <li>
        Personal data should be relevant to the purposes for which it is to be used, and, to the extent necessary for those purposes, should be accurate, complete, and up-to-date.
    </li>
    <li>
        We will protect personal information by reasonable security safeguards against loss or theft, as well as unauthorized access, disclosure, copying, use or modification.
    </li>
    <li>
        We will make readily available to customers information about our policies and practices relating to the management of personal information.
    </li>
</ul>

<p>
    We are committed to conducting our business in accordance with these principles in order to ensure that the confidentiality of personal information is protected and maintained.
</p>
""")),

('/fp/contact/', 'Contact Us', textwrap.dedent("""
<h2 class="text-center"> Contact Us </h2>
<p>
The best way to contact us is by leaving a comment below or emailing
info@saveyourvote.in.
</p>
""")),

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
