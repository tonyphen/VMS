from django import forms
from django.urls import reverse
from apps.master_file import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button


class ProfileMasterForm(forms.ModelForm):
    class Meta:
        model = models.ProfileMaster
        fields = [
            "group_name",
            "group_id",
            "sales_target",
        ]
        widgets = {
            'group_id': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileMasterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning', onclick="window.location.href = '{}';".format(reverse('wood_definition'))))
        self.helper.layout = Layout(
            Row(
                Column('group_id', css_class="col-sm-2"),
                Column('group_name', css_class="col-sm-8"),
                Column('sales_target', css_class="col-sm-2"),
            )
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = (
            'group_master', 'profile_group', 'profile_group_description', 'profile_id', 'profile_sym',
            'description', 'bundle', 'width', 'thick', 'image'
        )
        widgets = {
            'profile_group': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'profile_sym': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('wood_definition'))))
        self.helper.layout = Layout(
            Row(
                Column('group_master', css_class="col-sm-2"),
                Column('profile_group', css_class="col-sm-2"),
                Column('profile_group_description', css_class="col-sm-4"),
                Column('profile_id', css_class="col-sm-2"),
                Column('profile_sym', css_class="col-sm-2"),
            ),
            Row(
                Column('description', css_class="col-sm-4"),
                Column('image', css_class="col-sm-3"),
                Column('width', css_class="col-sm-2"),
                Column('thick', css_class="col-sm-2"),
                Column('bundle', css_class="col-sm-1"),
            )
        )


class WoodTypeForm(forms.ModelForm):
    class Meta:
        model = models.WoodType
        fields = [
            "wood_type_id", 'sym', 'description', 'parent_id', 'freqUsed', 'wood_group', 'prod_type', 'bod_view'
        ]
        widgets = {
            'wood_type_id': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'sym': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'parent_id': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'freqUsed': forms.CheckboxInput(),
            'bod_view': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(WoodTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('wood_definition'))))
        self.helper.layout = Layout(
            Row(
                Column('wood_type_id', css_class="col-sm-2"),
                Column('sym', css_class="col-sm-2"),
                Column('description', css_class="col-sm-6"),
                Column('parent_id', css_class="col-sm-2")
            ),
            Row(
                Column('wood_group', css_class="col-sm-4"),
                Column('prod_type', css_class="col-sm-4"),
                Column('freqUsed', css_class="col-sm-1"),
                Column('bod_view', css_class="col-sm-1"),
            )
        )


class SortGroupForm(forms.ModelForm):
    class Meta:
        model = models.SortGroup
        fields = [
            'id', 'description', 'sym', 'parent', 'freqUse'
        ]
        widgets = {
            'id': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'freqUse': forms.CheckboxInput,
        }

    def __init__(self, *args, **kwargs):
        super(SortGroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('wood_definition'))))
        self.helper.layout = Layout(
            Row(
                Column('id', css_class="col-sm-1"),
                Column('description', css_class="col-sm-6"),
                Column('sym', css_class="col-sm-2"),
                Column('parent', css_class="col-sm-2"),
                Column('freqUse', css_class="col-sm-1"),
            )
        )


class LengthForm(forms.ModelForm):
    class Meta:
        model = models.Length
        fields = [
            'mm', 'feet', 'inch', 'freqUsed'
        ]
        widgets = {
            'freqUsed': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        super(LengthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('mm', css_class="col-sm-2"),
                Column('feet', css_class="col-sm-2"),
                Column('inch', css_class="col-sm-2"),
                Column('freqUsed', css_class="col-sm-2"),
            )
        )
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('wood_definition'))))


class ThickForm(forms.ModelForm):
    class Meta:
        model = models.Thick
        fields = [
            'mm', 'cm', 'inch'
        ]

    def __init__(self, *args, **kwargs):
        super(ThickForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('wood_definition'))))
        self.helper.layout = Layout(
            Row(
                Column('mm', css_class="col-sm-2"),
                Column('cm', css_class="col-sm-2"),
                Column('inch', css_class="col-sm-2"),
            )
        )


class LogScaleForm(forms.ModelForm):
    class Meta:
        model = models.LogScale
        fields = [
            'dia', 'length', 'BF'
        ]

    def __init__(self, *args, **kwargs):
        super(LogScaleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-warning',
                                     onclick="window.location.href = '{}';".format(reverse('size'))))
        self.helper.layout = Layout(
            Row(
                Column('dia', css_class="col-sm-2"),
                Column('length', css_class="col-sm-2"),
                Column('BF', css_class="col-sm-2"),
            )
        )

