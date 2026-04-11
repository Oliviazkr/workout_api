from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="未分类")
    calories = models.FloatField(help_text="每100克的卡路里")
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    # 计算总卡路里
    def calculate_total_calories(self, weight):
        return (self.calories * weight) / 100

    def __str__(self):
        return self.name