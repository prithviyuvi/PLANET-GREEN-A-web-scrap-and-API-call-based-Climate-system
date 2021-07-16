from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Carbon, Planting
import urllib
import bs4 as bs
import re

from django.shortcuts import render, redirect
from .search import google, duck, bing, givewater

def home1(request):
    return (render(request, "home.html"))

def home2(request):
    return (render(request, "home2.html"))

def carbons(request):
    ok=val()
    return (render(request, "carbon.html", {"name": ok}))

def carbonresult(request):
    memberofhouses = request.POST['memberofhouses']
    sizeofhome = request.POST['sizeofhome']
    food = request.POST['food']
    household = request.POST['household']
    garbage = request.POST['garbage']
    recycle = request.POST['recycle']
    car = request.POST['car']
    flight = request.POST['flight']
    public = request.POST['public']
    total = int(memberofhouses) + int(sizeofhome) + int(food) + int(household) + int(garbage) + int(recycle) + int(car) + int(flight) + int(public)
    num = val()
    if Carbon.objects.filter(userid=num).exists():
        obj = Carbon.objects.get(userid=num)
        obj.carbonfootprint_score = total
        obj.save()
    else:
        obj = Carbon(userid = num , carbonfootprint_score = total )
        obj.save()
    return (render(request, "carbonresult.html", {'total': total}))

val  = None

def logins(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            global val
            def val():
                one_entry = User.objects.get(username=username)
                return one_entry.id


            return redirect('carbons')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('logins')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password2 == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                #return redirect('register')
                return render(request, 'login2.html')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                #return redirect('register')
                return render(request, 'login2.html')
            user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password1)
            user.save()
            return redirect('logins')
        else:
            messages.info(request, 'password does not match')
            #return redirect('register')
            return render(request, 'login2.html')
    else:
        return render(request, 'login.html')

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(email=email).exists():
            if password2 == password1:
                obj = User.objects.get(email=email)
                obj.set_password(password1)
                obj.save()
                messages.info(request, 'password reset successfully')
                return redirect('logins')
            else:
                messages.info(request,'Password not match')
        else:
            messages.info(request, 'Email not exists')
            return redirect('forgetpassword')

    return render(request,'forgetpassword.html')

# article web scrapping
def articles(request):
    # *****************  source1   ********************
    source = urllib.request.urlopen('https://simple.wikipedia.org/wiki/Global_warming').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    text = []
    for paragraph in soup.find_all('p'):
        text.append(paragraph.text)
    tex = []
    for t in text:
        t = re.sub(r'\[[0-9]*\]', ' ', t)
        tex.append(t)
    # source 1 image scrapping
    list = []
    for item in soup.find_all('img'):
        list.append(item['src'])
    text.clear()
    # *****************  source2  ********************
    source2 = urllib.request.urlopen('https://en.wikipedia.org/wiki/Carbon_footprint').read()
    soup2 = bs.BeautifulSoup(source2, 'lxml')
    text1 = []
    for paragraph in soup2.find_all('p'):
        text1.append(paragraph.text)
    tex1 = []
    for t in text1:
        t = re.sub(r'\[[0-9]*\]', ' ', t)
        tex1.append(t)
    text1.clear()

    # *****************  source3  ********************

    source3 = urllib.request.urlopen('https://climate.nasa.gov/effects/').read()
    soup3 = bs.BeautifulSoup(source3, 'lxml')
    text2 = []
    for paragraph in soup3.find_all('p'):
        text2.append(paragraph.text)

    tex2 = []
    for t in text2:
        t = re.sub(r'\[[0-9]*\]', ' ', t)
        tex2.append(t)

    text2.clear()

    return render(request, 'articles.html',
                  {'text': tex, 'text2': tex1[:len(tex1) - 30], 'text3': tex2[2:len(tex2) - 20], 'list2': list[2],
                   'list3': list[3]})


# -------------search engine---------


def searchhome(request):
    return render(request, 'serachhome.html')


def searchresults(request):
    if request.method == "POST":
        result = request.POST.get('search')
        google_link, google_text = google(result)
        google_data = zip(google_link, google_text)
        duck_link, duck_text = duck(result)
        duck_data = zip(duck_link, duck_text)
        bing_link, bing_text = bing(result)
        bing_data = zip(bing_link, bing_text)
        givewater_link, givewater_text = givewater(result)
        givewater_data = zip(givewater_link, givewater_text)

        if result == '':
            return redirect('searchhome')
        else:
            return render(request, 'searchresults.html',
                          {'search': result, 'google': google_data, 'duck': duck_data, 'bing': bing_data,
                           'givewater': givewater_data})


from .forms import UserUpdateForm

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context={'u_form': u_form}
    return render(request, 'profile.html',context)

def logout(request):
    auth.logout(request)
    return redirect('/')

#*******************************************************************weather***************************************************************
from django.shortcuts import render, redirect
import requests
from .models import Citys
from .forms import CityForm
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=bbf2d198ce6cfac726546f54e79c50b2'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = Citys.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
    form = CityForm()
    cities = Citys.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'humidity': r['main']['humidity'],
        }
        weather_data.append(city_weather)
    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather.html', context)


def delete_city(request, city_name):
    Citys.objects.get(name=city_name).delete()

    return redirect('weather')

#**************************

def community(request):
    num = val()
    if request.method == 'POST':
        one_entry = User.objects.get(id=num)
        if Planting.objects.filter(email=one_entry.email).exists():
            pass
            return redirect('saplinghome')
        else:
            one_entry = Planting(name=one_entry.first_name,email=one_entry.email)
            one_entry.save()
            return redirect('saplinghome')
    return render(request,'sappling1.html')

from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
# Create your views here.
def saplinghome(request):
    return render(request, 'saplinghome.html')
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):

    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def redir(request):
    return redirect('../saplinghome')
