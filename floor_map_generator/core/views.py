from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import ContactForm, FloorMapForm, CustomUserCreationForm
from .models import FloorMap, CustomUser
from .decorators import admin_required
from django.http import JsonResponse
import json
import socket
import requests
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required


@csrf_exempt  # If you are not using CSRF token in AJAX
def generate_map(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)  # This is the part you're having trouble with
            
            rooms = data.get('rooms')
            bathroom = data.get('bathroom')
            kitchen = data.get('kitchen')

            # Ensure that all fields are provided
            if not rooms or not bathroom or not kitchen:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Target server and port
            url = 'http://10.22.2.189:5000'

            # Prepare the data to be sent to the server
            data_to_send = {
                'rooms': rooms,
                'bathroom': bathroom,
                'kitchen': kitchen
            }

            # Sending the POST request with the JSON data
            response = requests.post(url, json=data_to_send)

            if response.status_code == 200:
                # Wait for 60 seconds before fetching the data
                time.sleep(60)

                # Send a GET request to fetch the exported data (URLs)
                fetch_response = requests.get(url)

                if fetch_response.status_code == 200:
                    # Assuming the response is a JSON list of URLs
                    image_urls = fetch_response.json()
                    return JsonResponse({'image_urls': image_urls})
                else:
                    return JsonResponse({'error': 'Failed to fetch data from server'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to send data to the server'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
def generate(request):
    if request.method == 'POST':
        form = FloorMapForm(request.POST)
        if form.is_valid():
            floor_map = form.save(commit=False)
            floor_map.user = request.user
            floor_map.save()
            floor_map.image = 'floor_maps/placeholder.png'
            floor_map.save()
            return redirect('view_floor_map', floor_map_id=floor_map.id)
    else:
        form = FloorMapForm()
    return render(request, 'generate.html', {'form': form})

@login_required
def view_floor_map(request, floor_map_id):
    # Fetch the FloorMap instance by its ID
    floor_map = FloorMap.objects.get(id=floor_map_id)
    
    # Assuming you want to fetch or generate four images for the floor map
    # Replace the image URLs with actual ones, or generate them dynamically
    image_urls = [
         "https://res.cloudinary.com/dq1zewmkm/image/upload/v1733575371/file_euxgva.png",
         "https://res.cloudinary.com/dq1zewmkm/image/upload/v1733575371/file_euxgva.png",
         "https://res.cloudinary.com/dq1zewmkm/image/upload/v1733575371/file_euxgva.png",
         "https://res.cloudinary.com/dq1zewmkm/image/upload/v1733575371/file_euxgv.png",
    ]
    
    return render(request, 'view_floor_map.html', {
        'floor_map': floor_map,
        'image_urls': image_urls
    })

@login_required
def dashboard(request):
    floor_maps = FloorMap.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'floor_maps': floor_maps})

@admin_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    floor_maps = FloorMap.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'floor_maps': floor_maps})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    # Disable help text for specific fields
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})