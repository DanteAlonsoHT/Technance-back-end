from rest_framework import viewsets, status #, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.template.loader import get_template
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import clone_request
from django.contrib.auth.hashers import check_password
#from user_messages.return_message_error_if_exist import return_message_error_if_exist_from_user
import requests
import json
import numpy as np
import datetime
import random
from django.conf import settings
import re
from pathlib import Path
import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()


def random_string():
  random_list = [
    "Lo siento, no entiendo...",
    "Puedes repetir tu pregunta?",
    "Puedes explicarlo de otra forma?"
  ]

  list_count = len(random_list)
  random_item = random.randrange(list_count)

  return random_list[random_item]

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Bot cargado exitosamente!")
        return json.load(bot_responses)

BASE_DIR = Path(__file__).resolve().parent.parent
# Store JSON data
response_data = load_json(f'{BASE_DIR}/api/bot.json')


def get_response(input_string):
    # Check if input is empty
    if input_string == "":
        return "Holaa, por favor escribe algo, no muerdo :("

    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_string()
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
      try:
        if not request.data['image_profile']:
          request.data['image_profile'] = ''
        serializer = UserSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
          serializer.save()
          response = { 'ok': { 'message': 'OK', 'data': 'NOT_AVAILABLE_YET' }}
          print(response)
        
        return Response(response)
      except:
        if serializer.errors:
          data_response = { 'error': { 'message': 'INVALID_DATA', 'data': serializer.errors }}
          return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        else:
          data_response = { 'error': { 'message': 'SERVER_ERROR', 'data': [] }}
          return Response(data_response, status=status.HTTP_400_BAD_REQUEST)  

    def update(self, request, pk=None, *args, **kwargs):
      try:
        copy = request.data.copy()
        current_user = User.objects.filter(id=pk)[0]
        if not request.data['password']:
          copy['password'] = current_user.password
        else:
          copy['password'] = make_password(copy['password'])
        if not request.data['image_profile']:
          del copy['image_profile']
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = UserSerializer(instance, data=copy, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance is None:
          lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
          lookup_value = self.kwargs[lookup_url_kwarg]
          extra_kwargs = {self.lookup_field: lookup_value}
          serializer.save(**extra_kwargs)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.save()
        return Response(serializer.data)
      except:
        try:
          data_response = { 'error': { 'message': 'INVALID_DATA', 'data': serializer.errors }}
          return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        except:
          data_response = { 'error': { 'message': 'SERVER_ERROR', 'data': [] }}
          return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                raise

    @action(detail=False, methods=['post'])
    def get_user_data_from_auth(self, request, pk=None):
        try:
            email = request.data['email']
            password = request.data['password']
            if not User.objects.filter(email=email):
                data_response = { 'error': { 'message': 'EMAIL_NOT_FOUND' }}
                return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            password_encoded = user.password
            if check_password(password, password_encoded):
                if not user.is_active:
                    response = { 'error': { 'message': 'USER_NOT_ACTIVE' }}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                token = Token.objects.get(user_id=user.id).key
                queryset = User.objects.get(id=user.id)

                serializer = UserSerializer(queryset, many=False)
                response = {
                    'authToken': token,
                    'userDetails': serializer.data,
                }
                return Response(response)

            data_response = { 'error': { 'message': 'INVALID_PASSWORD' }}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        except:
            data_response = { 'error': { 'message': 'SERVER_ERROR' }}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_password(self, request, pk=None):
        try:
            current_user_id = Token.objects.filter(key=request.headers['Authorization'].replace('Token ', ''))[0].user_id
            queryset = User.objects.filter(id=current_user_id)
            queryset.password = make_password(request.data['password'])
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            data_response = { 'error': 'User was not selected yet or Server error was found.' }
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def chat_bot(self, request, pk=None):
      try:
        user_message = request.data['message']
        bot_reponse = get_response(user_message)
        return Response(bot_reponse)
      except:
        data_response = { 'error': 'Server error was found.' }
        return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
