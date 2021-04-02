from django import forms

from .models import UploadFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file',)

class barChart(forms.Form):
    category = forms.CharField(max_length=10)
    print(category)
        
# class Login(forms.ModelForm):
#     class Meta:
#         model = Login
#         fields = ['trinity_id', 'trinity_password']
#         widgets = {
#             'trinity_id': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#             'trinity_password': forms.PasswordInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             )
#         }
