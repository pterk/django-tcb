from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import forms, models


def overview(request):
    if request.method == 'POST':
        form = forms.EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('/')
    else:
        form = forms.EntryForm()
    totals = models.Entry.objects.current_quarter().totals()
    total = sum([r['total'] for r in totals])
    vat = sum([r['vat'] for r in totals])
    total_with_vat = sum([r['total_with_vat'] for r in totals])
    return render(
        request, 'business/overview.html',
        {
            'current_quarter_totals': totals,
            'form': form,
            'total': total,
            'vat': vat,
            'total_with_vat': total_with_vat,
        })


def project_overview(request, project_id):
    project = get_object_or_404(models.Project, pk=project_id)
    entries = models.Entry.objects.current_quarter().filter(project=project)
    totals = entries.totals()
    total = sum([r['total'] for r in totals])
    vat = sum([r['vat'] for r in totals])
    total_with_vat = sum([r['total_with_vat'] for r in totals])
    return render(
        request, 'business/project-overview.html',
        {
            'project': project,
            'current_quarter_entries': entries,
            'current_quarter_totals': totals,
            'total': total,
            'vat': vat,
            'total_with_vat': total_with_vat,
        })
