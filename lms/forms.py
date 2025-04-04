import datetime

from django import forms
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy

class RenewBookInstanceDate(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check if a date renew is in the Past
        if data < datetime.date.today():
            raise ValidationError(gettext_lazy('Invalid date - renewal date in past'))

        #Check if a date is in the allowed Range(+4 Weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(gettext_lazy("Invalid date - renewal more than 4 weeks ahead"))

        return data


class RenewBookInstanceDueBackDateRecreate(forms.Form):
    renewal_date_recreate = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date_recreate(self):

        data = self.cleaned_data['renewal_date_recreate']

        #Check if the renew Date is in the Past

        if data < datetime.date.today():
            raise ValidationError(gettext_lazy('Invalid -- Date in the Past'))
        
        #Check if the renew date is over 4weeks 
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(gettext_lazy('Invalid date - renewal more than 4 weeks ahead'))
        
        return data

class SearchBook(forms.Form):

    search_query = forms.CharField(
        max_length=200,
        required=False,
        label="Search Book:",
        widget=forms.TextInput(attrs={"placeholder": 'Search Book..'})
    )

    def clean_search_query(self):
        data = self.cleaned_data['search_query']

        return data