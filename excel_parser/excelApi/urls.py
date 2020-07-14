
from django.urls import path, include 
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index" ),
    path('upload_file.html', views.upload_file, name="upload_file" ),
    path('file_upload.html', views.file_upload, name="file_upload" ),
    path('file_list.html', views.file_list, name="file_list" ),
    path('budget.html', views.budget, name="budget" ),

]


# this should be used only on developement mode and not on production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)