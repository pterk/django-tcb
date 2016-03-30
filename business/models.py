from datetime import date, timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone

from core.models import BaseModel


UNIT_TYPE_HOUR = 1
UNIT_TYPE_DAY = 8
UNIT_TYPE_FIXED = 0

UNIT_TYPE_HOUR_NAME = 'hourly'
UNIT_TYPE_DAY_NAME = 'daily'
UNIT_TYPE_FIXED_NAME = 'fixed'

UNITS = {
    UNIT_TYPE_HOUR: UNIT_TYPE_HOUR_NAME,
    UNIT_TYPE_DAY: UNIT_TYPE_DAY_NAME,
    UNIT_TYPE_FIXED: UNIT_TYPE_FIXED_NAME,
}

UNIT_TYPES = [(k,v) for k,v in UNITS.items()]


def today():
    return timezone.now().date()


def get_quarter(date):
    return (date.month-1)//3 + 1


def get_quarter_start(dte):
    start_month = ((get_quarter(dte) - 1) * 3) + 1
    return date(dte.year, start_month, 1)


def get_next_quarter_start(dte):
    this_quarter = get_quarter_start(dte)
    if this_quarter.month < 10:
        return this_quarter.replace(month=this_quarter.month + 3)
    else:
        return this_quarter.replace(
            year=this_quarter.year + 1,
            month=this_quarter.month - 9
        )


class Client(BaseModel):
    name = models.TextField(unique=True)
    email = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EntryQuerySet(models.QuerySet):
    def current_quarter(self):
        return self.select_related('project', 'project__rate', 'project__client').filter(
            date__gte=get_quarter_start(today()),
            date__lt=get_next_quarter_start(today()))

    def totals(self):
        rows = self.select_related('project', 'project__rate', 'project__client').values(
            'project__name', 'project__rate__rate', 'project__rate__unit_type',
            'project__client__name', 'project_id', 'project__vat', 'billable',
        ).annotate(hours=models.Sum('number')).order_by('project_id')
        #print (len(rows))
        for row in rows:
            if row['project__rate__unit_type'] == UNIT_TYPE_FIXED:
                row['total'] = row['project__rate__rate']
            elif not row['billable']:
                row['total'] = 0
            else:
                row['total'] = Decimal((
                    row['project__rate__rate'] / row['project__rate__unit_type']) * row['hours']
                                   ).quantize(Decimal('1.00'))
            row['vat'] = ((row['project__vat']/100) * row['total']).quantize(Decimal('1.00'))
            row['total_with_vat'] = (row['total'] + row['vat']).quantize(Decimal('1.00'))
            # rename
            row['unit'] = UNITS[row.pop('project__rate__unit_type')]
            row['project'] = row.pop('project__name')
            row['project_id'] = row.pop('project_id')
            row['client'] = row.pop('project__client__name')
            row['rate'] = row.pop('project__rate__rate')
        return rows


class Entry(BaseModel):
    date = models.DateField(default=today)
    project = models.ForeignKey('Project')
    unit_type = models.IntegerField(choices=UNIT_TYPES, default=1)
    number = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField()
    billable = models.BooleanField(default=True)

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "entries"
        ordering = ['date']

    @property
    def unit(self):
        return UNITS[self.unit_type]

    def total(self):
        # sanitize
        if self.unit_type == UNIT_TYPE_FIXED:
            return self.project.rate.rate
        if not self.billable:
            return 0
        return Decimal((self.project.rate.rate / self.project.rate.unit_type) * self.number).quantize(Decimal('1.00'))

    def __str__(self):
        return "{}: {} => {} {} : {}".format(
            self.date, self.project, self.number, UNITS[self.unit_type], self.total())


class ProjectManager(models.Manager):
    pass


class ActiveProjectManager(ProjectManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            start__lte=timezone.now(),
            end__gte=timezone.now())


class Project(BaseModel):
    client = models.ForeignKey('Client', related_name='projects')
    name = models.TextField()
    start = models.DateField(default=today)
    end = models.DateField()
    rate = models.ForeignKey('Rate')
    vat =  models.DecimalField(max_digits=4, decimal_places=2, default=21)

    objects = ProjectManager()
    active = ActiveProjectManager()

    class Meta:
        unique_together = ('client', 'name', 'start')

    def __str__(self):
        return "{} : {}".format(self.client, self.name)


class Rate(BaseModel):
    name = models.TextField()
    unit_type = models.IntegerField(choices=UNIT_TYPES, default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "{} (€{} / {})".format(
            self.name, self.rate, UNITS[self.unit_type])

    @property
    def unit(self):
        return UNITS[self.unit_type]
