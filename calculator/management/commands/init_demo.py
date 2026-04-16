from django.core.management.base import BaseCommand
from calculator.models import FoodItem
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Import food data from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
            return
        
        self.stdout.write(f'Reading CSV file: {csv_file}')
        
        try:
            df = pd.read_csv(csv_file)
            self.stdout.write(f'Found {len(df)} rows')
            self.stdout.write(f'Columns: {list(df.columns)}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading CSV: {e}'))
            return
        
        created = 0
        skipped = 0
        errors = 0
        
        # 定义分类映射（根据食物名称推断）
        category_mapping = {
            'cheese': 'dairy',
            'milk': 'dairy',
            'yogurt': 'dairy',
            'cream': 'dairy',
            'butter': 'dairy',
            'chicken': 'meat',
            'beef': 'meat',
            'pork': 'meat',
            'turkey': 'meat',
            'sausage': 'meat',
            'bacon': 'meat',
            'ham': 'meat',
            'fish': 'seafood',
            'salmon': 'seafood',
            'tuna': 'seafood',
            'shrimp': 'seafood',
            'crab': 'seafood',
            'oyster': 'seafood',
            'clam': 'seafood',
            'pizza': 'snacks',
            'burger': 'snacks',
            'sandwich': 'snacks',
            'taco': 'snacks',
            'burrito': 'snacks',
            'soup': 'other',
            'rice': 'grains',
            'pasta': 'grains',
            'noodle': 'grains',
            'bread': 'grains',
            'apple': 'fruits',
            'banana': 'fruits',
            'orange': 'fruits',
            'fruit': 'fruits',
            'vegetable': 'vegetables',
            'broccoli': 'vegetables',
            'spinach': 'vegetables',
            'potato': 'vegetables',
            'tomato': 'vegetables',
            'nut': 'nuts',
            'almond': 'nuts',
            'peanut': 'nuts',
            'chocolate': 'snacks',
            'cookie': 'snacks',
            'cake': 'snacks',
            'egg': 'dairy',
        }
        
        def guess_category(name):
            """根据名称推断分类"""
            name_lower = name.lower()
            for keyword, category in category_mapping.items():
                if keyword in name_lower:
                    return category
            return 'other'
        
        for idx, row in df.iterrows():
            try:
                # 获取食物名称
                name = row.get('food')
                if pd.isna(name) or not name:
                    skipped += 1
                    continue
                
                name = str(name).strip()
                
                # 检查是否已存在
                if FoodItem.objects.filter(name=name).exists():
                    skipped += 1
                    if skipped % 100 == 0:
                        self.stdout.write(f'  Skipped {skipped} existing items...')
                    continue
                
                # 获取营养值，处理缺失值
                calories = row.get('Caloric Value', 0)
                fat = row.get('Fat', 0)
                carbs = row.get('Carbohydrates', 0)
                protein = row.get('Protein', 0)
                fiber = row.get('Dietary Fiber', 0)
                sugar = row.get('Sugars', 0)
                
                # 转换为 float，处理 NaN
                calories = float(calories) if pd.notna(calories) else 0
                fat = float(fat) if pd.notna(fat) else 0
                carbs = float(carbs) if pd.notna(carbs) else 0
                protein = float(protein) if pd.notna(protein) else 0
                fiber = float(fiber) if pd.notna(fiber) else 0
                sugar = float(sugar) if pd.notna(sugar) else 0
                
                # 推断分类
                category = guess_category(name)
                
                # 创建食物记录
                FoodItem.objects.create(
                    name=name,
                    category=category,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                    fiber=fiber,
                    sugar=sugar,
                )
                
                created += 1
                
                if created % 50 == 0:
                    self.stdout.write(f'  Created {created} items... (last: {name})')
                    
            except Exception as e:
                errors += 1
                if errors <= 10:
                    self.stdout.write(self.style.WARNING(f'  Error on row {idx}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Import completed!\n'
            f'   Created: {created}\n'
            f'   Skipped (already exist): {skipped}\n'
            f'   Errors: {errors}'
        ))
        
        total = FoodItem.objects.count()
        self.stdout.write(f'\n📊 Total food items in database: {total}')
