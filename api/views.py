from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Shorts
# Create your views here.

User = get_user_model()

class RegisterView(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        user = User.objects.create(username=username,password=password,email=email)
        user.save()
        return Response({
            "status":"Account Successfully Created",
            "status_code":200,
            "user_id":user.id
        })

class LoginView(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username,password=password).exists():
            return Response({
                "status": "Incorrect username/password provided. Please retry",
                "status_code":401
            })
        
        user = User.objects.filter(username=username,password=password).first()
        if password!=user.password:
            return Response({
                "status": "Incorrect username/password provided. Please retry",
                "status_code":401
            })
        
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            "status": "Login successful",
            "status_code": 200,
            "user_id": user.id,
            "access_token": token.key
        })
    
class CreateShortsView(APIView):
    def post(self,request):
        data = request.data
        category = data.get('category')
        title = data.get('title')
        author = data.get('author')
        publish_date = data.get('publish_date')
        content = data.get('content')
        actual_content_link = data.get('actual_content_link')
        image = data.get('image')
        short = Shorts.objects.create(category=category,title=title,author=author,publish_date=publish_date,content=content,actual_content_link=actual_content_link,image=image)
        short.save()
        return Response({
            "message": "Short added successfully",
            "short_id": short.id,
            "status_code": 200
        })
    

class GetShortsFeed(APIView):
    def get(self,request):
        shorts = Shorts.objects.all()
        short_list = []
        for short in shorts:
            short_list.append({
                "category": short.category,
                "title": short.title,
                "author": short.author,
                "publish_date": short.publish_date,
                "content": short.content,
                "actual_content_link": short.actual_content_link,
                "image": short.image,
                "votes":{
                    "upvotes": short.upvotes,
                    "downvotes": short.downvotes
                }
            })
        short_list = sorted(short_list,key= lambda x:x['publish_date'],reverse=True)
        short_list = sorted(short_list,key= lambda x:x['votes']['upvotes'],reverse=True)
        return Response({
            "data":short_list
        })
    
class SearchAndFilter(APIView):
    def get(self,request):
        params = request.query_params
        filters = params.get('filter')
        search = params.get('search')
        category = filters.get('category')
        upvote = filters.get('upvote')
        shorts = []
        if category and upvote:
            shorts = Shorts.objects.filter(category=category,upvotes__gte=upvote)
        elif category:
            shorts = Shorts.objects.filter(category=category)
        elif upvote:
            shorts = Shorts.objects.filter(upvotes__gte=upvote)
        search_results = []
        if search.get('title'):
            search_results = Shorts.objects.filter(title__icontains=search.get('title'))
        elif search.get('author'):
            search_results = Shorts.objects.filter(author__icontains=search.get('author'))
        final_results = list(set(shorts) & set(search_results))

        return Response({
            final_results
        })
        
            






        



