from django.contrib import admin
from .models import UploadFile
from .models import RawData
from .models import ResultData_8
from .models import ResultData_17
from .models import CategoryData_8
from .models import CategoryData_17

# Register your models here.
admin.site.register(UploadFile)
admin.site.register(RawData)
admin.site.register(ResultData_8)
admin.site.register(ResultData_17)
admin.site.register(CategoryData_8)
admin.site.register(CategoryData_17)
