from django.db import models

import os
import re
import time

from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin, User


class Individual(AbstractUser):
    
    def __unicode__(self):
        if self.first_name and self.last_name:
            return "%s %s." % (self.first_name, self.last_name[:1])
        if self.first_name:
            return "%s" % (self.first_name)
        if self.email:
            return "%s" % self.email
        return "%s" % self.username
