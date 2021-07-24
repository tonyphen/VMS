from django.conf import settings
from django.shortcuts import render

from apps.master_file import models
from apps.master_file import forms

def profile_master(request):
    qs = models.ProfileMaster.objects.all().order_by('group_id')
    pageLength = settings.PAGE_LENGTH
    return render(request, 'master_file/profile_master.html', {'items': qs, 'pageLength': pageLength})


def wood_definition(request):
    qsProfile_Master = models.ProfileMaster.objects.all().order_by('group_id')
    qsProfile = models.Profile.objects.all().order_by('profile_id')
    qsWoodType = models.WoodType.objects.all().order_by('wood_type_id')
    qsSortGroup = models.SortGroup.objects.all().order_by('id')
    qsLength = models.Length.objects.all().order_by('feet')

    pageLength = settings.PAGE_LENGTH
    context = {
        'profile_master_list': qsProfile_Master,
        'profile_list': qsProfile,
        'wood_type_list': qsWoodType,
        'soft_group_list': qsSortGroup,
        'pageLength': pageLength
    }
    return render(request, 'master_file/wood_definition.html', context)

