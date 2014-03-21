from django import forms
from mirskutils.forms import BootstrapForm
from localflavor.us.forms import USStateField, USZipCodeField
from .fields import *
from .creditcard import CreditCard
        
        
class BillingAddressForm(BootstrapForm):
    first_name = forms.CharField(50, label="First Name")
    last_name = forms.CharField(50, label="Last Name")
    company = forms.CharField(50, label="Company", required=False)
    address = forms.CharField(60, label="Street Address")
    city = forms.CharField(40, label="City")
    state = USStateField(label="State")
    country = CountryField(label="Country", initial="US")
    zip = USZipCodeField(label="Postal / Zip Code")
    
    def as_stripe(self):
        return { 
            "name": "%s %s" % (self.cleaned_data['first_name'], self.cleaned_data['last_name']),
            "address_line1": self.cleaned_data['address'],
            "address_line2": None,
            "address_city": self.cleaned_data['city'],
            "address_state": self.cleaned_data['state'],
            "address_zip": self.cleaned_data['zip'],
            "address_country": self.cleaned_data['country'],
        }   
    
    def as_authorizenet(self):
        
        return {}
    
    
class PaymentForm(BootstrapForm):
    card_number = CreditCardField(label="Credit Card Number")
    expiration_date = CreditCardExpiryField(label="Expiration Date")
    card_code = CreditCardCVV2Field(label="Card Security Code")
    
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        
    def clear_cc_fields(self):
        self.data['card_number'] = ''
        self.data['card_code'] = ''
    
    def as_stripe(self):
        return {
            "number": self.cleaned_data['card_number'],
            "type": CreditCard(self.cleaned_data['card_number']).get_type(),
            "exp_month": self.cleaned_data['expiration_date'].month,
            "exp_year": self.cleaned_data['expiration_date'].year,
            "cvc":self.cleaned_data['card_code']
          }
    
    def as_authorizenet(self):
        
        return {}    