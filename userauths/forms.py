from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ImageField, FileInput, TextInput, Select

from userauths.models import Profile, User

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder':'Họ tên'}), 
                                max_length=100, required=True,error_messages={'required' : 'Vui lòng nhập họ tên'})
    username = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder':'Tài khoản'}), 
                               max_length=100, required=True,error_messages={'required' : 'Vui lòng nhập tài khoản'})
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder':'SĐT'}), 
                            max_length=100, required=True,error_messages={'required' : 'Vui lòng nhập số điện thoại'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': '' , 'id': "", 'placeholder':'Email'}), 
                             required=True,error_messages={'required' : 'Vui lòng nhập Email'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder':'Mật khẩu'}), 
                                required=True,error_messages={'required' : 'Vui lòng nhập mật khẩu'})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder':'Xác nhận mật khẩu'}), 
                                required=True,error_messages={'required' : 'Vui lòng nhập xác nhận mật khẩu'})
    # gender = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'with-border' , 'id': "", 'placeholder':'Enter Gender'}))
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2', 'phone', 'gender']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'with-border'
            # visible.field.widget.attrs['placeholder'] = visible.field.label


class ProfileUpdateForm(forms.ModelForm):
    image = ImageField(widget=FileInput)
    
    class Meta:
        model = Profile
        fields = [
            'cover_image' ,
            'image' ,
            'full_name', 
            'bio', 
            'about_me', 
            'phone',
            'gender',
            'relationship',
            'friends_visibility',
            'country', 
            'city', 
            'state', 
            'address', 
            'working_at',
            'instagram',
            'whatsApp',
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']