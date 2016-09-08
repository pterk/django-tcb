from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from . import forms
from . import models


@login_required
def entry(request):
    if request.method == 'POST':
        form = forms.EntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/log/')
    else:
        form = forms.EntryForm()
    return render(
        request, 'business/entry.html',
        {
            'form': form,
        })


@login_required
def entry_log(request):
    entries = models.Entry.objects.all().order_by('-created')[:50]
    return render(
        request, 'business/entry_log.html',
        {
            'entries': entries,
        })



@login_required
def overview(request):
    form = forms.FilterForm(request.GET)
    form.is_valid()
    quarters = models.get_quarters()
    quarter = form.cleaned_data['quarter']
    month = form.cleaned_data['month']
    month = [m for m in models.get_months() if str(m) == month]
    if quarter:
        entries = models.Entry.objects.get_quarter(quarters[quarter])
    else:
        if month:
            month = month[0]
            entries = models.Entry.objects.get_month(month)
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
