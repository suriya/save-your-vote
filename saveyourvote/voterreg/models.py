from django.db import models
from django.conf import settings

class IndianState(models.Model):
    name = models.CharField(max_length=40)
    shortcode = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.shortcode)

class IndianDistrict(models.Model):
    state = models.ForeignKey(IndianState)
    name = models.CharField(max_length=40)
    number = models.IntegerField()

    def __unicode__(self):
        return u'%s, %s' % (self.name, unicode(self.state))

class ExistingVoter(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    # user = ...
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    epic_number = models.CharField(max_length=20,
            help_text='Voter identity card number the format ABC1234567')
    district = models.ForeignKey(IndianDistrict)
    ac_number = models.CharField("Assembly Constituency number", max_length=20)
    ac_name = models.CharField("Assembly Constituency name", max_length=200)
    part_number = models.CharField("Part number", max_length=20)
    serial_number = models.CharField("Serial number", max_length=20)
    voter_first_name = models.CharField("First name (Voter)", max_length=200)
    voter_last_name = models.CharField("Last name (Voter)", max_length=200)
    relative_first_name = models.CharField("First name (Relative)", max_length=200)
    relative_last_name = models.CharField("Last name (Relative)", max_length=200)
    sex = models.CharField("Sex", max_length=20)
    age = models.CharField("Age", max_length=20)
    status_message = models.TextField("Status message")

    def __unicode__(self):
        return self.epic_number
