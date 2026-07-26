from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Restaurant, User, Item, Cart

# Create your views here.
import razorpay
from django.conf import settings

def index(request):
    return render(request, "index.html")
def open_signup(request):
    return render(request, "signup.html")
def open_signin(request):
    return render(request, "signin.html")
def signup(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address = request.POST.get("address")

        if password != confirm_password:
            return HttpResponse("""
    <div style="background:#ffebee;color:#d32f2f;padding:20px;
    text-align:center;font-size:20px;font-weight:bold;
    border-radius:10px;margin:50px auto;width:400px;">
        Passwords do not match!
    </div>
    """)

        if User.objects.filter(email=email).exists():
            return HttpResponse("""
    <div style="background:#fff3cd;color:#856404;padding:20px;
    text-align:center;font-size:20px;font-weight:bold;
    border-radius:10px;margin:50px auto;width:500px;">
        This email is already registered. Please use a different email.
    </div>
    """)

        user = User(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        user.save()

        return render(request, "signin.html")

    return HttpResponse("Invalid Response")
    
def signin(request):
    user = "adminboss"
    pwd = "123"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        User.objects.get(username=username, password=password)
        if username == 'adminboss':
            return render(request, 'admin_home.html')
        else:
            restaurantList = Restaurant.objects.all()
            return render(request, 'customer_home.html', {"restaurantList" : restaurantList , "username" : username})
        
    except User.DoesNotExist:
        return render(request, 'fail.html')
    
def open_add_restaurant(request):
    return render(request, 'add_restaurants.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("""
<div style="width:520px;margin:80px auto;padding:30px;background:#ffebee;color:#c62828;
                                border:1px solid #ef9a9a;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.2);
                                text-align:center;font-family:Arial,sans-serif;font-size:22px;font-weight:bold;">
                                ❗ Duplicate Restaurant!</div> """)
            
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
        return HttpResponse("""
<div style="width:520px;margin:80px auto;padding:30px;background:#e8f5e9;color:#2e7d32;border:1px solid #81c784;
                            border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.2);text-align:center;font-family:Arial,sans-serif;
                            font-size:22px;font-weight:bold;">
                            ✅ Successfully Added!</div>
""")
    
def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurant.html',{"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    #itemList = restaurant.items.all()
    itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("""
<div style="width:520px;margin:80px auto;padding:30px;background:#ffebee;color:#c62828;
                                border:1px solid #ef9a9a;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.2);
                                text-align:center;font-family:Arial,sans-serif;font-size:22px;font-weight:bold;">
                                ❗ Duplicate Item!</div> """)
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    #return render(request, 'admin_home.html')
    return HttpResponse("Item Added!")

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return HttpResponse("Item deleted successfully.")

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant" : restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurant.html',{"restaurantList" : restaurantList})

def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant,id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurant.html',{"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    return render(request, 'admin_home.html')

def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #return HttpResponse("Items collected")
    #itemList = Item.objects.all()
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant, 
                     "username":username})

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = User.objects.get(username = username)

    cart, created = Cart.objects.get_or_create(customer = customer)

    cart.items.add(item)

    return HttpResponse('added to cart')

def show_cart(request, username):
    customer = User.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})


def remove_item(request, item_id, username):
    customer = User.objects.get(username=username)
    cart = Cart.objects.get(customer=customer)
    item = Item.objects.get(id=item_id)

    cart.items.remove(item)

    return redirect('show_cart', username=username)


def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'error': 'Your cart is empty!', 'username' : username,
        })
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })

def orders(request, username):
    customer = get_object_or_404(User, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price before clearing the cart
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })