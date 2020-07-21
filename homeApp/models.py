from django.db import models

# Create your models here.
# Models are used to create tables in db
class Contact(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    content = models.TextField()
    # Taking the timestamp for the entry
    timeStamp = models.DateTimeField(auto_now_add=True, blank = True)

    def __str__(self):
        return 'Message from:- ' + self.name
    
