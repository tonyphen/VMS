from django.conf import settings
from django.shortcuts import render

from apps.master_file import models
from apps.master_file import forms

def profile_master(request):
    qs = models.ProfileMaster.objects.all().order_by('group_master__profile_id')
    pageLength = settings.PAGE_LENGTH
    return render(request, 'master_file/profile_master.html', {'items': qs, 'pageLength': pageLength})

