from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

from authentication.models import User

from . import widgets

class Product(models.Model):
    sku = models.CharField(max_length=31, unique=True, primary_key=True, verbose_name="SKU")
    # part_number = models.CharField(max_length=63, unique=True, verbose_name="SKU")
    data = JSONField(verbose_name="Product Data")
    backup_data = JSONField(default=dict, verbose_name="Product Data Backup")

    modified = models.BooleanField(default=False, verbose_name="Product Data Updated?")

    def __str__(self):
        return self.sku
    
    # because ordering incurs a cost
    # class Meta:
    #    ordering = ['sku']

class ProductBackup(models.Model):
    sku = models.CharField(max_length=31, unique=True, primary_key=True, verbose_name="SKU")
    part_number = models.CharField(max_length=63, unique=True, verbose_name="SKU")
    data = JSONField(verbose_name="Product Data")

    def __str__(self):
        return self.sku


class ShortCodeChange(models.Model):
    part_number = models.CharField(max_length=63, unique=True, primary_key=True, verbose_name="Part Number")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    data = JSONField(verbose_name="Product Data")


class Field(models.Model):
    name = models.CharField(max_length=63, unique=True, db_index=True, verbose_name="Field Name")
    label = models.CharField(max_length=63, verbose_name="Field Label")
    max_length = models.IntegerField(default=255, verbose_name="Field Max Length")
    min_length = models.IntegerField(default=0, verbose_name="Field Min Length")

    class FieldType(models.IntegerChoices):
        DATA = 0
        SHORTCODE = 1
        RESULT = 2
    
    field_type = models.IntegerField(choices=FieldType.choices, default=FieldType.DATA)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['pk']


class ColumnProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, verbose_name="User")
    description = models.CharField(max_length=63, verbose_name="Column Profile Description")

    def __str__(self):
        return f'{self.user.username} - {self.description}'

    class Meta:
        ordering = ['pk', 'user']


class ColumnProfileField(models.Model):
    column_profile = models.ForeignKey(ColumnProfile, on_delete=models.CASCADE, db_index=True, verbose_name="Column Profile")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="Corresponding Field")
    order = models.IntegerField(default=10000, verbose_name="Field Order")
    visible = models.BooleanField(default=True, verbose_name="Field Visible?")

    def __str__(self):
        return f'{self.column_profile.user.username} - {self.column_profile.description} - {self.field.name}'
    
    class Meta:
        unique_together = (("column_profile", "field"),)
        ordering = ['pk', "column_profile", "field"]


class ProductFile(models.Model):
    file = models.FileField(blank=False, null=False)
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description
    
    class Meta:
        ordering = ['uploaded_at']


class ProductChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="User")
    event_log = models.ForeignKey('EventLog', on_delete=models.SET_NULL, null=True, verbose_name="EventLog")
    sku = models.CharField(max_length=31, db_index=True, verbose_name="SKU")
    prev_data = JSONField(verbose_name="Previous Product Data")
    new_data = JSONField(verbose_name="New Product Data")
    fields = ArrayField(models.CharField(max_length=63), blank=True)


class EventLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="User")
    logged_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=511, verbose_name="Message")
    
    class EventState(models.IntegerChoices):
        STARTED = 0
        COMPLETED = 1
    
    event_state = models.IntegerField(choices=EventState.choices, default=EventState.STARTED)

    def __str__(self):
        if self.user:
            return f'{self.user.username} - {self.logged_at} - {self.message} - {self.event_state}'
        else:
            return f'deleted - {self.logged_at} - {self.message} - {self.event_state}'


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.ColorWidget
        return super().formfield(**kwargs)

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    color_dropdown = ColorField(default='#ffffff', verbose_name="Color for Dropdown")
    color_background = ColorField(default='#ffffff', verbose_name="Color for the Background")
    size_shortcode = models.IntegerField(default=11, verbose_name="Font Size for the ShortCode")
    active_column_profile = models.ForeignKey(ColumnProfile, on_delete=models.SET_NULL, null=True, verbose_name="Active Column Profile")
    
    def __str__(self):
        return self.user.username


class AdminSetting(models.Model):
    import_url = models.CharField(default="https://www.allendale-group.co.uk/shortcode/ShortcodeData.xml", max_length=511, verbose_name="Import Url")
    
    class ExportMethod(models.IntegerChoices):
        FILE = 0
        FTP = 1
    
    export_method = models.IntegerField(choices=ExportMethod.choices, default=ExportMethod.FILE, verbose_name="Export Method")
    export_path = models.CharField(default="", blank=True, max_length=511, verbose_name="Export File Path")
    ftp_export_path = models.CharField(default="", blank=True, max_length=511, verbose_name="FTP Export Path")
    ftp_export_filename = models.CharField(default="", blank=True, max_length=127, verbose_name="FTP Export File Name")
    ftp_host = models.CharField(default="", blank=True, max_length=127, verbose_name="FTP Host")
    ftp_user = models.CharField(default="", blank=True, max_length=63, verbose_name="FTP User")
    ftp_password = models.CharField(default="", blank=True, max_length=63, verbose_name="FTP Password")
    # ftp_port = models.IntegerField(default=22, blank=True, verbose_name="FTP Port")

    def __str__(self):
        return 'admin settings'

