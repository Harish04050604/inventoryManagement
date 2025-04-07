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


from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Item

@ensure_csrf_cookie
def delete_item(request, item_name):
    item = get_object_or_404(Item, ItemName=item_name)

    if request.method == 'POST':
        item.delete()
        return redirect('view_tasks')  # Redirect to the appropriate page after deletion

    return render(request, 'delete_item.html', {'item': item})


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


from django.shortcuts import render
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from .models import SellItem, AddItem

def generate_report(request):
    """Renders the inventory report in HTML format with profit calculations."""

    # Get the start and end dates of the current week (Monday-Sunday)
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Get sales and production data within the current week
    sales = SellItem.objects.filter(date_of_sales__range=[start_of_week, end_of_week])
    production = AddItem.objects.filter(date_of_production__range=[start_of_week, end_of_week])

    # Calculate profit per day
    daily_profit = {}
    for day_offset in range(7):  # Loop through each day of the week
        day = start_of_week + timedelta(days=day_offset)
        total_sales = sales.filter(date_of_sales=day).aggregate(Sum('total_sales_price'))['total_sales_price__sum'] or 0
        total_cost = production.filter(date_of_production=day).aggregate(Sum('total_production_cost'))['total_production_cost__sum'] or 0
        daily_profit[day] = total_sales - total_cost

    # Calculate total weekly profit
    weekly_profit = sum(daily_profit.values())

    return render(request, "report.html", {
        "sell_items": sales,
        "daily_profit": daily_profit,
        "weekly_profit": weekly_profit
    })

from django.contrib.staticfiles.finders import find

# In your function
logo_path = find('images/company-logo.png')

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
import os
import logging
from django.conf import settings
from members.models import SellItem, AddItem  # Adjust your model imports

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
    
    # Get data
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Fetch sales data
    sales = SellItem.objects.filter(date_of_sales__range=[start_of_week, end_of_week])

    # Fetch production data and calculate daily profits
    production = AddItem.objects.filter(date_of_production__range=[start_of_week, end_of_week])
    
    # Use proper aggregation with Coalesce to handle None values
    daily_profit = {}
    for day_offset in range(7):
        day = start_of_week + timedelta(days=day_offset)
        
        # Use Coalesce to handle None values safely
        total_sales = sales.filter(date_of_sales=day).aggregate(
            total=Coalesce(Sum('total_sales_price'), 0, output_field=DecimalField())
        )['total'] or 0
        
        total_cost = production.filter(date_of_production=day).aggregate(
            total=Coalesce(Sum('total_production_cost'), 0, output_field=DecimalField())
        )['total'] or 0
        
        # Convert to float to avoid decimal iteration issues
        daily_profit[day] = float(total_sales) - float(total_cost)

    # Calculate weekly profit as float
    weekly_profit = sum(daily_profit.values())
    
    # Create PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Common functions
    def add_page_elements(pdf, title):
        # Add watermark
        pdf.saveState()
        pdf.setFont("Helvetica-Bold", 60)
        pdf.setFillColor(colors.lightgrey.clone(alpha=0.3))  # Transparent watermark
        pdf.rotate(45)
        pdf.drawString(180, 40, "CONFIDENTIAL")
        pdf.restoreState()
        
        # Add logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'company-logo.png')
        try:
            if os.path.exists(logo_path):
                pdf.drawImage(logo_path, width - 1.5*inch, height - 0.8*inch, width=1.2*inch, height=0.6*inch, preserveAspectRatio=True)
        except Exception as e:
            logging.error(f"Error loading logo: {e}")
        
        # Add header
        pdf.setFont("Helvetica-Bold", 18)
        pdf.setFillColor(colors.black)
        pdf.drawString(1*inch, height - 1*inch, title)
        
        # Add date range
        pdf.setFont("Helvetica", 10)
        pdf.drawString(1*inch, height - 1.25*inch, f"Period: {start_of_week.strftime('%b %d, %Y')} - {end_of_week.strftime('%b %d, %Y')}")
        
        # Add horizontal line
        pdf.setLineWidth(1)
        pdf.line(1*inch, height - 1.4*inch, width - 1*inch, height - 1.4*inch)
        
        # Add page number
        pdf.drawRightString(width - 1*inch, 0.5*inch, f"Page {pdf.getPageNumber()}")
        
        # Add footer
        pdf.setFont("Helvetica-Oblique", 8)
        pdf.drawCentredString(width/2, 0.5*inch, "Confidential - For Internal Use Only")
        
        return height - 1.7*inch  # Return Y position for content

    # Page 1 - Available Stocks
    pdf.setTitle("Inventory Report")
    y = add_page_elements(pdf, "Available Stocks Report")
    
    # Sales Table
    data = [["Item Name", "Quantity Sold", "Date", "Sales Price (Rs)"]]
    
    for sell_item in sales:
        # Convert Decimal to float before formatting
        sales_price = float(sell_item.total_sales_price) if sell_item.total_sales_price else 0
        
        data.append([
            sell_item.item.ItemName,
            str(sell_item.total_items_sold),
            sell_item.date_of_sales.strftime("%b %d, %Y"),
            f"{sales_price:,.2f}"
        ])
    
    # Calculate column widths
    col_widths = [2.5*inch, 1.2*inch, 1.5*inch, 1.5*inch]
    
    # Create table
    table = Table(data, colWidths=col_widths)
    
    # Style the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    # Add alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey.clone(alpha=0.3))
    
    table.setStyle(table_style)
    
    # Draw the table
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 1*inch, y - (len(data) * 0.4*inch))
    
    # Add totals
    y_total = y - (len(data) * 0.4*inch) - 0.5*inch
    
    # Calculate total sales safely
    total_sales_value = 0
    for item in sales:
        if item.total_sales_price:
            total_sales_value += float(item.total_sales_price)
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(width - 1*inch, y_total, f"Total Sales: Rs {total_sales_value:,.2f}")
    
    # Move to next page
    pdf.showPage()

    # Page 2 - Profit of the Week
    y = add_page_elements(pdf, "Weekly Profit Report")
    
    # Profit Table
    profit_data = [["Date", "Sales (Rs)", "Costs (Rs)", "Profit (Rs)"]]
    
    sorted_dates = sorted(daily_profit.keys())
    for date in sorted_dates:
        # Get sales and costs for the day safely
        day_sales = sales.filter(date_of_sales=date).aggregate(
            total=Coalesce(Sum('total_sales_price'), 0, output_field=DecimalField())
        )['total'] or 0
        
        day_costs = production.filter(date_of_production=date).aggregate(
            total=Coalesce(Sum('total_production_cost'), 0, output_field=DecimalField())
        )['total'] or 0
        
        # Convert to float to avoid decimal iteration issues
        day_sales_float = float(day_sales)
        day_costs_float = float(day_costs)
        
        profit_data.append([
            date.strftime("%a, %b %d"),
            f"{day_sales_float:,.2f}",
            f"{day_costs_float:,.2f}",
            f"{daily_profit[date]:,.2f}"
        ])
    
    # Calculate total sales and costs
    total_sales_float = 0
    for item in sales:
        if item.total_sales_price:
            total_sales_float += float(item.total_sales_price)
    
    total_costs_float = 0
    for item in production:
        if item.total_production_cost:
            total_costs_float += float(item.total_production_cost)
    
    # Add totals row
    profit_data.append([
        "TOTAL",
        f"{total_sales_float:,.2f}",
        f"{total_costs_float:,.2f}",
        f"{weekly_profit:,.2f}"
    ])
    
    # Calculate column widths
    profit_col_widths = [1.5*inch, 1.7*inch, 1.7*inch, 1.7*inch]
    
    # Create table
    profit_table = Table(profit_data, colWidths=profit_col_widths)
    
    # Style the table
    profit_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        # Style for the total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue.clone(alpha=0.3)),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ])
    
    # Add alternating row colors
    for i in range(1, len(profit_data)-1):
        if i % 2 == 0:
            profit_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey.clone(alpha=0.3))
    
    profit_table.setStyle(profit_style)
    
    # Draw the table
    profit_table.wrapOn(pdf, width, height)
    profit_table.drawOn(pdf, 1*inch, y - (len(profit_data) * 0.4*inch))
    
    # Add profit/loss summary
    y_summary = y - (len(profit_data) * 0.4*inch) - 1*inch
    profit_status = "PROFIT" if weekly_profit >= 0 else "LOSS"
    profit_color = colors.green if weekly_profit >= 0 else colors.red
    
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(profit_color)
    pdf.drawCentredString(width/2, y_summary, f"Weekly {profit_status}: Rs {abs(weekly_profit):,.2f}")
    
    # Add a simple bar chart for daily profits
    chart_y = y_summary - 2*inch
    chart_width = 6*inch
    chart_height = 1.5*inch
    
    # Find max profit value safely
    max_profit = 0
    min_profit = 0
    for profit in daily_profit.values():
        if profit > max_profit:
            max_profit = profit
        if profit < min_profit:
            min_profit = profit
    
    max_abs_profit = max(max_profit, abs(min_profit))
    
    # Draw chart title
    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColor(colors.black)
    pdf.drawString(1*inch, chart_y + chart_height + 0.2*inch, "Daily Profit Breakdown")
    
    # Draw chart background
    pdf.setFillColor(colors.lightgrey.clone(alpha=0.3))
    pdf.rect(1*inch, chart_y, chart_width, chart_height, fill=1, stroke=1)
    
    # Draw x-axis
    pdf.setLineWidth(1)
    pdf.line(1*inch, chart_y, 1*inch + chart_width, chart_y)
    
    # Draw y-axis
    pdf.line(1*inch, chart_y, 1*inch, chart_y + chart_height)
    
    # Draw bars
    bar_width = chart_width / len(daily_profit)
    bar_spacing = 0.1 * bar_width
    
    for i, (date, profit) in enumerate(sorted(daily_profit.items())):
        # Calculate bar height safely
        bar_height = 0
        if max_abs_profit > 0:  # Avoid division by zero
            bar_height = (profit / max_abs_profit) * chart_height
        
        x = 1*inch + i * bar_width + bar_spacing
        if profit >= 0:
        # For profit bars, start from the baseline and go up
            y = chart_y
        else:
        # For loss bars, start from the baseline and go down, but stay within the box
            y = chart_y
        bar_height = abs(bar_height)
        pdf.setFillColor(colors.green if profit >= 0 else colors.red)
        pdf.rect(x, y, bar_width - 2*bar_spacing, bar_height, fill=1, stroke=0)
        
        # Draw day label
        pdf.setFont("Helvetica", 8)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(x + (bar_width - 2*bar_spacing)/2, chart_y - 0.2*inch, date.strftime("%a"))
    
    pdf.save()
    return response

def search_item(request):
    query = request.GET.get("query", "")
    if query:
        items = Item.objects.filter(ItemName__istartswith=query)  # Case-insensitive search from left to right
    else:
        items = Item.objects.all()  # If no search query, show all items
    
    return render(request, "task.html", {"items": items})


from datetime import timedelta
from .models import SellItem, ForecastData, Item
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.utils import timezone

def forecast_demand(request):
    items = SellItem.objects.all().select_related('item')

    if not items:
        return render(request, 'forecast.html', {'error': 'No sales data found.'})

    df = pd.DataFrame(list(items.values('item__ItemName', 'date_of_sales', 'total_items_sold')))
    df['date_of_sales'] = pd.to_datetime(df['date_of_sales'])

    forecasts = []

    for item_name in df['item__ItemName'].unique():
        item_data = df[df['item__ItemName'] == item_name].copy()
        item_data.set_index('date_of_sales', inplace=True)
        item_data = item_data.resample('W').sum()
        item_data = item_data[item_data['total_items_sold'] > 0].dropna()

        if item_data.empty or len(item_data) < 8:
            forecasts.append({'item_name': item_name, 'forecast': 'Not enough data'})
            continue

        try:
            model = ARIMA(item_data['total_items_sold'], order=(1, 1, 1))
            fitted_model = model.fit()
            forecast = fitted_model.forecast(steps=1)
            forecast_value = round(np.atleast_1d(forecast)[0])

            # Save to ForecastData table
            item_instance = Item.objects.get(ItemName=item_name)
            ForecastData.objects.create(
                item=item_instance,
                forecasted_demand=forecast_value,
                forecast_date=timezone.now().date()
            )

            forecasts.append({
                'item_name': item_name,
                'forecast': forecast_value
            })

        except Exception as e:
            forecasts.append({
                'item_name': item_name,
                'forecast': 'Error: ' + str(e)
            })

    return render(request, 'forecast.html', {'forecasts': forecasts})


