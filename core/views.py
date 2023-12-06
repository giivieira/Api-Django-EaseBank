from django.shortcuts import render
from rest_framework import viewsets
from models import *
from rest_framework import serializers
from rest_framework_simplejwt import authentication as authenticationJWT
from user.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

