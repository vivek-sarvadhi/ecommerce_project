from django import forms 
from users.models import CustomUser
from django.utils.translation import gettext as _
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError


class CustomUserForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('email','first_name','last_name','user_type','profile_image','phone_number','address','password')
		widgets = {
			'email':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),
			'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
			'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
			'user_type':forms.Select(attrs={'class':'form-control', 'placeholder':'User type'}),
			'profile_image':forms.FileInput(attrs={'class':'form-control'}),
			'phone_number':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'enter phone number'}),
			'address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'enter address'}),
			'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
		}


	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			match = CustomUser.objects.get(email=email)
			print(match)
		except CustomUser.DoesNotExist:
			return email
		raise forms.ValidationError("this email address already use")


class ProfileUserForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ('profile_image','phone_number','address')
		widgets = {
			'user_type':forms.Select(attrs={'class':'form-control', 'placeholder':'User type'}),
			'profile_image':forms.FileInput(attrs={'class':'form-control'}),
			'phone_number':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'enter phone number'}),
			'address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'enter address'}),
		}



class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
