from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import requests

from shortcode.operations import export_to_file, export_to_sftp, export_full_to_sftp
from shortcode.models import AdminSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        setting = AdminSetting.objects.first()
        if setting.export_method == AdminSetting.ExportMethod.FILE:
            export_to_file(setting.export_path)
        elif setting.export_method == AdminSetting.ExportMethod.FTP:
            export_to_sftp(setting.ftp_host, setting.ftp_user, setting.ftp_password, setting.ftp_export_path, setting.ftp_export_filename)
            export_full_to_sftp(setting.ftp_host, setting.ftp_user, setting.ftp_password, setting.ftp_export_path, setting.ftp_export_filename)
