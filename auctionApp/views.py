from django.shortcuts import render,HttpResponse,redirect

from .forms import UserForm,ProductsForm

from .models import *
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from datetime import date,datetime
from AuctionSite import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import generate_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str

date_today = date.today()
date_for_site = datetime.now().year


#++++++++++++========================= User SignUP Starts From Here ++++++++++++++==============================================--\\
def signup(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('cpass')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        # userType= request.POST.get('usertype')
        
        if User.objects.filter(email=email):
            messages.warning(request,"Username Already Taken")
            return redirect('signup')
        elif password == confirm_pass:
            user = User.objects.create_user(email=email,password=confirm_pass,first_name=fname,last_name=lname)
            user.is_active=False
            user.save()
            messages.success(request,"We have sent you the confirmation email in your email account please verify to login")
            
            # Sending Mail To User
            # Welcome Mail
            subject = "Welcome to Auction Bidding System!!"
            message = "Hello "+ user.first_name + "!!!\n " + "Welcome to Auction Bidding Site\n\n" + "Thank you for visting our site \n "+"We have sent you a confirmation email.\n"+"Please verify it in order to activate your account!!\n\n"+"Thanking you!!! Auction bidding team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            # End of Welcome Mail
            if send_mail(subject,message,from_email,to_list,fail_silently=True):
                print("Yes Mail is sent")
            else:
                print("Not Working")
            # Start of Email Confirmation 
            current_site = get_current_site(request)
            email_subject = "Confirmation Email From Auction Bidding!!"
            confirm_message = render_to_string("email_confirmation.html",{
                'name':user.first_name,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
            })
            email = EmailMessage(
                email_subject,
                confirm_message,
                from_email,
                to_list,
            )
            email.fail_silently = True
            email.send()
            
            return redirect('log_in')
        else:
            messages.warning(request,"Password Doesnot Match")
            return redirect('signup')
        # if form.is_valid():
        #     form.save()
        #     return HttpResponse("Data submitted Successfully")
        # else:
        #     # redirect back to the user page with errors
        #     return render(request, 'form.html', {'form':form})
    else:
        # in case of GET request
        form = UserForm(None)
        return render(request, 'signup.html', {'form':form})

# ===================================== User signupp Ends Here +++++++===================================== 
    
# ===============================  Activating The Account =================>>>>>>><<<<<<<<<<<<<<<<<<<<<
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesnotExists):
        user=None 
    
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True 
        user.save()
        login(request,user)
        return redirect("welcome")
    else:
        return render(request,"activation_failed.html")
    
      
# =========================  === For Login of the user Start from Here ===================*********************** 

  
def log_user(request):
    
    if request.method =="POST":
        email = request.POST.get("email")
        password = request.POST.get('pass_word')
        user = authenticate(email=email,password = password)
        if user is not None:
            login(request,user)
            Entries = User.objects.all().filter(email=email)
            for e in Entries:
                if e.user_type == 1:
                    return redirect("welcome")
                else:
                    return redirect('bidder')
                    
            
            # return redirect('welcome')
        else:
            messages.info(request,"Username and Password Didnot match")
            return redirect('log_in')
    
    return render(request,'login.html')

# ++=============================== Login Ends Here +++++++=========================***********************>


#================================= Main Page Rendering After login ===========================
@login_required(login_url='log_in')
def welcome(request):
    Context = {"datetime":date_for_site}
    return render(request,"auctioner.html",Context)

#============================= End Main Page Rendering ========= =============  ===== ==    ==================




@login_required(login_url='log_in')
def bidder(request):
    return render(request,"bidder.html")


#  ============================ Logout Function Help user to log out and it destroy the sessions ==============================
def log_out(request):
    logout(request)
    return redirect('log_in')

#  ========================= End of logout Function =================================

import pytz
from datetime import datetime
import time

# def image_path(request):
#     # form = ProductsForm(request.POST)
#     if request.method == "POST":
#         form = ProductsForm(request.POST,request.FILES)
#         if form.is_valid():
            
#             # Product.save()
#             return HttpResponse('/thank you')
        
#         # image1 = request.FILES["image"]
#         # print(image1)
#         # # e = datetime.now(pytz.timezone('Asia/kathmandu'))
#         # # print(e.date,e.hour,e.minute,e.second,e.milisecond)
#         # # Taking the miliseconds to append it with the image name
#         # e = int(round(time.time() * 1000))
#         # print(e)
#         # # Exploding or dividing the image name for checking extensions
#         # file_extension = os.path.splitext(image1.name)[-1]
#         # nameImg = os.path.splitext(image1.name)[0]
#         # print(nameImg)
#         # extensions = ['.jpeg','.gif','.jpg','.png','.svg','.webp']
#         # if any(file_extension in s  for s in extensions):
#         #     print('saving..........')
#         #     name = nameImg + str(e) + file_extension
#         #     upload_img = Image(image_name=name,image_path=image1)
#         #     upload_img.save()
#         #     print('done....')
#             redirect("show")    
#     else:
#         form = ProductsForm()     
#     return render(request, "imageForm.html",{'form':form})

# def ImgShow(request):
#     Entries = Image.objects.filter(User=2)
#     context = {'getImage':Entries}
#     return render(request,'show.html',context)



# =================================== Start of Add Products Function which helps user to add their Products============================

@login_required(login_url='log_in')
def AddProducts(request):
    if request.method=='POST':
        image = request.FILES["product_image_path"]
        e = int(round(time.time() * 1000))
        file_extension = os.path.splitext(image.name)[-1]
        file_extenson = file_extension.lower()
        nameImg = os.path.splitext(image.name)[0]
        extensions = ['.jpeg','.gif','.jpg','.png','.svg','.webp','.JPG']
        
        if any(file_extension in s  for s in extensions):
            name = nameImg + str(e) + file_extension
            creator = int(request.POST.get('creator'))
            category = int(request.POST.get('category'))
                    # print(type(category))
                    # CatEntry = Category.objects.all().filter(id = category)
                    # print(CatEntry)
                    # print(creator)
            # Entries = User.objects.get(id=creator)
            # print(Entries)
            # for entry in Entries:
            #     print(entry)
            
                    # return HttpResponse(Entries)
                    # category = request.POST.get('category')
            product_name = request.POST.get('product_name')
            product_description = request.POST.get('product_description')
            min_bid_amount = request.POST.get('min_bid_amount')
            product_bid_time = int(request.POST.get('product_bid_time'))
            min_bid_amount = float(min_bid_amount)
            if isinstance(min_bid_amount,float) or isinstance(min_bid_amount,int):
                addProduct = Product(creator=creator,product_description=product_description,category=category,product_bid_time=product_bid_time,min_bid_amount=min_bid_amount,product_name=product_name,product_image_name=name,product_image_path=image)
                addProduct.save()
                print('added....')
                messages.success(request,"Product Added Successfully")
                return redirect('/')
            else:
               return HttpResponse("Enter Bidding amount in numbers")
        else:
            return HttpResponse("your image got wrong extensions Please Enter Image File. The extensions must be jpeg, gif,svg,png,webpm,jpg")
    
    Entries = Category.objects.all()
    Entries2 = BiddingTime.objects.filter(bid_day__gte=date_today)
    
    Context = {'categoryItem':Entries,
               'timeBidItem':Entries2,
               'datetime':date_for_site}
    
    return render(request,'AddProducts.html',Context)

# =====================================    End of Add Products Function ========================================


#  ============================== Start of view products function which helps user to view their entered prodcuts================
@login_required(login_url='log_in')
def ViewProducts(request):
    
    user = request.user
    Entries = Product.objects.all().filter(creator = user.id)
    
    
    TimeEntry = BiddingTime.objects.all()
    # print(list(TimeEntry))
    date_today = date.today()
    
    
    Context = {'myEntry':Entries,'timeEntry':TimeEntry,'dateToday':date_today,'datetime':date_for_site}
    

    return render(request,'viewProducts.html',Context)
#  ================================== End of view Products Fuction ==========================



#  +========================== Start of the Edit Products Function  Which helps user to edit their Products if they want ================
@login_required(login_url='log_in')
def EditProducts(request,id):
    GetEntries = Product.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(GetEntries.product_image_path) > 0:
                os.remove(GetEntries.product_image_path.path)
            image = request.FILES['product_image_path']
            e = int(round(time.time() * 1000))
            file_extension = os.path.splitext(image.name)[-1]
            file_extenson = file_extension.lower()
            nameImg = os.path.splitext(image.name)[0]
            extensions = ['.jpeg','.gif','.jpg','.png','.svg','.webp','.JPG']
            if any(file_extension in s  for s in extensions):
                name = nameImg + str(e) + file_extension
                GetEntries.product_image_path = image
                GetEntries.creator = int(request.POST.get('creator'))
                GetEntries.category = int(request.POST.get('category'))
                GetEntries.product_name = request.POST.get('product_name')
                GetEntries.product_description = request.POST.get('product_description')
                GetEntries.product_image_name = name
                GetEntries.min_bid_amount = request.POST.get('min_bid_amount')
                GetEntries.product_bid_time = int(request.POST.get('product_bid_time'))
                GetEntries.save()
                messages.success(request, "Product Updated Successfully")
                return redirect("/")
    
    
    Entries = Category.objects.all()
    Entries2 = BiddingTime.objects.all().filter(bid_day__gte=date_today)
    Context = {'dataItem':GetEntries,'categoryItem':Entries,
               'timeBidItem':Entries2,'datetime':date_for_site}
    return render(request,'EditProducts.html',Context)

# ===============  End of Edit Product Function ============================

#  ============================== Start of Delete Product Function This function helps user to delete their Products ==============================
@login_required(login_url='log_in')
def DeleteProducts(request,id):
    product = Product.objects.get(id=id)
    if len(product.product_image_path) > 0:
        os.remove(product.product_image_path.path)
        product.delete()
        messages.success(request,"Product Deleted Successfully")
        return redirect("/")
# =========================================End of Delete Prodcuts Function ==============================================



# from json import dumps

#  ============ Start of the function that helps user to see the products on Bidding =============================
from django.db.models import Q

@login_required(login_url='log_in')
def OnBid(request):
    from datetime import datetime,timedelta
    now = datetime.now()
    user = request.user
    product = Product.objects.all().filter(~Q(creator=user.id))
    date_today = date.today()
    
    # print(date_today)
    Time_Bound = BiddingTime.objects.all().filter(bid_day=date_today)
    timeId = []
    for item in Time_Bound:
        # print(item.bid_start_time)
        if item.bid_start_time < now.time() and item.bid_end_time > now.time():
            timeId.append(item.id)
            print(timeId)
    Time_Bound = BiddingTime.objects.all().filter(id__in=timeId)
    # print(Time_Boupnd)
    # dataJSON = dumps(Time_Bound)
    Context = {'product':product,"bidDay":Time_Bound,'datetime':date_for_site}
    return render(request,"ProductsOnBid.html",Context)

#  =============================== End of the Function which helps to see products on bid =========================


# ====================== *************  Start of Bubble sort algorithm  ==**************========================

# My Bubble Sort Implementation to sort the Price of the Bidded Products
def bubbleSort(arr):
    n=len(arr)
    for i in range(n):
        swapped = False
        for j in range(0,n-i-1):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                swapped=True   
        if swapped ==False:
            break

# ==================* ***** ** ** * ** *  End of bubble sort algorithm *************==========================



#  ============== Start of Bidding the item  buy the user           ===================**********************
@login_required(login_url='log_in')
def Bid_Entry(request,id):
    # bidEdit = BiddingAmount.objects.get(product_name=id)
    product = Product.objects.all().filter(id=id)
    for item in product:
        time_id = item.product_bid_time
    time_id = BiddingTime.objects.all().filter(id=time_id)
    from datetime import datetime
    now = datetime.now().time()
    for item in time_id:
        bid_end_time = item.bid_end_time
    
    if now > bid_end_time:
        return redirect("/")
    else:
        user= request.user
        
        bid_amt_present = BiddingAmount.objects.all().filter(bidder_name=user.id,product_name=id)
        if len(bid_amt_present)==0:
            products = Product.objects.all().filter(id=id)
            Context = {'product':products}
            bidAmt = BiddingAmount.objects.all().filter(product_name=id)
            if len(bidAmt) > 0:
                bidAmtList = []
                
                for item in bidAmt:
                    bidAmtList.append(item.bid_amount)
                # Calling Sorting Algo To Sort The Price
                bubbleSort(bidAmtList)
                Max_Amount = max(bidAmtList)
                Context['Max_Amount'] = Max_Amount
                print(Max_Amount)
            
            if request.method == "POST":
                bid_amount = request.POST.get("bid_amount")
                addintoDatabase = BiddingAmount(bidder_name=user.id,product_name=id,bid_amount=bid_amount)
                addintoDatabase.save()
                return redirect("OnBidProducts")
            return render(request,'BidForm.html',Context) 
        else:
            product_amt = BiddingAmount.objects.get(product_name=id,bidder_name=user.id)
            product_all_amt = BiddingAmount.objects.all().filter(product_name=id)
            products_detail = Product.objects.all().filter(id=id)
            Context = {'BidAmount':product_amt,'product':products_detail}
            if len(product_all_amt) > 0:
                bidAmtList = []
                
                for item in product_all_amt:
                    bidAmtList.append(item.bid_amount)
                # Calling Sorting Algo To Sort The Price
                bubbleSort(bidAmtList)
                n = len(bidAmtList)
                Max_Amount = bidAmtList[n-1]
                Context['Max_Amount'] = Max_Amount
                # print(Max_Amount)
                
            if request.method =="POST":
                product_amt.bidder_name = user.id  
                product_amt.product_name = id
                product_amt.bid_amount = request.POST.get("bid_amount")
                product_amt.save()
                messages.success(request,"Bid Amount Updated Successfully")
                return redirect("/")
            Context['datetime'] = date_for_site
            return render(request,"BidEdit.html",Context)



# +++++================================== End of Bid Entry By User on Bidding Item ================================****************

# ======================View Of the item where the user has placed the bid  ==========
@login_required(login_url='log_in')   
def view_timeoutdated_products(request):
    date_today = date.today()
    print(date_today)
    time = BiddingTime.objects.all().filter(bid_day__lt=date_today)
    
    # Just for test
    timeId = []
    from datetime import datetime,timedelta
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print(current_time)
    # time1 = BiddingTime.objects.all()
    # print(time)
    # For all the time items having day less than today
    for item in time:
        timeId.append(item.id)
        # print(timeId)
    
    time2 = BiddingTime.objects.all().filter(bid_day=date_today)
    for item in time2:
        bid_start_day = item.bid_day
        bid_start_time = item.bid_start_time
        combined = datetime.combine(bid_start_day,bid_start_time)
        time_after_30_min = combined + timedelta(minutes=30)
        # if bid_start_time < now.time() and item.bid_end_time > now.time():
        if item.bid_end_time < now.time():
            timeId.append(item.id)
            # print(timeId)
        # print(time_after_30_min)
    # print(datetime.now())
    # end_time = now + timedelta(minutes=30)
    # end_time = end_time.strftime("%H:%M:%S")
    # print(end_time)
    
    # time2 = BiddingTime.objects.all().filter(bid_start_time__gte=current_time,bid_end_time__lte=end_time)
    # print(time2)
    # for item in time2:
    #     # print(item.bid_start_time)
    #     # print("heloo World")
    #     pass
    # TESt TEST TEST
    
    
    # timeId = []
    
    # print(timeId)
    Bidded_Products = BiddingAmount.objects.all()
    biddedItemId = []
    for item in Bidded_Products:
        if item.product_name not in biddedItemId:
            biddedItemId.append(item.product_name)
    # print(biddedItemId)
    products = Product.objects.all().filter(product_bid_time__in=timeId,id__in=biddedItemId)
    Context = {'bidded_products':products,'datetime':date_for_site}
    
    return render(request,'viewBidedProducts.html',Context)

#  ================================ End of The rendering the views of the item whose bidding time is finished ======================= 
    
    
    
 # ============================== this functions helps us to give the winner amount and name  ========================
@login_required(login_url='log_in')
def Winner(request,id):
    flag=False
    product = Product.objects.get(id=id)
    Context = {"product":product,'flag':flag}
    all_amounts = BiddingAmount.objects.all().filter(product_name=id)
    if len(all_amounts)==0:
        myMessage = "Noone Has Bidded on Your Products"
        Context['myMessage']=myMessage
    else:
        flag=True
        amounts = []
        for item in all_amounts:
            amounts.append(item.bid_amount)
        # print(amounts)
        bubbleSort(amounts)
        n  = len(amounts)
        Max_Amount = amounts[n-1]
        Context['Max_Amount']=Max_Amount
        
        # For Taking Max Bidder Name
        max_bidder_from_BiddingAmount = BiddingAmount.objects.all().filter(product_name=id,bid_amount=Max_Amount)
        
        for item in max_bidder_from_BiddingAmount:
            userId = item.bidder_name
            
        # print(userId)
        
        max_bidder = User.objects.get(id=userId)
        print(max_bidder.email)
        # for item in max_bidder:
        #     print(item.email)
        Context['max_bidder']=max_bidder
        Context['flag']=flag
        Context['datetime'] = date_for_site
         
    
    return render(request,'ViewWinner.html',Context)

# ================                   End of the winner Function ======================================


#  ========================== Start of view other's going to be bidded products ======================

from json import dumps
from django.http import JsonResponse
@login_required(login_url="log_in")
def view_products_going_to_bid(request):
    date_today = date.today()
    print(date_today)
    time = BiddingTime.objects.all().filter(bid_day__gt=date_today)
    timeId = []
    for item in time:
        timeId.append(item.id)
    # print(timeId)
    
    product = Product.objects.all().filter(product_bid_time__in=timeId)
    category = Category.objects.all()
    user = User.objects.all()
    timeDictonary = {}
    for item in time:
        timeDictonary[item.id]={"bid_day":item.bid_day,"bid_start_time":item.bid_start_time,"bid_end_time":item.bid_end_time}
    
    # print(timeDictonary)
        
    # timeDictonary JsonResponse(timelist,safe=False)
    dataJSON = dumps(timeDictonary,indent=4, sort_keys=True, default=str)
    context = {"product":product,"user":user,"Category":category,"time":time,"data":dataJSON}
    return render(request,"goingtobid.html",context)


