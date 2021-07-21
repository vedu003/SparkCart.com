from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Contact, Profile
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


class ProductView(View):
    def get(self,request):
        totalitems = 0
        mobiles = Product.objects.filter(id__in=[27,45,52,33,24,31,190])
        lc = Product.objects.filter(id__in=[59,84,62,90,70,77,79])
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'mobiles':mobiles,'lc':lc, 'totalitems':totalitems})


class ProductDetailView(View):
    def get(self,request,pk):
        totalitems = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart,'totalitems':totalitems})

@login_required
def add_to_cart(request):
    user= request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()

    return redirect('/cart')

@login_required
def show_cart(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_Amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = ( p.quantity * p.product.discounted_price )
                amount= amount + tempamount
                total_Amount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':total_Amount, 'amount':amount, 'shipping_Amount': shipping_amount,'totalitems':totalitems})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_Amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = ( p.quantity * p.product.discounted_price )
            amount= amount + tempamount
        
        data = {
            'amount': amount,
            'totalamount' : amount + shipping_amount,
            'quantity': c.quantity
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        if c.quantity == 0:
            c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_Amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        clen= len(cart_product)

        for p in cart_product:
            tempamount = ( p.quantity * p.product.discounted_price )
            amount= amount + tempamount
        
        data = {
            'amount': amount,
            'totalamount' : amount + shipping_amount,
            'quantity': c.quantity,
            'len':clen
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_Amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        clen= len(cart_product)

        for p in cart_product:
            tempamount = ( p.quantity * p.product.discounted_price )
            amount= amount + tempamount
            
        data = {
            'amount': amount,
            'totalamount' : amount + shipping_amount,
            'len':clen
        }
        return JsonResponse(data)

@login_required            
def empty_cart(request):
    return render(request, 'app/emptycart.html')

@login_required
def manageaddress(request):
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if request.method =="POST":
        user = request.user
        name= request.POST.get('name','')
        contact= request.POST.get('contact','')
        locality= request.POST.get('locality','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zipcode= request.POST.get('zip','')
        profile = Customer(user=user, name=name, contact=contact,locality=locality, city=city, state=state, zipcode=zipcode)
        profile.save()
        messages.success(request,'Your Address is Added Successfully.')
        return redirect('address')
        
    return render(request, 'app/manageaddress.html',{'active':'btn-warning', 'totalitems':totalitems})

@login_required
def address(request):
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-warning', 'totalitems':totalitems})

@login_required
def profile(request):   
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))

    if request.method =="POST":
        user = request.user
        name= request.POST.get('name','')
        dob= request.POST.get('dob','')
        contact= request.POST.get('contact','')
        gender= request.POST.get('gender','')
        profile = Profile(user=user, name=name,dob=dob, contact=contact,gender=gender)
        messages.success(request,'Your Profile is Updated Successfully.')
        profile.save()

    profile = Profile.objects.filter(user=request.user)
    return render(request, 'app/profile.html',{'profile':profile,'active':'btn-warning', 'totalitems':totalitems})    

@login_required
def manage_profile(request, id):
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    pr = Profile.objects.get(pk=id)
    if request.method == 'POST':
        pr.name= request.POST.get('name','')
        pr.dob= request.POST.get('dob','')
        pr.contact= request.POST.get('contact','')
        pr.gender= request.POST.get('gender','')
        pr.save()
        messages.success(request,'Your Profile is Updated Successfully.')
        return redirect('profile')

    return render(request, 'app/manageprofile.html', {'id': id,'pr':pr, 'active':'btn-warning', 'totalitems':totalitems})


@login_required
def update_address(request, id):
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    cust = Customer.objects.get(pk=id)
    if request.method == 'POST':
        cust.name= request.POST.get('name','')
        cust.contact= request.POST.get('contact','')
        cust.locality= request.POST.get('locality','')
        cust.city= request.POST.get('city','')
        cust.state= request.POST.get('state','')
        cust.zipcode= request.POST.get('zip','')
        cust.save()
        messages.success(request,'Your Address is Updated Successfully.')
        return redirect('address')

    return render(request, 'app/updateaddress.html', {'id': id,'add':cust, 'active':'btn-warning', 'totalitems':totalitems})

@login_required
def delete_address(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Your Address is Deleted Successfully.')
        return redirect('address')

@login_required
def orders(request):
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.order_by('-ordered_date').filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op, 'totalitems':totalitems})



def mobile(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category = 'Mobile')
    
    elif data == 'Mi'or data == 'Samsung' or data == 'Apple' or data == 'One' or data == 'Realme':
        mobiles = Product.objects.filter(category = 'Mobile').filter(brand = data)
    
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'Mobile').filter(discounted_price__lt=15000)
    
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'Mobile').filter(discounted_price__gt=15000)

    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitems':totalitems})


def laptop(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    
    elif data == 'Dell'or data == 'HP' or data == 'Lenovo' or data == 'MacBook':
        laptops = Product.objects.filter(category = 'L').filter(brand = data)
    
    elif data == 'below':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__lt=50000)
    
    elif data == 'above':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__gt=50000)

    return render(request, 'app/laptop.html', {'laptops':laptops, 'totalitems':totalitems})


def camera(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        cameras = Product.objects.filter(category = 'C')
    
    elif data == 'Canon'or data == 'Nikon' or data == 'Sony':
        cameras = Product.objects.filter(category = 'C').filter(brand = data)
    
    elif data == 'below':
        cameras = Product.objects.filter(category = 'C').filter(discounted_price__lt=50000)
    
    elif data == 'above':
        cameras = Product.objects.filter(category = 'C').filter(discounted_price__gt=50000)

    return render(request, 'app/camera.html', {'cameras':cameras, 'totalitems':totalitems})


def menWatches(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mwatches = Product.objects.filter(category = 'MW')
    
    elif data == 'Fastrack'or data == 'Titan' or data == 'Fossil' or data == 'Casio':
        mwatches = Product.objects.filter(category = 'MW').filter(brand = data)
    
    elif data == 'below':
        mwatches = Product.objects.filter(category = 'MW').filter(discounted_price__lt=5000)
    
    elif data == 'above':
        mwatches = Product.objects.filter(category = 'MW').filter(discounted_price__gt=5000)

    return render(request, 'app/menwatch.html', {'mwatches':mwatches, 'totalitems':totalitems})

def womenWatches(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wwatches = Product.objects.filter(category = 'WW')
    
    elif data == 'Fastrack'or data == 'Titan' or data == 'Fossil' or data == 'Casio':
        wwatches = Product.objects.filter(category = 'WW').filter(brand = data)
    
    elif data == 'below':
        wwatches = Product.objects.filter(category = 'WW').filter(discounted_price__lt=5000)
    
    elif data == 'above':
        wwatches = Product.objects.filter(category = 'WW').filter(discounted_price__gt=5000)

    return render(request, 'app/womenwatch.html', {'wwatches':wwatches, 'totalitems':totalitems})

def mensTshirt(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mtshirt = Product.objects.filter(category = 'MTS')
    
    return render(request, 'app/mentshirt.html', {'mtshirt':mtshirt, 'totalitems':totalitems})

def womensTshirt(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wtshirt = Product.objects.filter(category = 'WTS')
    
    return render(request, 'app/womentshirt.html', {'wtshirt':wtshirt, 'totalitems':totalitems})

def shirt(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        shirt = Product.objects.filter(category = 'MS')
    
    return render(request, 'app/shirt.html', {'shirt':shirt, 'totalitems':totalitems})

def menJeans(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mjeans = Product.objects.filter(category = 'MJ')
    
    return render(request, 'app/menjeans.html', {'mjeans':mjeans, 'totalitems':totalitems})

def womenJeans(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wjeans = Product.objects.filter(category = 'WJ')
    
    return render(request, 'app/womenjeans.html', {'wjeans':wjeans, 'totalitems':totalitems})


def menSuit(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        msuit = Product.objects.filter(category = 'MSU')
    
    return render(request, 'app/mensuit.html', {'msuit':msuit, 'totalitems':totalitems})

def womenSaree(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wsaree = Product.objects.filter(category = 'WSA')
    
    return render(request, 'app/womensaree.html', {'wsaree':wsaree, 'totalitems':totalitems})

def womenKurti(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wkurti = Product.objects.filter(category = 'WK')
    
    return render(request, 'app/womenkurti.html', {'wkurti':wkurti, 'totalitems':totalitems})

def womenTops(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wtops = Product.objects.filter(category = 'WT')
    
    return render(request, 'app/womentop.html', {'wtops':wtops, 'totalitems':totalitems})

def menShoes(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        mshoes = Product.objects.filter(category = 'MSH')
    
    return render(request, 'app/menshoes.html', {'mshoes':mshoes, 'totalitems':totalitems})

def womenShoes(request, data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    if data == None:
        wshoes = Product.objects.filter(category = 'WSH')
    
    return render(request, 'app/womenshoes.html', {'wshoes':wshoes, 'totalitems':totalitems})

@login_required
def checkout(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_Amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:        
        for p in cart_product:
            tempamount = ( p.quantity * p.product.discounted_price )
            amount= amount + tempamount
        
        total_Amount = amount + shipping_amount
    
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':total_Amount, 'cart_items':cart_item, 'shipping_Amount':shipping_amount, 'totalitems':totalitems})

@login_required
def payment_done(request):
    user= request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    messages.success(request,'Order Placed Successfully.')
    return redirect("orders")


def contact(request):
    if request.method =="POST":
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        contact= request.POST.get('contact','')
        feedback= request.POST.get('feedback','')
        Contact(name=name, email=email, contact=contact, feedback=feedback).save()
        subject = 'Hello ' + name + ' from SparkCart.com!'
        message = 'Your Responce: '+feedback+'\nStay Connected. We would love to hear you!'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email, ]
        send_mail(subject, message, email_from, email_to)
        messages.success(request,'Your Feedback is Submitted Successfully and you will get a mail.')
        return redirect("home")

    return render(request, 'app/contact.html')

def searchMatch(query,item):
    if query.lower() in item.title.lower() or query.lower() in item.category.lower() or query.lower() in item.brand.lower():
        return True
    else:
        return False

def search(request):
    
    totalitems=0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    query = request.GET.get('search')
    prods = Product.objects.all()
    prod = [item for item in prods if searchMatch(query,item)]
    prodlen=len(prod)
    if prodlen== 0:
        return render(request, 'app/search.html')
    else:
        return render(request,'app/search.html',{'products':prod, 'totalitems':totalitems})