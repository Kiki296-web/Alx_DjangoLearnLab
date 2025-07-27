from django import forms

class ExamplrForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)