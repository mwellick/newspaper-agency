from string import ascii_letters

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

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("First name can contain only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("Last name can contain only letters")
        return last_name


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

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("First name can contain only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("Last name can contain only letters")
        return last_name


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
    name = forms.CharField(max_length=30, required=False,
                           label="",
                           widget=forms.TextInput(attrs={"placeholder": "Search by topic name"})
                           )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(max_length=30,
                               required=False,
                               label="",
                               widget=forms.TextInput(attrs={"placeholder": "Search by username"}))


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(max_length=64,
                            required=False,
                            label="",
                            widget=forms.TextInput(attrs={"placeholder": "Search news by title"}))
