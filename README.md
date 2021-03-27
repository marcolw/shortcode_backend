# Django Back-End for ShortCode Processor

Project: shcp

Apps:

* authentication

  Uses djangorestframework-simplejwt.

* shortcode

  Main

* front

  For integration with the Angular site.



#### shortcode

* Models

  1. Product

  2. ProductBackup

  3. Field

  4. ColumnProfile

  5. ColumnProfileField

  6. ProductChangeLog

  7. ProductFile

     

* Serializers

  1. ProductSerializer, ProductListSerializer

  2. ProductBackupSerializer

  3. FieldSerializer, FieldListSerializer

  4. ColumnProfileSerializer

  5. ColumnProfileFieldSerializer, ColumnProfileFieldListSerializer, ColumnProfileFieldDetailSerializer

  6. ProductChangeLogSerializer

     

* Views

  1. UploadFileView - ProductFileSerializer

     

* APIs

  1. ProductViewSet - ProductSerializer

     /products/

     

     ProductView: POST

     /products-bulk/?log=0 - products update, make backup here (calls celery task - backup_products())

     /products-bulk/?log=1 - product shortcodes update, make log of changed fields
  
     
  
  2. ProductBackupViewSet - ProductBackupSerializer
  
     /products-backup/
  
     
  
  3. FieldViewSet - FieldSerializer
  
     /fields/
  
     
  
     FieldView: POST
  
     /fields-bulk/ - fields bulk insert
  
     
  
  4. ColumnProfileViewSet - ColumnProfileSerializer
  
     /column-profiles/ - column profiles of the current user (get_queryset - user=self.request.user)
  
     
  
  5. ColumnProfileFieldViewSet - ColumnProfileFieldSerializer
  
     /column-profile-fields/
  
     
  
     ColumnProfileFieldView: POST, PUT
  
     /column-profile-fields-bulk/?column_profile=n - column profile fields bulk insert, update
  
     
  
     ColumnProfileFieldDetailView: GET
  
     /column-profile-fields-detail/?column_profile=n - column profile fields get details (field name, field label)
  
     
  
  6. SyncColumnProfileView: GET
  
     /sync/column-profile-fields/ - if column profile has missing fields, fill them
  
     Default value of column profile field is (order=field.pk, visible=field.field_type is SHORTCODE or DATA?)



#### Auto import and export

* Import

  1. read from url, and convert XML string to python dict

  2. Make event log

  3. Add new fields

  4. Sync column profile fields

  5. Update shortcodes

  6. Update results

  7. Update database

     

* Export

  1. Read from database

  2. Make Excel (XLSX) file

  3. FTP or local file

     

### How to make a new API

1. Create a model
2. Create a serializer
3. Add to admin
4. Create a view set
5. Configure url

