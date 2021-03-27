from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from .helpers import BulkCreateManager
from shortcode.tasks import backup_products
from authentication.models import User
from .operations import sync_user_column_profile

import sys


class FieldViewSet(viewsets.ModelViewSet):
    queryset = models.Field.objects.all()
    serializer_class = serializers.FieldSerializer

class FieldView(APIView):
    def post(self, request):
        field_serializer = serializers.FieldSerializer(data=request.data, many=True)
        if field_serializer.is_valid():
            field_serializer.save()
            queryset = models.Field.objects.all()
            fields = serializers.FieldSerializer(queryset, many=True)
            return Response(fields.data)
        else:
            return Response(field_serializer.errors)


class ColumnProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ColumnProfileSerializer

    def get_queryset(self):
        return models.ColumnProfile.objects.filter(user=self.request.user)


class ColumnProfileFieldDetailView(APIView):
    def get(self, request):
        queryset = models.ColumnProfileField.objects.filter(column_profile_id=self.request.GET['column_profile'])
        column_profile_fields_detail = serializers.ColumnProfileFieldDetailSerializer(queryset, many=True)
        return Response(column_profile_fields_detail.data)

class ColumnProfileFieldViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ColumnProfileFieldSerializer

    def get_queryset(self):
        return models.ColumnProfileField.objects.filter(column_profile_id=self.request.GET['column_profile'])

class ColumnProfileFieldView(APIView):
    def post(self, request):
        column_profile_field_serializer = serializers.ColumnProfileFieldSerializer(data=request.data, many=True)
        if column_profile_field_serializer.is_valid():
            column_profile_field_serializer.save()
            queryset = models.ColumnProfileField.objects.filter(column_profile_id=request.GET['column_profile'])
            column_profile_fields = serializers.ColumnProfileFieldSerializer(queryset, many=True)
            return Response(column_profile_fields.data)
        else:
            return Response(column_profile_field_serializer.errors)
    
    def put(self, request):
        cpfs = []
        for item in request.data:
            column_profile_field = models.ColumnProfileField.objects.get(pk=item['id'])
            column_profile_field.order = item.get('order', column_profile_field.order)
            column_profile_field.visible = item.get('visible', column_profile_field.visible)

            cpfs.append(column_profile_field)
        models.ColumnProfileField.objects.bulk_update(cpfs, ['order', 'visible'], batch_size=25)

        queryset = models.ColumnProfileField.objects.filter(column_profile_id=request.GET['column_profile'])
        column_profile_fields = serializers.ColumnProfileFieldSerializer(queryset, many=True)
        return Response(column_profile_fields.data)
    
class SyncColumnProfileFieldView(APIView):
    def get(self, request):
        sync_user_column_profile(self.request.user)

        return Response({
            "result": "success"
        })


class ProductView(APIView):
    def post(self, request):
        bulk_mgr = BulkCreateManager(chunk_size=50)
        shouldLog = (request.GET['log'] == "1")

        for item in request.data:
            try:
                product = models.Product.objects.get(sku=item['sku'])
                
                if shouldLog:
                    try:
                        bulk_mgr.add(
                            models.ProductChangeLog(
                                user=request.user, 
                                sku=item['sku'], fields=item['fields'], 
                                prev_data=product.data, new_data=item.get('data', product.data)
                            )
                        )
                    except:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print (exc_type, exc_obj, exc_tb)

                product.data = item.get('data', product.data)
                product.save()
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print (exc_type, exc_obj, exc_tb)
                bulk_mgr.add(models.Product(sku=item['sku'], data=item['data']))

        bulk_mgr.done()
        
        """
        if not shouldLog:
            # backup_products.delay()
            backup_product_data()
        """
        
        queryset = models.Product.objects.all()
        products = serializers.ProductSerializer(queryset, many=True)
        return Response(products.data)

def backup_product_data():
    products = []
    for product in models.Product.objects.all():
        product.backup_data = product.data
        products.append(product)
    models.Product.objects.bulk_update(products, ['backup_data'], batch_size=100)

class ProductUpdateView(APIView):
    def post(self, request):
        bulk_mgr = BulkCreateManager(chunk_size=50)
        event_log = models.EventLog.objects.get(pk=int(request.GET['event_log']))

        for item in request.data:
            try:
                product = models.Product.objects.get(sku=item['sku'])
                
                bulk_mgr.add(
                    models.ProductChangeLog(
                        user=request.user, 
                        event_log=event_log,
                        sku=item['sku'], 
                        fields=item['fields'], 
                        prev_data=product.data, 
                        new_data=item.get('data', product.data)
                    )
                )

                product.data = item.get('data', product.data)
                product.modified = True
                product.save()
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print (exc_type, exc_obj, exc_tb)

        bulk_mgr.done()
        
        event_log.event_state = models.EventLog.EventState.COMPLETED
        event_log.save()
        
        return Response({
            "status": "success"
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

class ProductBackupViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductBackupSerializer


class EventLogViewSet(viewsets.ModelViewSet):
    queryset = models.EventLog.objects.all()
    serializer_class = serializers.EventLogSerializer

class EventLogView(APIView):
    def get(self, request):
        user = User.objects.get(pk=int(request.GET['user']))
        queryset = models.EventLog.objects.filter(user=user)
        event_logs = serializers.EventLogSerializer(queryset, many=True)
        return Response(event_logs.data)


class UserSettingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSettingSerializer

    def get_queryset(self):
        return models.UserSetting.objects.filter(user=self.request.user)


class ProfileView(APIView):
    def get(self, request):
        return Response({
            "is_staff": self.request.user.is_staff,
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "email": self.request.user.email,
        })


class ProductChangeLogView(APIView):
    def get(self, request):
        queryset = models.ProductChangeLog.objects.filter(user_id=self.request.GET['user'], 
                                                            event_log_id=self.request.GET['event_log'])
        product_change_logs = serializers.ProductChangeLogSerializer(queryset, many=True)
        return Response(product_change_logs.data)


class ShortCodeChangeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShortCodeChangeSerializer

    def get_queryset(self):
        return models.ShortCodeChange.objects.filter(user=self.request.user)

class ShortCodeChangeView(APIView):
    def delete(self, request):
        try:
            models.ShortCodeChange.objects.filter(user=self.request.user).delete()
            return Response({
                "status": "success"
            })
        except:
            return Response({
                "status": "failure"
            })

    def post(self, request):
        bulk_mgr = BulkCreateManager(chunk_size=50)
        changes = []

        # part_number hardcoded
        for item in request.data:
            try:
                change = models.ShortCodeChange.objects.get(part_number=item['part_number'], user=request.user)
                change.data = item.get('data', change.data)

                changes.append(change)
            except:
                bulk_mgr.add(
                    models.ShortCodeChange(
                        user=request.user, 
                        part_number=item['part_number'],
                        data=item['data']
                    )
                )

        bulk_mgr.done()
        models.ShortCodeChange.objects.bulk_update(changes, ['data'], batch_size=25)

        return Response({
            "status": "success"
        })
