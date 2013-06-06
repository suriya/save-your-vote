# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from models import ExistingVoter
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from utils import check_karnataka_epic
# ZBG6433064

class ExistingVoterForm(forms.ModelForm):
    class Meta:
        model = ExistingVoter
        fields = [ 'district', 'epic_number' ]

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
    voter_with_data = check_karnataka_epic(voter)
    if voter_with_data:
        assert (voter is voter_with_data)
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
        voter = None
    return render(request, 'voterreg/epic-delete.html', { 'voter': voter })

@login_required
def epic_list(request):
    voter_list = ExistingVoter.objects.filter(created_by=request.user)
    return render(request, 'voterreg/epic-list.html', { 'voter_list': voter_list })
