from rest_framework import serializers
from .models import Product, Category, Tag, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    tag_names = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id reviews category category_name tags tag_names title price created'.split()
        # depth = 1

    def get_tag_names(self, product):
        return [i.name for i in product.tags.all()]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=100)
    text = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=1, max_value=1000000)
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist!')
        return category_id

    def validate_tags(self, tags):  # [1,2,99]
        existing_tags = Tag.objects.filter(id__in=tags)  # [1,2]
        if len(existing_tags) != len(tags):
            raise ValidationError('Tag does not exist!')
        return tags