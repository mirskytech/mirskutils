from django import forms



class PlaceholderForm(forms.Form):
    
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            placeholder = self.placeholders[f] if f in self.placeholders else f.replace('_',' ')
            self.fields[f].widget.attrs = {'placeholder': placeholder}
class BootstrapForm(PlaceholderForm):
    pass
