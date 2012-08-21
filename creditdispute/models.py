from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('D', 'Draft'),
    ('Q', 'Queued for Send'),
    ('S', 'Sent'),
    ]

BUREAU_CHOICES = [
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

WRONG_INFO_TYPE_CHOICES = [
    ('name', 'Name'),
    ('dob', 'Date of Birth'),
    ('employer', 'Employer'),
    ('address', 'Address'),
    ('spouse', 'Spouse'),
    ('phone', 'Telephone'),
    ]


class Dispute(models.Model):
    user = models.ForeignKey(User, blank=False)
    ts_created = models.DateTimeField(auto_now_add=True, blank=False, 
        verbose_name='Created Timestamp')
    ts_updated = models.DateTimeField(auto_now=True, blank=False, 
        verbose_name='Updated Timestamp')
    status = models.CharField(max_length=3, blank=False, choices=STATUS_CHOICES)
    #
    # Personal Info 
    # - use encrypted fields before running in production!
    #
    given_name = models.CharField(max_length=128, blank=False)
    family_name = models.CharField(max_length=128, blank=False)
    address1 = models.CharField(max_length=128, blank=False)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=False)
    state = models.CharField(max_length=128, blank=False)
    zip = models.CharField(max_length=128, blank=False)
    date_of_birth = models.DateField(blank=False)
    ssn = models.CharField(max_length=128, blank=False)
    #
    # Credit Report(s)
    #
    report_number = models.CharField(max_length=128, blank=False)
    bureau = models.CharField(max_length=128, blank=False, choices=BUREAU_CHOICES)
    #
    # Disputed Account
    # - This should be split into a separate model with a M2M relationship
    #
    dispute_company_name = models.CharField(max_length=128, blank=True, null=True)
    dispute_account_number = models.CharField(max_length=128, blank=True, null=True)
    dispute_reason = models.CharField(max_length=32, blank=True, null=True, 
        choices=ACCT_DISPUTE_REASON_CHOICES)
    dispute_other_reason = models.TextField(blank=True, null=True)
    #
    # Inquiries
    #
    inquiry_company_name = models.CharField(max_length=128, blank=True, null=True)
    inquiry_date = models.DateField(blank=True, null=True)
    #
    # Wrong Info
    #
    wrong_info_type = models.CharField(max_length=32, blank=True, null=True, 
        choices=WRONG_INFO_TYPE_CHOICES)
    wrong_info_explain = models.TextField(blank=True, null=True)