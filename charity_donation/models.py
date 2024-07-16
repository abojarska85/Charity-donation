from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    INSTITUTION_TYPE = (
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna')
    )
    type = models.IntegerField(choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.name}, {self.description}, {self.type}"
