from django import forms


class SearchSchoolForm(forms.Form):
    school_name = forms.CharField(label='Enter School Name')
