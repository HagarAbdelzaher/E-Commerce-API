from django.contrib import admin
from wishlist.models  import Wishlist, Wishlist_Item

# Register your models here.
admin.site.register(Wishlist)
admin.site.register(Wishlist_Item)