from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Type your message here',
        'class': 'form-control'
    }))