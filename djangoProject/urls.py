from django.contrib import admin
from django.urls import path,include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls')), # 加入app对应urls
    path('swagger-docs/', schema_view),
]
