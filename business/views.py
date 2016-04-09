from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from . import forms
from . import models


@login_required
def entry(request):
    if request.method == 'POST':
        form = forms.EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('/')
    else:
        form = forms.EntryForm()
    return render(
        request, 'business/entry.html',
        {
            'form': form,
        })


@login_required
def overview(request):
    form = forms.FilterForm(request.GET)
    _ = form.is_valid()
    quarters = models.get_quarters()
    quarter = form.cleaned_data['quarter']
    if quarter:
        entries = models.Entry.objects.get_quarter(quarters[quarter])
    else:
        entries = models.Entry.objects.get_quarter(timezone.now())
    project = form.cleaned_data.get('project', None)
    if project:
        entries = entries.filter(project=project)
    totals = entries.totals()
    total = sum([r['total'] for r in totals])
    vat = sum([r['vat'] for r in totals])
    total_with_vat = sum([r['total_with_vat'] for r in totals])
    return render(
        request, 'business/overview.html',
        {
            'entries': entries,
            'totals': totals,
            'form': form,
            'project': project,
            'total': total,
            'vat': vat,
            'total_with_vat': total_with_vat,
        })
