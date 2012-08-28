# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

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
        return '#%s' % self.pk


class Inquiry(models.Model):
    '''
    What is this?  An inquiry about what?  Is it tied to a user in general, or 
    only to a specific credit report, or...?
    '''
    dispute = models.ForeignKey(Dispute) # Maybe should be attached to CreditReport?
    inquiry_company_name = models.CharField(max_length=128, blank=True, null=True)
    inquiry_date = models.DateField(blank=True, null=True)


class Detail(models.Model):
    '''
    A disputed account detail
    '''
    dispute = models.ForeignKey(Dispute)
    company_name = models.CharField(max_length=128)
    account_number = models.CharField(max_length=128)
    reason = models.CharField(max_length=32,
        choices=DETAIL_REASON_CHOICES)
    Explanation = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['dispute', 'company_name', 'account_number']


class BadInfo(models.Model):
    '''
    Bad demographic info
    '''
    dispute = models.ForeignKey(Dispute)
    problem = models.CharField(max_length=32, blank=True, null=True, 
        choices=BAD_INFO_TYPE_CHOICES)
    explanation = models.TextField(blank=True, null=True)

