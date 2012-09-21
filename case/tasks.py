# Copyright (c) 2012 Jason McVetta.

from django.contrib.sites.models import Site
#
from celery.task import Task
from celery.registry import tasks
#
from templated_email import send_templated_mail
#
from creditswarm.settings import DEFAULT_FROM_EMAIL
from creditswarm.settings import CREDIT_REPORTING_AGENCIES as AGENCIES
#
from case.models import Case


class SendDisputeEmailTask(Task):
    '''
    Sends dispute emails
    '''
    
    def run(self, case_obj, **kwargs):
        '''
        Sends a dispute email for a given Case object.
        '''
        case_obj.email_cra()
        
tasks.register(SendDisputeEmailTask)