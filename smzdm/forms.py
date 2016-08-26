from django import forms
import re



class LoginForm(forms.Form):
    username = forms.CharField(
            required=True,
            label="用户名",
            error_messages={'required': '请输入用户名'},
            widget=forms.TextInput(
                    attrs={
                        'placeholder': "用户名",
                    }
            ),
    )
    password = forms.CharField(
            required=True,
            label="密码",
            error_messages={'required': '请输入密码'},
            widget=forms.PasswordInput(
                    attrs={
                        'placeholder': "密码",
                    }
            ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()
            return cleaned_data

from django.core.exceptions import ValidationError

def validate_num(value):
    try:
        int(value)
    except:
        raise ValidationError('%s is not an number' % value)

class UserForm(forms.Form):
    username = forms.CharField(
            required=True,
            label="用户名",
            error_messages={'required': '请输入用户名'},
            widget=forms.NumberInput(
                    attrs={
                        'placeholder': "目前只支持QQ邮箱，请输入QQ号",
                        'id':'username',
                    }
            ),
            validators=[validate_num]
    )
    password = forms.CharField(
            required=True,
            label="密码",
            error_messages={'required': '请输入密码'},
            widget=forms.PasswordInput(
                    attrs={
                        'placeholder': "密码",
                        'id':'password',
                    }
            ),
    )

    password_again = forms.CharField(
            required=True,
            label="确认密码",
            error_messages={'required': '请输入密码'},
            widget=forms.PasswordInput(
                    attrs={
                        'placeholder': "确认密码",
                        'id':'password_again',
                    }
            ),
    )

    nick_name=forms.CharField(
        required=True,
        label='昵称',
        error_messages={'required':'请输入昵称'},
        widget=forms.PasswordInput(
                attrs={
                    'placeholder': "昵称",
                    'id':'nick_name',
                }
        ),
    )