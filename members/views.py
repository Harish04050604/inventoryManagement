from gettext import translation
from django.shortcuts import render, redirect,get_object_or_404
from .models import Signup
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Item 
from django.http import JsonResponse
from .models import Item
from django.shortcuts import render, redirect,get_object_or_404
from .models import Signup
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Item 
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from .models import Item
from reportlab.lib.pagesizes import letter
import os
from django.conf import settings

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

from django.utils.timezone import now
from .models import AddItem  # Import AddItem model

def add_items(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        number_of_items = request.POST.get("number_of_items")
        selling_price = request.POST.get("selling_price")
        date_of_production = request.POST.get("date_of_production")
        total_production_cost = request.POST.get("total_production_cost")

        if item_name and number_of_items and selling_price and date_of_production and total_production_cost:
            item, created = Item.objects.get_or_create(
                ItemName=item_name,
                defaults={
                    "NumberOfItems": int(number_of_items),
                    "SellingPrice": float(selling_price),
                },
            )

            # Update quantity if item exists
            if not created:
                item.NumberOfItems += int(number_of_items)
                item.save()

            # Store production details in AddItem model
            AddItem.objects.create(
                item=item,
                date_of_production=date_of_production,
                total_items_produced=int(number_of_items),  # Use same value
                total_production_cost=float(total_production_cost),
            )

            return redirect("view_tasks")

    return render(request, "add_items.html")

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

def add_item(request, item_name):
    item = get_object_or_404(Item, ItemName=item_name)

    if request.method == "POST":
        number_of_items = int(request.POST.get("number_of_items", 0))
        date_of_production = request.POST.get("date_of_production")
        total_production_cost = request.POST.get("total_production_cost")

        if number_of_items > 0 and date_of_production and total_production_cost:
            # Update total number of items in inventory
            item.NumberOfItems += number_of_items
            item.save()

            # Store only the new quantity in history
            AddItem.objects.create(
                item=item,
                date_of_production=date_of_production,
                total_items_produced=number_of_items,  # Only new quantity
                total_production_cost=float(total_production_cost),
            )

            messages.success(request, f"Successfully added {number_of_items} units to {item.ItemName}.")
            return redirect("view_tasks")
        else:
            messages.error(request, "Please provide valid details.")

    return render(request, "add_item.html", {"item": item})



from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from .models import Item, SellItem  # Ensure SellItem model is imported

def sell_item(request, item_name):
    item = get_object_or_404(Item, ItemName=item_name)

    if request.method == 'POST':
        try:
            quantity_to_sell = int(request.POST.get('number_of_items', 1))

            if quantity_to_sell <= 0:
                messages.error(request, 'Quantity must be greater than zero.')
                return redirect('sell_item', item_name=item.ItemName)

            if quantity_to_sell > item.NumberOfItems:
                messages.error(request, f'Cannot sell more than available stock ({item.NumberOfItems}).')
                return redirect('sell_item', item_name=item.ItemName)

            total_sales_price = quantity_to_sell * item.SellingPrice  # Calculate total price

            with transaction.atomic():  
                # Deduct sold items from inventory
                item.NumberOfItems -= quantity_to_sell
                item.save()

                # Store sale in SellItem table
                SellItem.objects.create(
                    item=item,
                    date_of_sales=timezone.now().date(),
                    total_items_sold=quantity_to_sell,
                    total_sales_price=total_sales_price
                )

            messages.success(request, f'Successfully sold {quantity_to_sell} units of {item.ItemName}.')
            return redirect('view_tasks')  

        except ValueError:
            messages.error(request, 'Invalid quantity entered.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'sell_item.html', {'item': item})


def generate_report(request):
    """Renders the inventory report in HTML format."""
    items = Item.objects.all()
    sell_items=SellItem.objects.all()
    return render(request, "report.html", {"sell_items": sell_items, "items": items}) 

from django.contrib.staticfiles.finders import find

# In your function
logo_path = find('images/company-logo.png')

import os
import logging
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors 

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
    
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Inventory Report")
    
    # Construct path to logo file
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'company-logo.png')
    
    # Log the path for debugging
    logging.debug(f"Attempting to load logo from: {logo_path}")
    
    try:
        # Check if file exists before loading
        if os.path.exists(logo_path):
            pdf.drawImage(logo_path, 500, 740, width=100, height=50, preserveAspectRatio=True)
            logging.debug("Logo loaded successfully")
        else:
            logging.warning(f"Logo file not found at: {logo_path}")
    except Exception as e:
        logging.error(f"Error loading logo: {e}")
    
    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(300, 760, "Inventory Report")
    
    # Get items first to avoid multiple queries
    items = SellItem.objects.all()
    row_count = len(items)
    
    # Calculate the bottom of the table
    table_bottom = 680 - (row_count * 20)
    
    # Draw table borders and background
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor(colors.lightgrey)
    pdf.rect(50, 680, 500, 20, fill=1)  # Header row background
    
    # Vertical lines for the entire table
    pdf.line(50, 700, 50, table_bottom)  # Left border
    pdf.line(150, 700, 150, table_bottom)  # After Item Name
    pdf.line(250, 700, 250, table_bottom)  # After Quantity
    pdf.line(400, 700, 400, table_bottom)  # After Date
    pdf.line(550, 700, 550, table_bottom)  # Right border
    
    # Table Headers
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 685, "Item Name")
    pdf.drawString(160, 685, "Quantity Sold")
    pdf.drawString(300, 685, "Date")
    pdf.drawString(440, 685, "Sales Price (Rs)")
    
    # Draw horizontal line below headers
    pdf.line(50, 680, 550, 680)
    
    # Data
    y = 660
    pdf.setFont("Helvetica", 10)
    
    for i, sell_item in enumerate(items):
        # Draw data
        pdf.drawString(60, y + 5, sell_item.item.ItemName)
        pdf.drawString(190, y + 5, str(sell_item.total_items_sold))
        pdf.drawString(295, y + 5, str(sell_item.date_of_sales))
        pdf.drawRightString(500, y + 5, f"{sell_item.total_sales_price:.2f}")
        
        # Draw horizontal line after each row
        pdf.line(50, y, 550, y)
        
        y -= 20  # Move down
    
    pdf.save()
    return response