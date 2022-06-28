from django.db import models


class InstaStorage(models.Model):

    access_token = models.CharField(max_length=299)
    account_id = models.CharField(max_length=299)
    app_id = models.CharField(max_length=299)
    app_secret = models.CharField(max_length=299)
