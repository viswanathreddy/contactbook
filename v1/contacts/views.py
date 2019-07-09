from django.db.models import Q
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contact
from .serializers.contact import ContactSerializer

from .utils import StandardResultsSetPagination


# Create your views here.

#
# returns paginated response
class ContactListViewAPI(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        qs = Contact.objects.filter(created_by=user.pk)
        name_search = self.request.query_params.get('name', None)
        email_search = self.request.query_params.get('email', None)

        if name_search and email_search:
            qs = qs.filter(
                Q(name__icontains=name_search) &
                Q(email__contains=email_search)
            )
        elif name_search:
            qs = qs.filter(
                Q(name__icontains=name_search))
        elif email_search:
            qs = qs.filter(Q(email__contains=email_search))
        return qs


class ContactView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return Contact.objects.get(pk=pk)

    # create contact
    def post(self, request):
        user = request.user
        print('req ', request, request.data)
        data = request.data
        data['created_by'] = user.pk
        serializer = ContactSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            contact_saved = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError(serializer.errors)

    def get(self, request):
        user = request.user
        data = Contact.objects.filter(created_by=user)
        serializer = ContactSerializer(data, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        contact_model_object = self.get_object(pk)
        if contact_model_object.created_by.pk != request.user.pk:
            raise PermissionDenied()
        request_data = request.data
        request_data['created_by'] = request.user.pk
        serializer = ContactSerializer(contact_model_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            contact_updated = serializer.save()
            print("updated contact", contact_updated, contact_updated.name)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError(serializer.errors)

    def delete(self, request, pk):
        contact_model_object = self.get_object(pk)
        if contact_model_object.created_by.pk != request.user.pk:
            raise PermissionDenied()
        contact_model_object.delete()
        return Response(status=status.HTTP_200_OK)
