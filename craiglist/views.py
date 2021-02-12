from django.shortcuts import render
import requests
from requests.compat import quote_plus
from . import models
from bs4 import BeautifulSoup

# Create your views here.
BASE_URL= 'https://delhi.craigslist.org/d/services/search/?query={}'
IMAGE_URL= 'https://images.craigslist.org/{}_300x300.jpg'

def index(req):
    return (render(req,'base.html'))

def search(req):
    search = req.POST.get('search')
    models.Search.objects.create(search=search)
    url=BASE_URL.format(quote_plus(search))
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, features='html.parser')
    posting = soup.find_all('li',{'class':'result-row'})
    final_posting = []
    for post in posting:
        title = post.find(class_='result-title').text
        url=post.find('a').get('href')
        if post.find(class_='result-pice'):
            price=post.find(class_='result-price').text
        else:
            price = 'NA'

        if post.find(class_='result-image').get('data-ids'):
            image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            image_url=IMAGE_URL.format(image_id)
            print(image_url)    
        else:
            image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((title,url,price,image_url))

    context ={'search':search,'final_posting':final_posting,}
    
    return render(req,'craiglist/new_search.html',context)
