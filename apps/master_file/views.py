import decimal
import string
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

        if file_name == 'profiles.xlsx':
            for row in worksheet.iter_rows(min_row=2):
                profile = models.Profile()
                profile.group_master = models.ProfileMaster.objects.get(group_id=row[0].value)
                profile.profile_group = row[1].value
                profile.profile_group_description = str(row[2].value).upper()
                profile.profile_id = str(row[3].value).upper()
                profile.profile_sym = str(row[4].value).upper()
                profile.description = str(row[5].value).upper()
                profile.image = None
                profile.width = round(float(row[6].value),2)
                profile.thick = round(float(row[7].value),3)
                profile.CBM_Feet = round(float(row[8].value),6)
                profile.M2_Feet = round(float(row[9].value),6)
                profile.bundle = int(row[10].value)
                profile.save()
            # models.Profile.objects.bulk_create(data)

        if file_name == 'sortgroup.xlsx':
            for row in worksheet.iter_rows(min_row=2):
                sortgroup = models.SortGroup()
                sortgroup.id = row[0].value
                sortgroup.description = row[1].value
                sortgroup.sym = str(row[2].value).upper()
                sortgroup.parent = row[3].value
                if row[4].value == 1:
                    freqused = True
                else:
                    freqused = False

                sortgroup.freqUse = freqused
                sortgroup.save()

        if file_name == 'WoodType.xlsx':
            for row in worksheet.iter_rows(min_row=2):
                wt = models.WoodType()
                wt.wood_type_id = row[0].value
                wt.description = str(row[1].value).upper()
                wt.parent_id = row[2].value
                if row[3].value == 1:
                    freqused = True
                else:
                    freqused = False
                wt.freqUsed = freqused
                wt.wood_group = row[4].value
                wt.prod_type = row[5].value
                wt.sym = str(row[6].value).upper()
                if row[7].value == 1:
                    bodview = True
                else:
                    bodview = False
                wt.bod_view = bodview
                wt.save()

        return redirect('wood_definition')

    return render(request, 'master_file/master_file_upload.html')
