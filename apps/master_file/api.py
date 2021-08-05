import json
from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

from django.conf import settings
from apps.master_file import models


class AjaxProductList(View):
    def get(self, request):
        products = self._datatables(request)
        return HttpResponse(json.dumps(products, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request):
        datatables = request.GET
        main_cat = datatables.get("main_cat")
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        search = datatables.get('search[value]')
        records_total = models.Product.objects.filter(warehouse_id=main_cat).count()
        records_filtered = records_total
        products = models.Product.objects.filter(warehouse_id=main_cat).order_by('category', 'code')
        if search:
            products = models.Product.objects.filter(
                Q(warehouse__id__icontains=search) |
                Q(category__id__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search) |
                Q(profile__profile_id__icontains=search) |
                Q(wood_type__wood_type_id__icontains=search) |
                Q(unit__unit__icontains=search)
            )
            records_total = products.count()
            records_filtered = records_total

        paginator = Paginator(products, length)
        # page_number = start / length + 1
        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = [
            {
                'warehouse': prod.warehouse.description,
                'category': prod.category.description,
                'code': prod.code,
                'description': prod.description,
                'profile': prod.profile.profile_sym,
                'color': prod.color_id,
                'wood_type': prod.wood_type.sym,
                'unit': prod.unit.unit,
                'min_qty': prod.min_qty,
                'max_qty': prod.max_qty
            } for prod in object_list
        ]
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data
        }


class AjaxColorList(View):
    def get(self, request):
        colors = self._datatables(request)
        return HttpResponse(json.dumps(colors, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request):
        datatables = request.GET
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        search = datatables.get('search[value]')
        records_total = models.Color.objects.all().count()
        records_filtered = records_total
        colors = models.Color.objects.all().order_by('color_group', 'color_id')
        if search:
            colors = models.Color.objects.filter(
                Q(color_group__icontains=search) |
                Q(color_id__icontains=search) |
                Q(description__icontains=search) |
                Q(sort_group__icontains=search) |
                Q(sort_group_note__icontains=search) |
                Q(wood_type__icontains=search) |
                Q(gloss__icontains=search)
            )
            records_total = colors.count()
            records_filtered = records_total

        paginator = Paginator(colors, length)
        # page_number = start / length + 1
        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = [
            {
                'color_group': color.color_group,
                'color_id': color.color_id,
                'description': color.description,
                'wood_type': color.wood_type_id,
                'sort_group': color.sort_group_id,
                'sort_group_note': color.sort_group_note,

                'gloss': color.gloss,
                'printed': color.printed,
                'distressed': color.distressed,
                'distressed_remark': color.distressed_remark,
                'phun_hot': color.phun_hot,
                'emboss': color.emboss,
                'scratch': color.scratch,
                'glazed': color.glazed,
                'danh_bui': color.danh_bui,
                'remark': color.remark
            } for color in object_list
        ]
        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data
        }



