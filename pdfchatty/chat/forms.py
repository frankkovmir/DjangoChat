from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Nachricht eingeben...',
        'class': 'form-control'
    }))