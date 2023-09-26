import os
import shutil
from django.conf import settings

from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, response, pagination


from apps.permissions.permissions import ClassifiedOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Category, Classified, ClassifiedImage
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ImageView(generics.ListCreateAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.filter(
        is_active=True).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    http_method_names = ['get', ]


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.filter(is_active=True)
    serializer_class = ClassifiedSerializer
    permission_classes = (ClassifiedOwnerOrReadOnly, )


class ClassifiedCreateView(generics.CreateAPIView):
    serializer_class = ClassifiedSerializer
    permission_classes = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        classified = serializer.save()

        for image_data in serializer.validated_data.get('images', []):
            image = self.handle_image(image_data, classified)
            image.save()

        return classified

    def handle_image(self, image_data, classified):

        if not image_data.get('imageUrl'):
            raise ValidationError('Image URL required')

        image_path = image_data['imageUrl']

        if not os.path.exists(image_path):
            raise ValidationError('Image not found')

        image_name = os.path.basename(image_path)

        shutil.copy(
            image_path,
            os.path.join(settings.MEDIA_ROOT, 'classifieds', image_name)
        )

        return ClassifiedImage(
            classified=classified,
            image=f'classifieds/{image_name}'
        )
