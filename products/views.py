from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer, ProductValidateSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_update_destroy_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.text = serializer.validated_data.get('text')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect products (QuerySet)
        products = (Product.objects.select_related('category')
                    .prefetch_related('tags', 'reviews').all())

        # step 2: Reformat(Serialize) QuerySet to list of Dictionaries (QueryDict)
        data = ProductSerializer(instance=products, many=True).data

        # step 3: Return response as JSON
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 0: Validation of data (Existing, Typing, Extra, Custom)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data from Serialized Data
        title = serializer.validated_data.get('title')  # None
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')  # "Y"
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')  # [1,2,3]

        # step 2: Create product by received data
        product = Product.objects.create(
            title=title,
            text=text,
            price=price,
            is_active=is_active,
            category_id=category_id
        )
        product.tags.set(tags)
        product.save()

        # step 3: Return Response (status, data)
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'str': 'Hello world',
        'int': 100,
        'float': 2.77,
        'bool': True,
        'list': [1, 2],
        'dict': {"key": "value"}
    }
    return Response(data=[dict_])