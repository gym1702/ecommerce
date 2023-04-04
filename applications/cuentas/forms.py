from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        #'placeholder': 'Ingrese contraseña'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        #'placeholder': 'Confirmar contraseña'
    }))


    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']

 
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
      
    
    #Verificar qie los password sean igiuales
    def clean(self):
         cleaned_data = super(RegistrationForm, self).clean()
         password = cleaned_data.get('password')
         confirm_password = cleaned_data.get('confirm_password')

         if password != confirm_password:
              raise forms.ValidationError('El password no coincide, escriba de nuevo.')