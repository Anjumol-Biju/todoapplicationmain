from django.db import models

# Create your models here.
class Todo(models.Model):
    tittle=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True,blamk=True)
    user=models.CharField(max_length=200)
    options=(
        ("complete","complete")
        ("pending","pending")
        ("inprogress","inprogress")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")
    
    
    def __str__(self):
        return self.tittle