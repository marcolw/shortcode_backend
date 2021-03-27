from . import utils

import requests
import xmltodict
import xlsxwriter
import re
import datetime
from ftplib import FTP, FTP_TLS
import shutil
import os
import pysftp

from authentication.models import User
from . import models

import sys, traceback


def sync_user_column_profile(user):
    # todo - multi threading

    # if column profile doesn't exists at all, create Default
    queryset = models.ColumnProfile.objects.filter(user=user)
    if not queryset:
        instance = models.ColumnProfile(user=user, description="Default")
        instance.save()

    # get all fields
    fields = models.Field.objects.all()

    # get column profiles
    for instance in models.ColumnProfile.objects.filter(user=user):
        column_profile_fields = models.ColumnProfileField.objects.filter(
            column_profile=instance)

        # column_profile_field exists while field doesn't exist - impossible
        # for column_profile_field in column_profile_fields:

        # field exists while column_profile_field doesn't exist - create
        for field in fields:
            if not column_profile_fields.filter(field=field):
                models.ColumnProfileField(column_profile=instance, field=field, order=field.pk, visible=(
                    field.field_type != models.Field.FieldType.RESULT)).save()

    # end


def import_from_url(url):
    try:
        print("getting data")
        text = requests.get(url).text
        doc = xmltodict.parse(text)
        print("successfully retrieved XML data")

        # make event log
        event_log = models.EventLog(
            message="import", event_state=models.EventLog.EventState.STARTED)
        event_log.save()
        print("left an event log")

        fields = {"sku"}
        new_data = {}
        items = doc['products']['item']

        # depending on the number of items, 
        # items can be a list (>1) or an OrderedDict (==1)
        if isinstance(items, list):
            for item in items:
                fields.update(item.keys())
                new_data[item['sku']] = item
        else:
            item = items
            fields.update(item.keys())
            new_data[item['sku']] = item

        print("updating fields")
        # fields
        for field in fields:
            try:
                models.Field.objects.get(name=field)
            except:
                label = re.sub("_SC$", " (SC)", field)
                label = re.sub("_x([^x]*)x$", " (\\1)", label)
                label = label.replace("_", " ")

                field_type = models.Field.FieldType.DATA
                if field.endswith("_SC"):
                    field_type = models.Field.FieldType.SHORTCODE
                elif f'{field}_SC' in fields:
                    field_type = models.Field.FieldType.RESULT

                models.Field(name=field, label=label,
                             field_type=field_type).save()
        print("successfully updated fields")

        print("syncing column profiles")
        # sync column profiles
        for user in User.objects.all():
            sync_user_column_profile(user)
        print("successfully synced")

        print("updating products")
        # update products
        products = []
        organized_products = {}
        part_number_organized_products = {}
        for product in models.Product.objects.all():
            if product.data["sku"] in new_data:
                product.data = new_data[product.data["sku"]]
            products.append(product)
            organized_products[product.data["sku"]] = product.data
            part_number_organized_products[product.data["Part_Number"]
                                           ] = product.data

        print("reading new products")
        # new products
        new_products = []
        for sku, product in new_data.items():
            if sku not in organized_products:
                new_products.append(models.Product(sku=sku, data=product))
                organized_products[sku] = product
                part_number_organized_products[product["Part_Number"]] = product

        print("updating product database")
        # update result fields
        for product in products:
            for field in fields:
                shortcode = f'{field}_SC'
                if shortcode in fields and shortcode in product.data:
                    product.data[field] = utils.getRenderedText(
                        product.data[shortcode], product.data, part_number_organized_products)

        models.Product.objects.bulk_update(products, ['data'], batch_size=25)
        print("successfully updated product database")

        print("adding new products to database")
        # set result fields for new products
        for product in new_products:
            for field in fields:
                shortcode = f'{field}_SC'
                if shortcode in fields and shortcode in product.data:
                    product.data[field] = utils.getRenderedText(
                        product.data[shortcode], product.data, part_number_organized_products)

        models.Product.objects.bulk_create(new_products, batch_size=25)
        print("successfully addes new product to database")

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)


def make_diff_excel():
    try:
        print("creating a new Excel (XLSX) file")
        # Create a workbook and add a worksheet.
        filename = f'backups/diff_{str(datetime.datetime.now())}.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        # Start from the header row
        row = 0
        col = 2

        print("writing the header row")
        organized_fields = {"sku": 0, "Part_Number": 1}
        worksheet.write(row, 0, "sku")
        worksheet.write(row, 1, "Part_Number")
        for field in models.Field.objects.all():
            if field.name != "sku" and field.name != "Part_Number":
                organized_fields[field.name] = col
                worksheet.write(row, col, field.name)
                col += 1

        print("writing product data")
        modified_products = models.Product.objects.filter(modified=True)
        for product in modified_products:
            product.modified = False
            row += 1
            for key, value in product.data.items():
                if key in organized_fields:
                    if isinstance(value, str):
                        worksheet.write(row, organized_fields[key], value)
                    else:
                        print("unrecognized field", key, value)

        models.Product.objects.bulk_update(modified_products, ['modified'])
        
        print("closing")
        workbook.close()

        return filename
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        return ''


def make_excel():
    try:
        print("creating a new Excel (XLSX) file")
        # Create a workbook and add a worksheet.
        filename = f'backups/{str(datetime.datetime.now())}.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        # Start from the header row
        row = 0
        col = 2

        print("writing the header row")
        organized_fields = {"sku": 0, "Part_Number": 1}
        worksheet.write(row, 0, "sku")
        worksheet.write(row, 1, "Part_Number")
        for field in models.Field.objects.all():
            if field.name != "sku" and field.name != "Part_Number":
                organized_fields[field.name] = col
                worksheet.write(row, col, field.name)
                col += 1

        print("writing product data")
        all_products = models.Product.objects.all()
        for product in all_products:
            row += 1
            for key, value in product.data.items():
                if key in organized_fields:
                    if isinstance(value, str):
                        worksheet.write(row, organized_fields[key], value)
                    else:
                        print("unrecognized field", key)
        
        print("closing")
        workbook.close()

        return filename
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        return ''


def export_to_file(export_path):
    fn = make_excel()
    print(fn)

    if not fn:
        print("creating file failed")
        return

    try:
        print("copying file")
        shutil.copyfile(fn, export_path)
        print("finished")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        print("failed")


def export_to_sftp(ftp_host, ftp_user, ftp_password, export_path, export_filename):
    make_excel()
    fn = make_diff_excel()
    print(fn)

    if not fn:
        print("creating file failed")
        return

    try:
        print("establising connection")
        
        srv = pysftp.Connection(
            host=ftp_host, username=ftp_user, password=ftp_password)

        remote_path = f'{export_path}/{export_filename}'
        print(remote_path)
        print("writing file")
        # srv.put(os.path.basename(fn), remote_path)  # upload file
        srv.put(fn, remote_path)

        print("closing connection")
        # Closes the connection
        srv.close()

        print("finished")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        print("failed")
		
def export_full_to_sftp(ftp_host, ftp_user, ftp_password, export_path, export_filename):
    make_excel()
    fn = make_excel()
    print(fn)

    if not fn:
        print("creating file failed")
        return

    try:
        print("establising connection")
        
        srv = pysftp.Connection(
            host=ftp_host, username=ftp_user, password=ftp_password)

        remote_path = f'{export_path}/ShortcodeDataFull.xlsx'
        print(remote_path)
        print("writing file")
        # srv.put(os.path.basename(fn), remote_path)  # upload file
        srv.put(fn, remote_path)

        print("closing connection")
        # Closes the connection
        srv.close()

        print("finished")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        print("failed")

def export_to_ftp(ftp_host, ftp_user, ftp_password, export_path):
    fn = make_excel()
    print(fn)

    if not fn:
        print("creating file failed")
        return

    try:
        print("establising connection")

        ftp = FTP_TLS(host=ftp_host, user=ftp_user, passwd=ftp_password)

        # switch to secure data connection
        ftps.prot_p()

        if export_path:
            print("changing working directory")
            ftp.cwd(export_path)

        print("writing file")
        fp = open(fn, 'rb')
        # upload file
        ftp.storbinary('STOR %s' % os.path.basename(fn), fp, 1024)
        fp.close()

        print("closing connection")
        # Closes the connection
        ftp.quit()

        print("finished")
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb)
        traceback.print_tb(exc_tb)
        print("failed")
