from django import forms
from mirskutils.forms import BootstrapForm
from localflavor.us.forms import USStateField, USZipCodeField
from .fields import *

        
        
class BillingAddressForm(BootstrapForm):
    first_name = forms.CharField(50, label="First Name")
    last_name = forms.CharField(50, label="Last Name")
    company = forms.CharField(50, label="Company", required=False)
    address = forms.CharField(60, label="Street Address")
    city = forms.CharField(40, label="City")
    state = USStateField(label="State")
    country = CountryField(label="Country", initial="US")
    zip = USZipCodeField(label="Postal / Zip Code")
    
    
class PaymentForm(BootstrapForm):
    card_number = CreditCardField(label="Credit Card Number")
    expiration_date = CreditCardExpiryField(label="Expiration Date")
    card_code = CreditCardCVV2Field(label="Card Security Code")