# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

import datetime
#
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('D', 'Draft'),
    ('Q', 'Queued for Send'),
    ('S', 'Sent'),
    ]

# Credit Reporting Agencies
CRA_CHOICES = [
    ('xp', 'Experian'),
    ('eq', 'Equifax'),
    ('tu', 'TransUnion'),
    ]

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
    ('name', 'Name'),
    ('dob', 'Date of Birth'),
    ('employer', 'Employer'),
    ('address', 'Address'),
    ('spouse', 'Spouse'),
    ('phone', 'Telephone'),
    ]

class Dispute(models.Model):
    '''
    A credit report dispute
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
    
    def get_absolute_url(self):
        return reverse('dispute-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-ts_updated']
    
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
            or self.badinfo_set.all()
            )


class Inquiry(models.Model):
    '''
    A disputed credit score inquiry
    '''
    dispute = models.ForeignKey(Dispute) # Maybe should be attached to CreditReport?
    company_name = models.CharField(max_length=128)
    date = models.DateField(default=datetime.date.today)
    explanation = models.TextField(blank=False, null=False, 
        help_text='Explain why this inquiry record is incorrect.')
    

class Account(models.Model):
    '''
    A disputed account detail
    '''
    dispute = models.ForeignKey(Dispute)
    creditor = models.CharField(max_length=128, help_text='Name of creditor company')
    account_number = models.CharField(max_length=128)
    reason = models.CharField(max_length=32, choices=DETAIL_REASON_CHOICES, 
        help_text='Reason you are disputing this account')
    explanation = models.TextField(blank=True, null=True, 
        help_text='Explain why this account detail is incorrect.')
    evidence = models.FileField(null=True, blank=True,
        upload_to='evidence',
        help_text='Upload document supporting your dispute.'
        )


class BadInfo(models.Model):
    '''
    Bad demographic info
    '''
    dispute = models.ForeignKey(Dispute)
    problem = models.CharField(max_length=32, blank=True, null=True, 
        choices=BAD_INFO_TYPE_CHOICES)
    explanation = models.TextField(blank=True, null=True)

