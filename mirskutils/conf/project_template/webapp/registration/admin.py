from django.contrib import admin
from django.contrib import auth

from models import Individual


class IndividualCreationForm(auth.forms.UserCreationForm):
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Individual.objects.get(username=username)
        except Individual.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    
    class Meta:
        model = Individual
        fields = ('username',)
    
    
    
    
    
    
class IndividualChangeForm(auth.forms.UserChangeForm):
    pass


class IndividualAdmin(auth.admin.UserAdmin):
    form = IndividualChangeForm
    add_form = IndividualCreationForm
    
    pass

    
admin.site.register(Individual, IndividualAdmin)