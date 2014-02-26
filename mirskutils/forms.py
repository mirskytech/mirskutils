from django import forms



class PlaceholderForm(forms.Form):
    """
    Description:
        the ``placeholder`` attribute is common but none of the django widgets
        include it by default. extending from this form, widgets will take their
        ``placeholder`` attribute value from (in priority order):
        
        *  ``placeholders`` object attribute with dictionary name/placeholder pairings
        *  from a widget's label attribute
        *  from a widget's name
    
    """
    
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for name,field in self.fields.iteritems():
            label = field.label if field.label else name
            placeholder = self.placeholders[name] if name in self.placeholders else label.replace('_',' ')
            self.fields[name].widget.attrs = {'placeholder': placeholder}
            
class BootstrapForm(PlaceholderForm):
    """alias for PlaceholderForm as bootstrap 3 ``styles form-control`` with placeholders in mind"""
    pass
