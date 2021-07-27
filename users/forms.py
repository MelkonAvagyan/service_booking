from django import forms
from .models import ClientProfile, Message, Reviews, SpecialistProfile


class SpecialistProfileForm(forms.ModelForm):
    class Meta:
        model = SpecialistProfile
        fields = '__all__'
                  
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'description_bio': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            }
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items(): 
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(forms.ModelFormModelForm):
    class Meta:
        model = Reviews
        fields = ['description','value', 'rating']

        labels = {
            'value': 'Place your vote',
            'description': 'Add a comment with your vote',
            'rating' : 'Rate the specialist'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

