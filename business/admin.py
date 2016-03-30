from django.contrib import admin

from . import forms, models


class ClientAdmin(admin.ModelAdmin):
    form = forms.ClientForm


class EntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'project', 'number', 'total']
    form = forms.EntryForm


class ProjectAdmin(admin.ModelAdmin):
    form = forms.ProjectForm


class RateAdmin(admin.ModelAdmin):
    form = forms.RateForm


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Rate, RateAdmin)
