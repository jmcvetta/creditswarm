# Copyright (c) 2012 Jason McVetta.  This is Free Software, released under the
# terms of the AGPL v3.  See www.gnu.org/licenses/agpl-3.0.html for details.

from django.db import models
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

ACCT_DISPUTE_REASON_CHOICES = [
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

class CreditReport(models.Model):
    '''
    A credit report, furnished by a Credit Reporting Agency
    '''
    user = models.ForeignKey(User, blank=False)
    cra = models.CharField(max_length=128, blank=False, choices=CRA_CHOICES, 
        verbose_name='Credit Reporting Agency')
    report_number = models.CharField(max_length=128, blank=False)
    
    class Meta:
        unique_together = ['user', 'cra', 'report_number']
    
    def __str__(self):
        return '%s:%s' % (self.get_cra_display().lower(), self.report_number)


class Inquiry(models.Model):
    '''
    What is this?  An inquiry about what?  Is it tied to a user in general, or 
    only to a specific credit report, or...?
    '''
    inquiry_company_name = models.CharField(max_length=128, blank=True, null=True)
    inquiry_date = models.DateField(blank=True, null=True)


class Detail(models.Model):
    '''
    A disputed account detail
    '''
    report = models.ForeignKey(CreditReport, blank=False)
    company_name = models.CharField(max_length=128, blank=True, null=True)
    account_number = models.CharField(max_length=128, blank=True, null=True)
    reason = models.CharField(max_length=32, blank=True, null=True, 
        choices=ACCT_DISPUTE_REASON_CHOICES)
    other_reason = models.TextField(blank=True, null=True)


class BadInfo(models.Model):
    '''
    Bad demographic info
    '''
    report = models.ForeignKey(CreditReport, blank=False)
    problem = models.CharField(max_length=32, blank=True, null=True, 
        choices=BAD_INFO_TYPE_CHOICES)
    explanation = models.TextField(blank=True, null=True)


class Dispute(models.Model):
    '''
    A credit report dispute
    '''
    user = models.ForeignKey(User, blank=False)
    ts_created = models.DateTimeField(auto_now_add=True, blank=False, 
        verbose_name='Created Timestamp')
    ts_updated = models.DateTimeField(auto_now=True, blank=False, 
        verbose_name='Updated Timestamp')
    status = models.CharField(max_length=3, blank=False, choices=STATUS_CHOICES)