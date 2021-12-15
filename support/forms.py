from django import forms


class NewTicketForm(forms.Form):
    customer_email = forms.EmailField(label='Your email', max_length=100)
    issue = forms.CharField(widget=forms.Textarea, label='Your issue')
