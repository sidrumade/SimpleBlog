from django import forms
from django.core.mail import send_mail
from .models import Comment
class EmailForm(forms.Form):
    # from_email = forms.EmailField()
    to_email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email '
        }
    ))
    subject = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subject '
        }
    ))




    def send_email(self,context):
        # print(self.cleaned_data['from_email'])
        # print(self.cleaned_data['to_email'])
        # print(self.cleaned_data['email_sub'])
        # print(self.cleaned_data['email_content'])
        print('context',context)
        post=context['post']
        send_mail(self.cleaned_data['subject'],
                  post.body,
                  'siddhesh.djangoapplication@gmail.com',
                  [self.cleaned_data['to_email']],
                  fail_silently=False,)

class CommentForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Name '
        }
    ))
    email=forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email '
        }
    ))
    body=forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Comment '
        }
    ))

    class Meta:
        model = Comment
        fields = ('name','email','body')
