from django.contrib import admin

from . import models

admin.site.register(models.Field)
admin.site.register(models.Product)

admin.site.register(models.ColumnProfile)
admin.site.register(models.ColumnProfileField)

admin.site.register(models.ProductChangeLog)
admin.site.register(models.EventLog)

admin.site.register(models.UserSetting)

admin.site.register(models.AdminSetting)

admin.site.register(models.ShortCodeChange)

