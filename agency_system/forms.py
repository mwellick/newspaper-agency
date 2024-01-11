from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from agency_system.models import Redactor


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience",)


class RedactorEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience",)
