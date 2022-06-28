from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from manageProduct.models.galleryImage import GalleryImage
from manageProduct.models.defineProduct import DefineProduct

from manageProduct.serializers.product.gImage import ProdGalImageSz


class ProdGalImageList(GenericAPIView):

    def get(self, request, prod_id):

        prod = get_object_or_404(DefineProduct, id=prod_id)
        imgs = GalleryImage.objects.filter(product=prod)
        sz = ProdGalImageSz(imgs, many=True)

        return Response({'status': 'get images of a product',
                         'images': sz.data})
