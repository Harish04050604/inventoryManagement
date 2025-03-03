from django.shortcuts import render, redirect,get_object_or_404
from .models import Signup
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Item 
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

@csrf_exempt  # Only if you're having CSRF issues during testing
def delete_item(request):
    if request.method == 'POST':
        try:
            item_name = request.POST.get('item_name')
            if not item_name:
                return JsonResponse({'success': False, 'error': 'Item name is required'})
            
            # Get the item and delete it
            item = Item.objects.get(ItemName=item_name)
            item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Item {item_name} successfully deleted'
            })
            
        except Item.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Item {item_name} not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def task_list(request):  # or whatever your main view is called
    items = Item.objects.all()
    return render(request, 'your_template.html', {
        'items': items,
    })

@ensure_csrf_cookie
def edit_item(request, item_name):
    item = get_object_or_404(Item, ItemName=item_name)

    if request.method == 'POST':
        new_item_name = request.POST.get('item_name')
        number_of_items = request.POST.get('number_of_items')
        selling_price = request.POST.get('selling_price')

        # Ensure new name does not already exist (except for this item)
        if new_item_name != item.ItemName and Item.objects.filter(ItemName=new_item_name).exists():
            return render(request, 'edit_item.html', {'item': item, 'error': 'Item name already exists'})

        # Update fields
        item.ItemName = new_item_name
        item.NumberOfItems = number_of_items
        item.SellingPrice = selling_price
        item.save()

        return redirect('view_tasks')

    return render(request, 'edit_item.html', {'item': item})
