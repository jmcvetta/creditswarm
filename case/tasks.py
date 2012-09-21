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
        #c = Case.objects.get(pk=case_pk)
        send_templated_mail(
            template_name = 'cra_dispute_notification',
            from_email = DEFAULT_FROM_EMAIL,
            recipient_list = [AGENCIES[case_obj.agency]['email'],],
            context = {
                'object': case_obj,
                'current_site': Site.objects.get_current(),
                },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_ 
            template_suffix = 'html',
            )
        case_obj.status = 'S'
        case_obj.save()
        
tasks.register(SendDisputeEmailTask)