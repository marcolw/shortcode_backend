from __future__ import absolute_import, unicode_literals

from celery import shared_task

from . import models


@shared_task
def backup_products():
    products = []
    for product in models.Product.objects.all():
        product.backup_data = product.data
        products.append(product)
    models.Product.objects.bulk_update(products, ['backup_data'], batch_size=100)
    print (len(products))
