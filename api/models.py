from django.db import models
from django.contrib.auth.models import User
from .utils import sendTransaction
import hashlib

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateField(auto_now_add=True)
    title = models.TextField( default= 'None')
    content = models.TextField()
    hash = models.CharField(max_length=32,default= None,  null = True)
    txId = models.CharField(max_length=66,default= None,  null = True)

    def __str__(self):
        return self.title

    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()
