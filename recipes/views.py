from django.http import HttpResponse
from .models import Ingredient

def calculate_calorie(request, id):
    ingredient = Ingredient.objects.get(id=id)

    weight = request.GET.get('weight', 100)
    try:
        weight = float(weight)
    except:
        weight = 100

    total = ingredient.calories * weight / 100

    return HttpResponse(f"""
        <h3>{ingredient.name}</h3>
        每100g热量：{ingredient.calories} 千卡<br>
        食用重量：{weight} 克<br>
        <h2 style="color:red">总热量：{total:.2f} 千卡</h2>
        <br>
        使用示例：?weight=150
    """)