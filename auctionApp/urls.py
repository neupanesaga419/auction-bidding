
from django.urls import path
from auctionApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.welcome, name='welcome'),
    path('login/',views.log_user, name='log_in'),
    path('signup/',views.signup, name='signup'),
    path('log_out/',views.log_out, name='log_out'),
    path('bidder/',views.bidder, name='bidder'),
    # path('img/',views.image_path,name='image'),
    # path('show/',views.ImgShow,name='show'),
    path('addProducts/',views.AddProducts,name='addProduct'),
    path('ViewProducts/',views.ViewProducts,name='ViewProducts'),
    path('EditProducts/<int:id>',views.EditProducts,name='EditProducts'),
    path('DeleteProducts/<int:id>',views.DeleteProducts,name='DeleteProducts'),
    path('OnBidProducts/',views.OnBid,name='OnBidProducts'),
    path('BidEntry/<int:id>',views.Bid_Entry,name="BidEntry"),
    path('ViewBiddedProducts/',views.view_timeoutdated_products,name='ViewBiddedProducts'),
    path('ViewWinner/<int:id>',views.Winner,name='ViewWinner'),
    path('ViewProductsGettingBidded/',views.view_products_going_to_bid,name='ViewProductsGettingBidded'),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)