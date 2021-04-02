from django.db import models
# Create your models here.

# HotelName,HotelAddress,HotelRating,Date,ReviewRating,ReviewTitle,ReviewText
# text,category,sentiment,rawid


class UploadFile(models.Model):
    def __str__(self):
        return self.file.name
    file = models.FileField(upload_to="rawfile")


class RawData(models.Model):
    def __str__(self):
        return str(self.id)
    id = models.IntegerField(primary_key=True)
    HotelName = models.TextField()
    HotelAddress = models.TextField()
    HotelRating = models.FloatField()
    ReviewDate = models.TextField()
    ReviewRating = models.FloatField()
    ReviewTitle = models.TextField()
    ReviewText = models.TextField(default="")


class ResultData_8(models.Model):
    def __str__(self):
        return str(self.id)
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    category = models.TextField()
    sentiment = models.BooleanField()
    date = models.TextField(default="")
    raw_text = models.TextField(default="")
    # rawid = models.IntegerField()
    # rawid = models.ForeignKey(
    #     RawData, on_delete=models.CASCADE, db_column="rawid")


class ResultData_17(models.Model):
    def __str__(self):
        return str(self.id)
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    category = models.TextField()
    sentiment = models.BooleanField()
    date = models.TextField(default="")
    raw_text = models.TextField(default="")
    # rawid = models.ForeignKey(
    #     RawData, on_delete=models.CASCADE, db_column="rawid")


class CategoryData_8(models.Model):
    def __str__(self):
        return self.title
    title = models.TextField()
    first = models.TextField()
    second = models.TextField()
    third = models.TextField()


class CategoryData_17(models.Model):
    def __str__(self):
        return self.title
    title = models.TextField()
    first = models.TextField()
    second = models.TextField()
    third = models.TextField()
