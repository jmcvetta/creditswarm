# Copyright (c) 2012 Jason McVetta.

import datetime
#
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
#
from storages.backends.s3boto import S3BotoStorage
#
from celery.task import Task
from celery.registry import tasks
#
from templated_email import send_templated_mail
#
from creditswarm.settings import DEFAULT_FROM_EMAIL
from creditswarm.settings import CREDIT_REPORTING_AGENCIES as AGENCIES


STATUS_CHOICES = [
    ('D', 'Draft'),
    ('Q', 'Queued for Send'),
    ('S', 'Sent'),
    ]

CRA_CHOICES = [(key, AGENCIES[key]['name']) for key in AGENCIES]

DETAIL_REASON_CHOICES = [
    ('unknown_acct', 'Unknown Account'),
    ('not_mine', 'Not Mine'),
    ('on_time', 'Paid On Time'),
    ('fraud', 'Fraud / ID Theft'),
    ('unauthorized', 'Unauthorized Charge / Fee / Interest'),
    ('bankruptcy', 'Bankruptcy Discharge'),
    ('expired', 'Expired Account'),
    ('wrong_details', 'Wrong Account Details'),
    ('other', 'Other'),
    ]

BAD_INFO_TYPE_CHOICES = [
    ('name', 'Incorrect Name'),
    ('dob', 'Incorrect Date of Birth'),
    ('employer', 'Incorrect Employer'),
    ('address', 'Incorrect Address'),
    ('spouse', 'Incorrect Spouse'),
    ('phone', 'Incorrect Telephone'),
    ('other', 'Other Incorrect Information'),
    ]


class Case(models.Model):
    '''
    A Credit Swarm dispute case, containing one or more varieties of Dispute
    '''
    user = models.ForeignKey(User)
    ts_created = models.DateTimeField(auto_now_add=True,
        verbose_name='Created Timestamp')
    ts_updated = models.DateTimeField(auto_now=True,
        verbose_name='Updated Timestamp')
    ts_submitted = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='D')
    #
    # Credit Report
    #
    agency = models.CharField(max_length=128, choices=CRA_CHOICES, 
        verbose_name='Credit Reporting Agency')
    report_number = models.CharField(max_length=128)
    
    class Meta:
        ordering = ['-ts_updated']
        permissions = [
            ('cra_view', 'CRA can view case'),
            ]
    
    def get_absolute_url(self):
        return reverse('case-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return '%s: %s %s (%s)' % (self.pk, self.get_agency_display(), self.report_number, self.user)
    
    def ready_to_submit(self):
        '''
        Returns True if this Dispute has enough information attached that it
        is ready to submit.
        '''
        return bool(
            self.account_set.all() 
            or self.inquiry_set.all()
            or self.demographic_set.all()
            )
    
    @property
    def case_number(self):
        '''
        An formatted number officially designating this case.
        '''
        s = u'%012d' % self.pk
        return s[:3] + '-' + s[3:6] + '-' + s[6:9] + '-' + s[9:]
    
    @property
    def case_id(self):
        '''
        An formatted string, consisting of the prefix NCDAC- and the case 
        number, officially designating this case.
        '''
        return 'NCDAC-' + self.case_number
    
    def email_cra(self):
        '''
        Sends a dispute email for to the Credit Reporting Agency
        '''
        send_templated_mail(
            template_name = 'cra_dispute_notification',
            from_email = DEFAULT_FROM_EMAIL,
            recipient_list = [AGENCIES[self.agency]['email'],],
            context = {
                'object': self,
                'current_site': Site.objects.get_current(),
                },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_ 
            template_suffix = 'html',
            )
        self.status = 'S'
        self.save()


class Dispute(models.Model):
    '''
    Abstract base class for the several varieties of credit dispute
    '''
    case = models.ForeignKey(Case) 
    ts_created = models.DateTimeField(auto_now_add=True,
        verbose_name='Created Timestamp')
    ts_updated = models.DateTimeField(auto_now=True,
        verbose_name='Updated Timestamp')

    class Meta:
        abstract = True



class Inquiry(Dispute):
    '''
    A disputed credit score inquiry
    '''
    company_name = models.CharField(max_length=128)
    date = models.DateField(default=datetime.date.today)
    
    class Meta:
        verbose_name = 'Credit Inquiry'
        verbose_name_plural = 'Credit Inquiries'
    

class Account(Dispute):
    '''
    A disputed account detail
    '''
    creditor = models.CharField(max_length=128, help_text='Name of creditor company')
    account_number = models.CharField(max_length=128)
    reason = models.CharField(max_length=32, choices=DETAIL_REASON_CHOICES, 
        help_text='Reason you are disputing this account')
    explanation = models.TextField(blank=True, null=True, 
        help_text='Explain why this account detail is incorrect.')
    evidence = models.FileField(null=True, blank=True,
        upload_to='evidence',
        help_text='Upload document supporting your dispute.',
        storage=S3BotoStorage(bucket='creditswarm-secure'),
        )
    
    class Meta:
        verbose_name = 'Account Detail'


class Demographic(Dispute):
    '''
    Disputed demographic info
    '''
    problem = models.CharField(max_length=32, blank=True, null=True, 
        choices=BAD_INFO_TYPE_CHOICES)
    explanation = models.TextField(blank=True, null=True)

