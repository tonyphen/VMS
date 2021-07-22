from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.conf import settings
from tablib import Dataset

from apps.basic.utilities import created_updated, HealthCheckItemResource
from apps.hr import models, forms


@login_required
def hc_chart(request, id):
    label = []
    data = []

    qs = models.HealthCheckItem.objects.filter(hc_id=id, status__isnull=False).values('status').annotate(count=Count('ho_ten'))
    for item in qs:
        label.append(item['status'])
        data.append(item['count'])
    print(label,data)
    return JsonResponse(data={
        'label': label,
        'data': data,
    })


def hc_list(request):
    hc_list = models.HealthCheck.objects.all()
    return render(request, 'hr/hc_list.html', {'hc_list': hc_list})


def hc_create(request):
    form = forms.HCForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            created_updated(models.HealthCheck, request)
            return redirect('hc_list')

    return render(request, 'hr/hc_add.html', {'form': form})


def hc_update(request, id):
    obj = get_object_or_404(models.HealthCheck, id=id)
    form = forms.HCForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('hc_list')
    return render(request, "hr/hc_update.html", {'form': form})


def hc_delete(request, id):
    obj = get_object_or_404(models.HealthCheck, pk=id)
    if request.method == "POST":
        obj.delete()
        return redirect('hc_list')
    return render(request, "hr/hc_delete.html", {'hc': obj})

# ================ Items detail ====================

def hc_items(request, hc_id):
    items = models.HealthCheckItem.objects.filter(hc=hc_id)
    hc = get_object_or_404(models.HealthCheck, id=hc_id)
    pageLength = settings.PAGE_LENGTH
    return render(request, 'hr/hc_items.html', {'hc_items': items, 'hc_id': hc_id, 'hc': hc, 'pageLength': pageLength})


def hc_item_create(request, hc_id):
    form = forms.HCItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.hc_id = hc_id
            form.save()
            return redirect('hc_items', hc_id=hc_id)

    return render(request, 'hr/hc_item_create.html', {'form': form, 'hc_id': hc_id})


def hc_item_update(request, hc_id, id):
    obj = get_object_or_404(models.HealthCheckItem, id=id)
    form = forms.HCItemForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.instance.hc_id = hc_id
        form.save()
        return redirect('hc_items', hc_id)

    return render(request, "hr/hc_item_update.html", {'form': form, 'hc_id': hc_id, 'id': id})


def hc_item_delete(request, hc_id, id):
    obj = get_object_or_404(models.HealthCheckItem, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('hc_items', hc_id=hc_id)
    return render(request, "hr/hc_item_delete.html", {'item': obj, 'hc_id': hc_id})


def hc_item_upload(request, hc_id):
    if request.method == 'POST':
        hc_resource = HealthCheckItemResource()
        dataset = Dataset()

        new_hc_items = request.FILES['hc_itemlist']

        imported_data = dataset.load(new_hc_items.read(), format='xlsx')
        for data in imported_data:
            value = models.HealthCheckItem(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                data[10], data[11], data[12], data[13], data[14], data[15], data[16]
            )
            value.save()
        return redirect('hc_items', hc_id=hc_id)

    return render(request, 'hr/hc_item_upload.html', {'hc_id': hc_id})
