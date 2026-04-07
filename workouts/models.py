from django.db import models

# Create your models here.
# 运动打卡数据模型（满足CRUD，关联数据库）
class Workout(models.Model):
    sport_type = models.CharField(max_length=100, verbose_name="运动类型")  # 跑步/瑜伽等
    duration = models.IntegerField(verbose_name="运动时长(分钟)")          # 数字型，必填
    checkin_date = models.DateField(verbose_name="打卡日期")               # 日期型，必填
    notes = models.TextField(blank=True, null=True, verbose_name="运动备注")# 可选，文本型

    def __str__(self):
        # 后台显示：运动类型 + 打卡日期，方便查看
        return f"{self.sport_type} - {self.checkin_date}"
