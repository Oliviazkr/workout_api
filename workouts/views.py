from django.shortcuts import render

from rest_framework import viewsets
from .models import Workout
from .serializers import WorkoutSerializer

# DRF的ViewSet自动生成完整CRUD，不用自己写每个接口的逻辑
class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()  # 查所有打卡记录
    serializer_class = WorkoutSerializer  # 关联JSON序列化器
