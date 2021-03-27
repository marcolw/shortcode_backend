from rest_framework import serializers
from . import models

class ProductFileSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.ProductFile
		fields = ('file', 'description', 'uploaded_at')


class ProductBackupSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.Product
		fields = ('sku', 'data', 'backup_data')

class ProductListSerializer(serializers.ListSerializer):
	class Meta():
		model = models.Product
		fields = ('sku', 'data')

class ProductSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.Product
		fields = ('sku', 'data')
		list_serializer_class = ProductListSerializer


class FieldListSerializer(serializers.ListSerializer):
	class Meta():
		model = models.Field
		fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.Field
		fields = '__all__'
		list_serializer_class = FieldListSerializer


class ColumnProfileSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.ColumnProfile
		fields = '__all__'


class ColumnProfileFieldListSerializer(serializers.ListSerializer):
	class Meta():
		model = models.ColumnProfileField
		fields = '__all__'

class ColumnProfileFieldSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.ColumnProfileField
		fields = '__all__'
		list_serializer_class = ColumnProfileFieldListSerializer

class ColumnProfileFieldDetailSerializer(serializers.ModelSerializer):
	# working - ideal solution
	field_label = serializers.ReadOnlyField(source='field.label')
	field_name = serializers.ReadOnlyField(source='field.name')

	# not working - NotImplementedError: RelatedField.to_representation() must be implemented for field field_label.
	# field_label = serializers.StringRelatedField(source='field', read_only=True)
	
	# working - implicitly by Field.__str__()
	# field_label = serializers.StringRelatedField(source='field', read_only=True)

	class Meta():
		model = models.ColumnProfileField
		fields = ('id', 'column_profile', 'field', 'field_label', 'field_name', 'order', 'visible')


class ProductChangeLogSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.ProductChangeLog
		fields = '__all__'


class EventLogSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.EventLog
		fields = '__all__'


class UserSettingSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.UserSetting
		fields = '__all__'

class ShortCodeChangeSerializer(serializers.ModelSerializer):
	class Meta():
		model = models.ShortCodeChange
		fields = '__all__'

