from django.db import models

# Create your models here.

try:
    from api.v0.model01 import *
except ImportError:
    pass
