from django import forms

from chat.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        self.recipient = kwargs.pop('recipient', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        message = super().save(commit=False)
        message.sender = self.instance
        message.recipient = self.recipient
        if commit:
            message.save()
        return message