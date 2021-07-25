from django import forms
from django.conf import settings
from django.shortcuts import render, redirect
from openpyxl import load_workbook
from tablib import Dataset

from apps.master_file import models, forms, resources


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
        file_name = request.FILES['fileName'].name
        upload_file = request.FILES['fileName']
        workbook = load_workbook(upload_file, read_only=True)
        # Get name of the first sheet and open the sheet name
        first_sheet = workbook.get_sheet_names()[0]
        worksheet = workbook.get_sheet_by_name(first_sheet)
        data = []
        if file_name == 'Length_Master.xlsx':
            for row in worksheet.iter_rows(min_row=2):
                length = models.Length()
                length.feet = round(row[0].value,4)
                length.inch = round(row[1].value,2)
                length.mm = int(row[2].value)
                if row[3].value == 1:
                    length.freqUsed = True
                else:
                    length.freqUsed = False
                data.append(length)
            models.Length.objects.bulk_create(data)
        return redirect('wood_definition')

    return render(request, 'master_file/master_file_upload.html')
