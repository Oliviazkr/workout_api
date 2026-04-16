from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json

from .models import FoodItem, CalculationHistory
from .forms import RegisterForm, LoginForm, FoodItemForm, CSVUploadForm


# ============ Home ============
def home(request):
    """Home - Nutrition Calculator"""
    foods = FoodItem.objects.all()

    # Get categories for filtering - ensure distinct
    categories = FoodItem.objects.values_list('category', flat=True).distinct()
    categories = sorted([c for c in categories if c])

    context = {
        'foods': foods,
        'categories': categories,
    }
    return render(request, 'calculator/home.html', context)


# ============ Authentication Views ============
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'calculator/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'calculator/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('home')


# ============ Food Management ============
@login_required
def food_list(request):
    """Food list page"""
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    foods = FoodItem.objects.all()
    if search:
        foods = foods.filter(name__icontains=search)
    if category:
        foods = foods.filter(category=category)

    # Get all distinct categories and sort
    categories = FoodItem.objects.values_list('category', flat=True).distinct()
    categories = sorted([c for c in categories if c])  # Filter out empty values and sort

    context = {
        'foods': foods,
        'categories': categories,
        'search': search,
        'selected_category': category,
    }
    return render(request, 'calculator/food_list.html', context)


@login_required
def food_add(request):
    """Add food"""
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food = form.save()
            messages.success(request, f'"{food.name}" added successfully!')
            return redirect('food_list')
    else:
        form = FoodItemForm()
    return render(request, 'calculator/food_form.html', {'form': form, 'title': 'Add Food'})


@login_required
def food_edit(request, pk):
    """Edit food"""
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{food.name}" updated successfully!')
            return redirect('food_list')
    else:
        form = FoodItemForm(instance=food)
    return render(request, 'calculator/food_form.html', {'form': form, 'title': 'Edit Food', 'food': food})


@login_required
def food_delete(request, pk):
    """Delete food"""
    food = get_object_or_404(FoodItem, pk=pk)
    name = food.name
    food.delete()
    messages.success(request, f'"{name}" has been deleted.')
    return redirect('food_list')


@login_required
def import_csv(request):
    """Import food data from CSV"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                import pandas as pd
                df = pd.read_csv(csv_file)

                created = 0
                skipped = 0

                def guess_category(name):
                    name_lower = name.lower()
                    if 'cheese' in name_lower or 'milk' in name_lower:
                        return 'dairy'
                    elif 'chicken' in name_lower or 'beef' in name_lower or 'pork' in name_lower:
                        return 'meat'
                    elif 'fish' in name_lower or 'salmon' in name_lower or 'tuna' in name_lower:
                        return 'seafood'
                    elif 'apple' in name_lower or 'banana' in name_lower or 'fruit' in name_lower:
                        return 'fruits'
                    elif 'rice' in name_lower or 'pasta' in name_lower or 'bread' in name_lower:
                        return 'grains'
                    elif 'pizza' in name_lower or 'burger' in name_lower or 'sandwich' in name_lower:
                        return 'snacks'
                    else:
                        return 'other'

                for _, row in df.iterrows():
                    name = row.get('food')
                    if pd.isna(name):
                        continue
                    name = str(name).strip()

                    if FoodItem.objects.filter(name=name).exists():
                        skipped += 1
                        continue

                    calories = float(row.get('Caloric Value', 0)) if pd.notna(row.get('Caloric Value')) else 0
                    fat = float(row.get('Fat', 0)) if pd.notna(row.get('Fat')) else 0
                    carbs = float(row.get('Carbohydrates', 0)) if pd.notna(row.get('Carbohydrates')) else 0
                    protein = float(row.get('Protein', 0)) if pd.notna(row.get('Protein')) else 0
                    fiber = float(row.get('Dietary Fiber', 0)) if pd.notna(row.get('Dietary Fiber')) else 0
                    sugar = float(row.get('Sugars', 0)) if pd.notna(row.get('Sugars')) else 0

                    FoodItem.objects.create(
                        name=name,
                        category=guess_category(name),
                        calories=calories,
                        protein=protein,
                        carbs=carbs,
                        fat=fat,
                        fiber=fiber,
                        sugar=sugar,
                    )
                    created += 1

                messages.success(request, f'Import completed! Added {created} items, skipped {skipped} items.')
                return redirect('food_list')

            except Exception as e:
                messages.error(request, f'Import failed: {str(e)}')
    else:
        form = CSVUploadForm()

    return render(request, 'calculator/import_csv.html', {'form': form})


# ============ Nutrition Calculation ============
@csrf_exempt
def calculate_nutrition(request):
    """Calculate nutrition (AJAX request)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])

        total_weight = 0
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        total_sugar = 0

        details = []

        for item in items:
            food_id = item.get('id')
            weight = float(item.get('weight', 0))

            if weight > 0:
                try:
                    food = FoodItem.objects.get(id=food_id)
                    factor = weight / 100

                    calories = food.calories * factor
                    protein = food.protein * factor
                    carbs = food.carbs * factor
                    fat = food.fat * factor

                    total_weight += weight
                    total_calories += calories
                    total_protein += protein
                    total_carbs += carbs
                    total_fat += fat
                    total_fiber += food.fiber * factor
                    total_sugar += food.sugar * factor

                    details.append({
                        'id': food.id,
                        'name': food.name,
                        'weight': weight,
                        'calories': round(calories, 1),
                        'protein': round(protein, 1),
                        'carbs': round(carbs, 1),
                        'fat': round(fat, 1),
                    })
                except FoodItem.DoesNotExist:
                    pass

        result = {
            'success': True,
            'total_weight': round(total_weight, 1),
            'total_calories': round(total_calories, 1),
            'total_protein': round(total_protein, 1),
            'total_carbs': round(total_carbs, 1),
            'total_fat': round(total_fat, 1),
            'total_fiber': round(total_fiber, 1),
            'total_sugar': round(total_sugar, 1),
            'details': details,
        }

        # Save to history (if user is logged in)
        if request.user.is_authenticated and details:
            CalculationHistory.objects.create(
                user=request.user,
                name=f"Meal on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
                items=json.dumps(details),
                total_weight=total_weight,
                total_calories=total_calories,
                total_protein=total_protein,
                total_carbs=total_carbs,
                total_fat=total_fat,
            )

        return JsonResponse(result)

    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def history_list(request):
    """Calculation history"""
    history = CalculationHistory.objects.filter(user=request.user)
    return render(request, 'calculator/history.html', {'history': history})


@login_required
def history_detail(request, pk):
    """History detail"""
    record = get_object_or_404(CalculationHistory, pk=pk, user=request.user)
    items = json.loads(record.items)
    return render(request, 'calculator/history_detail.html', {'record': record, 'items': items})


# ============ API ============
def search_foods(request):
    """Search foods (AJAX)"""
    query = request.GET.get('q', '')
    if len(query) >= 1:
        foods = FoodItem.objects.filter(name__icontains=query)[:20]
        data = [{'id': f.id, 'name': f.name, 'calories': f.calories, 'category': f.get_category_display()} for f in foods]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
