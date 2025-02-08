from django.shortcuts import render, redirect
from .models import Signup
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        designation=request.POST.get('designation')
        user = Signup.objects.filter(username=username, password=password, designation=designation).first()
        
        if user:
            if designation=="manager":
                return redirect('manager')
            else:
                return redirect('staff')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        designation=request.POST.get('designation')

        # filling all fields
        if not username or not email or not password or not confirm_password or not designation:
            return render(request, 'signup.html', {'error': 'All fields are required'})

        # to ensure password and confirmation password are same
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # to check whether same username should not exist for more than one person
        if Signup.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        Signup.objects.create(username=username, email=email, password=password, designation=designation) # this line is used to store the user contents in members_signup table present in mysql workbench login database
        return redirect('login')
    return render(request, 'signup.html')

def manager(request):
    return render(request, 'manager.html')

def staff(request):
    return render(request, 'staff.html')

def view_tasks(request):
    items = Item.objects.all()
    return render(request, 'task.html', {'items': items})

def add_items(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        number_of_items = request.POST.get("number_of_items")
        selling_price = request.POST.get("selling_price")

        if item_name and number_of_items and selling_price:
            Item.objects.create(
                ItemName=item_name,
                NumberOfItems=int(number_of_items),
                SellingPrice=float(selling_price)
            )
            return redirect('view_tasks')  # Redirect to task page after adding

    return render(request, 'add_items.html')

@csrf_exempt
def update_quantity(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        action = request.POST.get("action")  # 'increase' or 'decrease'

        item = Item.objects.get(ItemName=item_name)
        if action == "increase":
            item.NumberOfItems += 1
        elif action == "decrease" and item.NumberOfItems > 0:
            item.NumberOfItems -= 1

        item.save()
        return JsonResponse({"success": True, "new_quantity": item.NumberOfItems})

    return JsonResponse({"success": False})