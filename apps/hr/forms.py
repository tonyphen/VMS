from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from apps.hr import models


class HCForm(forms.ModelForm):
    class Meta:
        model = models.HealthCheck

        fields = [
            "name",
            "ngay",
            "noi_dung",
            "hc_image",
            "attachment",
        ]
        widgets = {
            'ngay': DatePickerInput(format='%d/%m/%Y'),
        }

    def __init__(self, *args, **kwargs):
        super(HCForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Row (
               Column('name', css_class="col-sm-12")
            ),
            Row(
                Column('ngay'), Column('hc_image'), Column('attachment'),
            ),

            Row(
                Column('noi_dung')
                )
        )


class HCItemForm(forms.ModelForm):
    class Meta:
        model = models.HealthCheckItem
        fields = [
            "stt", "ho_ten", "msnv", "ngay_sinh", "so_bhyt", "gioi_tinh", "cmnd", "cong_ty", "dia_chi", "so_dt",
            "ngay_kham", "gio_kham", "gio_ketthuc", "status", "completed",
        ]
        widgets = {
            'ho_ten': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'ngay_sinh': DatePickerInput(format='%Y-%m-%d'),
            'ngay_kham': DatePickerInput(format='%Y-%m-%d'),
            'gio_kham': TimePickerInput(format='%H:%M'),
            'gio_ketthuc': TimePickerInput(format='%H:%M'),
            'completed': forms.CheckboxInput,
        }

    def __init__(self, *args, **kwargs):
        super(HCItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Row(
                Column('stt', css_class='col-sm-1'), Column('ho_ten', css_class='text-uppercase col-sm-4'),
                Column('msnv', css_class='col-sm-1'),
                Column('ngay_sinh', css_class='col-sm-2'),
                css_class='p-0'
            ),
            Row(
                Column('gioi_tinh', css_class='col-sm-1'), Column('so_bhyt', css_class='col-sm-2'), Column('cmnd', css_class='col-sm-2'),
                css_class='p-0'),
            Row(
                Column('so_dt', css_class='col-sm-2'), Column('dia_chi', css_class='col-sm-8'),
                Column('cong_ty', css_class='col-sm-2'),
            ),
            Row(
                Column('ngay_kham', css_class='col-sm-2'), Column('gio_kham', css_class='col-sm-2'),
                Column('gio_ketthuc', css_class='col-sm-2'), Column('status', css_class='col-sm-2'),
                Column('completed', css_class='col-sm-2'), css_class='d-flex align-items-end'
            )
        )

