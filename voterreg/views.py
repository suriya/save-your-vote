# Create your views here.

import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from models import ExistingVoter, IndianState, IndianDistrict
from ceo_server_client import CEOClient
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from utils import check_karnataka_epic
from django.contrib.auth import REDIRECT_FIELD_NAME

class ExistingVoterForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=IndianState.objects.all())
    class Meta:
        model = ExistingVoter
        fields = [ 'district', 'epic_number' ]

    def __init__(self, *args, **kwargs):
        super(ExistingVoterForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [ 'state', 'district', 'epic_number' ]

@login_required
def epic_new(request):
    # Empty Form
    if request.method != 'POST':
        form = ExistingVoterForm()
        return render(request, 'voterreg/epic-new.html', { 'form': form, })
    # Form with errors
    form = ExistingVoterForm(request.POST)
    if not form.is_valid():
        return render(request, 'voterreg/epic-new.html', { 'form': form, })
    # Completed form
    voter = form.save(commit=False)
    voter.created_by = request.user
    try:
        CEOClient.record_voter_info(voter)
    except Exception, e:
        voter.status_message = str(e)
    voter.save()
    form.save_m2m()
    url = ('%s?thanks=1' % reverse('epic-info', args=[ voter.pk ]))
    return HttpResponseRedirect(url)

def epic_info(request, pk):
    voter = get_object_or_404(ExistingVoter, pk=pk)
    thanks = request.GET.get('thanks', False)
    return render(request, 'voterreg/epic-info.html', { 'voter': voter, 'thanks': thanks })

@csrf_protect
@login_required
def epic_delete(request, pk):
    voter = get_object_or_404(ExistingVoter, pk=pk)
    if (request.user.pk is not voter.created_by.pk):
        raise PermissionDenied
    if request.method == 'POST':
        voter.delete()
        url = ('%s?deleted=1' % reverse('epic-list'))
        return HttpResponseRedirect(url)
    return render(request, 'voterreg/epic-delete.html', { 'voter': voter })

@login_required
def epic_list(request):
    deleted = request.GET.get('deleted', False)
    voter_list = ExistingVoter.objects.filter(created_by=request.user)
    return render(request, 'voterreg/epic-list.html', { 'deleted': deleted, 'voter_list': voter_list })

def facebook_login(request, template_name='voterreg/facebook-login.html',
        redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    return render(request, 'voterreg/facebook-login.html', { redirect_field_name: redirect_to })

def district_list(request):
    districts = [ { 'pk': d.pk,
                    'name': d.name,
                    'state_name': d.state.name,
                    'state_shortcode': d.state.shortcode,
                    'state_id': d.state.pk,
                  } for d in IndianDistrict.objects.all() ]
    dictionary = { 'districts': districts }
    return HttpResponse(json.dumps(dictionary, indent=2), mimetype="application/json")

def home_page(request):
    return render(request, 'voterreg/home-page.html', { 'next': reverse('epic-new') })
