import unicodedata
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from .models import *
from user.models import User

UserModel = get_user_model()

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
        }

class MainForm(forms.Form):
    start_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город отправления', required=True)
    end_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город прибытия', required=True)
    start_date = forms.DateField(label='Дата отправления', required=True)

    def clean_start_date_date(self):
        data = self.cleaned_data['start_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - start_date in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=8):
            raise ValidationError(_('Invalid date - start_date more than 8 weeks ahead'))

        return data


class LoginForm(forms.ModelForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwarks):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwarks)
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        self.fields['email'].label = 'E-mail'
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)
        self.fields['password'].label = 'Пароль'


    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, email):
        if not email.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )

class LoginForm2(forms.Form):
    email = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        # self.email = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
        # self.password = forms.CharField(
        #     label=_("Password"),
        #     strip=False,
        #     widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        # )
        # self.request = request
        # self.user_cache = None
        # super().__init__(*args, **kwarks)
        # self.fields['email'].label = 'E-mail'
        # self.fields['password'].label = 'Пароль'
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    # class Meta:
    #     model = User
    #     fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, email):
        if not email.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )

class RegForm(forms.ModelForm):
    def __init__(self, *args, **kwarks):
        super().__init__(*args, **kwarks)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
        self.fields['email'].label = 'E-mail'
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = User
        fields = ['email', 'password']

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            password_validation.validate_password(password, self.instance)

    def save(self, commit=True):
        email = super().save(commit=False)
        email.set_password(self.cleaned_data["password"])
        if commit:
            email.save()
        return email
        
class BuyForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user','train','carriage', 'places']

    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','third_name']

    
