import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from piplmesh.account import fields

class LimitedDateTimeField(forms.DateTimeField):
    default_error_messages = forms.DateTimeField.default_error_messages.copy()
    default_error_messages.update({
        'bounds': _(u"Value is out of bounds."),
    })

    def __init__(self, upper_limit=None, lower_limit=None, input_formats=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            raise AttributeError
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            raise AttributeError

        super(LimitedDateTimeField, self).__init__(input_formats=None, *args, **kwargs)

    def clean(self, value):
        value = super(LimitedDateTimeField, self).clean(value)

        def error():
            raise forms.ValidationError(self.error_messages['bounds'])

        fields.limit_date(value, self.lower_limit, self.upper_limit, error)

        return value