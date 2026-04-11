import os
import django
import pandas as pd
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_api.settings')
django.setup()

from recipes.models import Ingredient

def run():
    print("开始导入数据...")
    root = Path(__file__).parent
    files = list(root.glob("FOOD-DATA-GROUP*.csv"))

    for f in files:
        try:
            df = pd.read_csv(f, encoding='utf-8-sig')
            print(f"导入：{f.name}")

            for _, row in df.iterrows():
                name = str(row['food']).strip()
                cal = float(row['Caloric Value']) if pd.notna(row['Caloric Value']) else 0
                fat = float(row['Fat']) if pd.notna(row['Fat']) else 0
                pro = float(row['Protein']) if pd.notna(row['Protein']) else 0
                carb = float(row['Carbohydrates']) if pd.notna(row['Carbohydrates']) else 0

                if not Ingredient.objects.filter(name=name).exists():
                    Ingredient.objects.create(
                        name=name,
                        calories=cal,
                        fat=fat,
                        protein=pro,
                        carbs=carb
                    )
        except Exception as e:
            print(f"跳过：{f.name} | 错误：{e}")

    print("✅ 全部导入完成！")

if __name__ == '__main__':
    run()