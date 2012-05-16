import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.forms import widgets
from django.forms.extras import widgets as extras_widgets
from django.utils import encoding, safestring
from django.utils.translation import ugettext_lazy as _

from piplmesh.account import fields, form_fields, models

class RadioFieldRenderer(widgets.RadioFieldRenderer):
    """
    RadioSelect renderer which adds ``first`` and ``last`` style classes
    to first and last radio widgets.
    """

    def _render_widgets(self):
        for i, w in enumerate(self):
            classes = []
            if i == 0:
                classes.append('first')
            if i == len(self.choices) - 1:
                classes.append('last')

            cls = ''
            if classes:
                cls = u' class="%s"' % (u' '.join(classes),)

            yield u'<li%s>%s</li>' % (cls, encoding.force_unicode(w))

    def render(self):
        return safestring.mark_safe(u'<ul>\n%s\n</ul>' % (u'\n'.join(self._render_widgets())),)

class RegistrationForm(auth_forms.UserCreationForm):
    """
    Class with user registration form.
    """

    # Required data
    email = forms.EmailField(label=_("E-mail"))
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

    # Additional information
    gender = forms.ChoiceField(
        label=_("Gender"),
        required=False,
        choices=fields.GENDER_CHOICES,
        widget=forms.RadioSelect(renderer=RadioFieldRenderer),
    )
    birthdate = form_fields.LimitedDateTimeField(
        upper_limit=models.upper_birthdate_limit,
        lower_limit=models.lower_birthdate_limit,
        label=_("Birth date"),
        required=False,
        widget=extras_widgets.SelectDateWidget(
            years=[
                y for y in range(
                    models.upper_birthdate_limit().year,
                    models.lower_birthdate_limit().year,
                    -1,
                )
            ],
        ),
    )

    def clean_password2(self):
        # This method checks whether the passwords match
        if self.cleaned_data.has_key('password1') and self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(_("Passwords do not match."))

    def clean_username(self):
        # This method checks whether the username exists in case-insensitive manner
        username = self.cleaned_data['username']
        if models.User.objects(username__iexact=username).count():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def save(self):
        # We first have to save user to database
        new_user = models.User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            birthdate=self.cleaned_data['birthdate'],
        )

        new_user.set_password(self.cleaned_data['password2'])
        new_user.save()

        return self.cleaned_data['username'], self.cleaned_data['password2']

    def validate_unique(self):
        # validate_unique() is called on model instance and our MongoEngine 
        # objects do not have this, so this function doesn't do anything
        pass
