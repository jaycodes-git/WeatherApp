# from django.shortcuts import render
# from django.http import HttpResponse


# def get_html_content(city):
#     import requests
#     USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
#     LANGUAGE = "en-US,en;q=0.5"
#     session = requests.Session()
#     session.headers['User-Agent'] = USER_AGENT
#     session.headers['Accept-Language'] = LANGUAGE
#     session.headers['Content-Language'] = LANGUAGE
#     city = city.replace(' ', '+')
#     html_content = session.get(f'https://www.google.com/search?client=firefox-b-d&q=weather+{city}').text
#     print(html_content)
#     return html_content


# def home(request):
#     if request.method == "GET":
#         city = request.GET.get('city')
#         html_content = get_html_content(city)
#         from bs4 import BeautifulSoup
#         soup = BeautifulSoup(html_content, 'html.parser')
#         region = dict()
#         result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
#         # print(region)
#         return render(request, 'basic.html')


import urllib.request
import json
from django.shortcuts import render


def home(request):

    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(' ', '+')

        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        city + '&units=metric&appid=a8f8eb7cb2e020ef148f69e9e8e40c2f').read()
        
        list_of_data = json.loads(source)

        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ', '
            + str(list_of_data['coord']['lat']),

            "temp": str(list_of_data['main']['temp']) + ' °C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            'icon': list_of_data['weather'][0]['icon'],
        }

    else:
        data = {}

    return render(request, 'basic.html', data)