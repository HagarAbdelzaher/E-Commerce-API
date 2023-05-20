from rest_framework import serializers
from .models import Wishlist, Wishlist_Item
from user.serializers import SignUpSerializer
from product.serializers import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'id', 'price', 'quantity', 'image']


class ViewWishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist_Item
        fields = ['id', 'product', 'wish_list']


class WishListSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(read_only=True)
    fav_items = ViewWishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['user', 'fav_items']


class EditWishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist_Item
        fields = ['id', "product"]

    def create(self, validated_data):
        user = self.context['user']
        product = self.context['product_id']

        try:
            product = Product.objects.get(id=product)
            wishlist_exist = Wishlist.objects.filter(user=user).first()

            if (wishlist_exist):
                try:
                    wishlist_item = Wishlist_Item.objects.get(
                        wish_list=wishlist_exist, product=int(product.id))

                except Wishlist_Item.DoesNotExist:
                    wishlist_item = Wishlist_Item.objects.create(
                        wish_list=wishlist_exist, product=product)

            else:
                wishlist = Wishlist.objects.create(user=user)
                wishlist_item = Wishlist_Item.objects.create(
                    wish_list=wishlist, product=product)

            wishlist_item.save()
            return wishlist_item
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {'error': ['product does not exist.']}, 400)
