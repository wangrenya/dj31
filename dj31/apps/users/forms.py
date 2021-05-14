import re


from django import forms
from django.contrib.auth import login
from django.db.models import Q

from .models import Users
from . import constants

class LoginForm(forms.Form):
    user_account = forms.CharField()
    password = forms.CharField(max_length=20,min_length=6,
                               error_messages={
                                   'min_length':'密码长度大于6',
                                   'max_length':'密码长度小于20',
                                   'required':'密码不能为空'
                               })
    remember = forms.BooleanField(required=False)


    def __init__(self,*a,**k):
        self.request =k.pop('request')
        super().__init__(*a,**k)

    def clean_user_account(self):
        user_info = self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('用户名不能为空')

        if not re.match(r'^1[3-9]\d{9}$]', user_info) and (len(user_info)<5 or len(user_info)>20 ):
            raise forms.ValidationError('输入的用户名格式错误，请重新输入！')
        return user_info

    def clean(self):
        cleaned_data = super().clean()
        user_info = cleaned_data.get('user_account')
        pass_wd= cleaned_data.get('password')
        rmber = cleaned_data['remember']

        # 判断是否是用户名你还是手机号  Q
        user_qs = Users.objects.filter(Q(mobile=user_info) | Q(username=user_info))
        if user_qs:
            user = user_qs.first()
            # 判断密码
            if user.check_password(pass_wd):
                if rmber:
                    self.request.session.set_expiry(constants.SESSION_EXPIRY_TIME)
                else:
                    self.request.session.set_expiry(constants.SESSION_TIME)
                login(self.request,user)

            else:
                raise forms.ValidationError('用户名或密码错误，请重新输入')
        else:
            raise forms.ValidationError('用户名不存在，请重新输入！')

        return cleaned_data