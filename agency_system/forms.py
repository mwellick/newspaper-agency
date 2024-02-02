from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm,
                                       )

from agency_system.models import Redactor, Comment, ReplyComment


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
        fields = UserCreationForm.Meta.fields + (
            "profile_images", "first_name", "last_name", "bio", "email", "years_of_experience",)

    def __init__(self, *args, **kwargs):
        super(RedactorEditForm, self).__init__(*args, **kwargs)
        self.fields.pop("password")
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["bio"].required = False


class PasswordChangingForm(PasswordChangeForm):
    class Meta(PasswordChangeForm):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("old_password", "new_password1", "new_password2",)


class PasswordResettingForm(PasswordResetForm):
    class Meta(PasswordResetForm):
        model = Redactor


class PasswordResettingFormConfirm(SetPasswordForm):
    class Meta(SetPasswordForm):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("email", "new_password", "new_password2",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ["reply_body"]


class TopicSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False,
                            label="",
                            widget=forms.TextInput(attrs={"placeholder": "Search by topic name"})
                            )
