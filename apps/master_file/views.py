from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from tablib import Dataset
from django.http import HttpResponse

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
        'length_list': qsLength,
        'pageLength': pageLength
    }
    return render(request, 'master_file/wood_definition.html', context)


def wdefinition_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        file_name = request.FILES['fileName'].name
        upload_file = request.FILES['fileName']
        imported_data = dataset.load(upload_file.read(), format='xlsx')
        if file_name == 'Length_Master.xlsx':
            freqused = False
            for data in imported_data:
                if str(data[3]) == "True":
                    freqused = True
                else:
                    freqused = False
                print(str(data[3]))
                value = models.Length(
                    round(float(data[0]), 2), round(float(data[1]), 2), int(data[2]), freqused
                )
                value.save()
        return redirect('wood_definition')

    return render(request, 'master_file/master_file_upload.html')
