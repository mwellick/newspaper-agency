from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm,
                                       )

from agency_system.models import Redactor


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "years_of_experience",)

    def __init__(self, *args, **kwargs):
        super(RedactorCreationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class RedactorEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "years_of_experience",)

    def __init__(self, *args, **kwargs):
        super(RedactorEditForm, self).__init__(*args, **kwargs)
        self.fields.pop("password")
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class PasswordsChangingForm(PasswordChangeForm):
    class Meta(PasswordChangeForm):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("old_password", "new_password1", "new_password2",)


class PasswordsResettingForm(PasswordResetForm):
    class Meta(PasswordResetForm):
        model = Redactor


class PasswordsResettingFormConfirm(SetPasswordForm):
    class Meta(SetPasswordForm):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("email", "new_password", "new_password2",)