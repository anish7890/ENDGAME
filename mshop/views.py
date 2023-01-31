from django.http import HttpResponse
from django.shortcuts import render
from .models import Products, Contact, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'mshop/index.html', params)

def about(request):
    return render(request, 'mshop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email= request.POST.get('email', '')
        phone= request.POST.get('phone', '')
        desc= request.POST.get('desc', '')
        # print(name,email,phone,desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'mshop/contact.html',{'thank':thank})

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')


        try:
            order = Orders.objects.filter(order_id=orderid, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse("{}")

    return render(request, 'mshop/tracker.html')

def search(request):
    return render(request, 'mshop/search.html')
def productview(request, myid):
    #Fetch the product using id
    product = Products.objects.filter(id=myid)
    print(product)
    return render(request, 'mshop/prodview.html', {'product':product[0]})
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        curlocation = request.POST.get('curlocation', '')
        hostel = request.POST.get('hostel', '')
        room = request.POST.get('room', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, amount=amount, email=email, curlocation=curlocation, hostel=hostel, room=room, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'mshop/checkout.html',{'thank':thank, 'id':id})
    return render(request, 'mshop/checkout.html')


