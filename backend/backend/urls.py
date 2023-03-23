from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

api = [
    path('', include('users.urls', namespace='users')),
    path('', include('foodgram.urls', namespace='foodgram')),
]

urlpatterns = [
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]
