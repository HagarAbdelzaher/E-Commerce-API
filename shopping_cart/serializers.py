from rest_framework import serializers
from .models import Cart, Cart_Item
from user.serializers import SignUpSerializer
from product.models import Product


def edit_product_quantity(product: Product, quantity: int):
    if (product.quantity - quantity < 0):
        if (product.quantity == 0):
            raise serializers.ValidationError(
                {'error': ['product out of stock.']}, 422)
        else:
            raise serializers.ValidationError(
                {'error': [f' Only {product.quantity} items available.']}, 422)
    else:
        product.quantity -= quantity
        product.save()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'id', 'price', 'quantity', 'image']


class ViewCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart_Item
        fields = ['id', 'product', 'quantity', 'cart']


class CartSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(read_only=True)
    cart = ViewCartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart']


class EditCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart_Item
        fields = ['id', 'quantity', "product"]

    def create(self, validated_data):
        print(validated_data['quantity'], type(validated_data['quantity']))
        quantity = validated_data['quantity']
        user = self.context['user']
        product = self.context['product_id']

        try:
            product = Product.objects.get(id=product)
            cart_exist = Cart.objects.filter(user=user).first()

            if (cart_exist):
                try:
                    cart_item = Cart_Item.objects.get(
                        cart=cart_exist, product=int(product.id))
                    edit_product_quantity(product, quantity)
                    cart_item.quantity += quantity

                except Cart_Item.DoesNotExist:
                    edit_product_quantity(product, quantity)
                    cart_item = Cart_Item.objects.create(
                        cart=cart_exist, product=product, quantity=quantity)

            else:
                cart = Cart.objects.create(user=user)
                edit_product_quantity(product, quantity)
                cart_item = Cart_Item.objects.create(
                    cart=cart, product=product, quantity=quantity)

            cart_item.save()
            return cart_item
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {'error': ['product does not exist.']}, 400)

    def update(self, instance, validated_data):
        quantity = validated_data['quantity']
        action = self.context.get('action')
        product = self.context.get('product_id')
        try:
            product = Product.objects.get(id=product)
            if action not in ('add', 'remove' , 'edit'):
                raise serializers.ValidationError(
                    {'error': "Action can only be 'add' or 'remove' or 'edit"}, code=400)

            if action == 'add':
                edit_product_quantity(product, quantity)
                instance.quantity += quantity

            elif action == 'remove' and instance.quantity > 0:
                instance.quantity -= quantity
                product.quantity += quantity
                product.save()

            elif action == 'edit':
                product.quantity += instance.quantity
                edit_product_quantity(product, quantity)
                instance.quantity = quantity
            instance.save()
            
            if instance.quantity == 0:
                instance.delete()

            return instance
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {'error': "Product doesn't exist"}, code=422)
    