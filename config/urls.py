from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [

    # Core
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Django REST Boilerplate')),

    url(r'^accounts/', include('allauth.urls')),

    # API (v1)
    url(r'^', include('v1.accounts.urls')),
    url(r'^v1/contacts', include('v1.contacts.urls')),

    url(r'^swagger$', schema_view),

    # rest auth
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
