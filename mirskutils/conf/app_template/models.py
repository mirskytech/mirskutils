from django.db import models

# enables routing by model
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.
