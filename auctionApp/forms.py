from django import forms
from django.forms import ModelForm 
from django.contrib.auth.hashers import check_password
from .models import User,Product


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        
        fields = ('email','password','confirm_password','user_type','first_name','last_name','mobile')
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-sm'}),
            'password' : forms.PasswordInput(attrs={'class':'form-sm'}),
            # 'user_type' : forms.OptionInput(attrs={'class':'form-sm'}),
            'first_name' : forms.TextInput(attrs={'class':'form-sm'}),
            'last_name' : forms.TextInput(attrs={'class':'form-sm'}),
            'mobile' : forms.TextInput(attrs={'class':'form-sm'}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
    

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['creator','category','product_bid_time','min_bid_amount','product_name','product_description','product_image_name','product_image_path']
        
        # widgets = {
        #     'creator': forms.ChoiceField(attrs={'class':'form-control'})
        # }