
from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.auth.models import Group
admin.site.unregister(Group)
from .models import *
# from django.contrib.sessions import django_session
# import adminlte3
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","email","first_name","last_name","is_superuser","is_verified","is_active")
    fields = ("first_name","last_name","email","password","mobile","is_superuser","is_verified","is_active")
    
@admin.register(BiddingTime)
class BiddingTimeAdmin(admin.ModelAdmin):
    list_display=("id","bid_day","bid_start_time","bid_end_time","added_date")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","category_name","category_details","added_date")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ("id","Product_Created_By","Category_of_product","Product_Bidding_Time","min_bid_amount","product_name","product_description","product_image_name","added_date")
    # list_filter = ("creator","category","product_bid_time")
    search_fields = ['creator']
    def Category_of_product(self,obj):
        from .models import Category
        myCat = Category.objects.all().filter(id=obj.category)
        for item in myCat:
            category_name =item
        return category_name
    def Product_Created_By(self,obj):
        from .models import User
        myUser = User.objects.all().filter(id=obj.creator) 
        for item in myUser:
            user_name = item
        return user_name
    def Product_Bidding_Time(self,obj):
        from .models import BiddingTime
        myTime = BiddingTime.objects.all().filter(id=obj.product_bid_time)
        for item in myTime:
            product_bid_time = item
        return product_bid_time
    
  
  
        
@admin.register(BiddingAmount)
class BiddingAmountAdmin(admin.ModelAdmin):
    def has_add_permission(self,request):
        return False
    list_display = ("id","Product_Bidded_By","Product_Bidded_On","bid_amount")
    list_filter = ("bidder_name","product_name")
    
    def Product_Bidded_By(self,obj):
        from .models import User
        myUser = User.objects.all().filter(id=obj.bidder_name) 
        for item in myUser:
            user_name = item
        return user_name
    def Product_Bidded_On(self,obj):
        from .models import Product
        myProduct = Product.objects.all().filter(id=obj.product_name)
        for item in myProduct:
            name_of_product = item
        return name_of_product
        
# admin.site.register(User)
# admin.site.register(Image)
# admin.site.register(BiddingTime)
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(BiddingAmount)


admin.site.site_header = "Auction Bidding"
# admin.site.unregister(Group)
# @admin.register(django_session)