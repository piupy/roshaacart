from math import ceil
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum

MERCHANT_KEY = 'TkCZbSnD7yAI0@ma'

def index(request):
    allProducts = []
    catProducts = Product.objects.values('category', 'id')
    categories = {item['category'] for item in catProducts}
    for cat in categories:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil(n / 4 - n // 4)
        allProducts.append([prod, range(1, nSlides), n])

    params = {
        'allProducts': allProducts
    }
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        isPOSTRequest = True

    elif request.method == "GET":
        isPOSTRequest = False

    return render(request, 'shop/contact.html',{'isPOSTRequest' : isPOSTRequest})

def product(request,myid):
    prod = Product.objects.filter(id=myid)[0]
    return render(request, 'shop/product.html',{ 'prod' : prod})


def checkout(request):

    if request.method == "POST":
        items_json = request.POST.get('itemsJson')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address1') + ' ' + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        order = Order(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        id = order.order_id
        isOrderPlaced = True
        update = OrderUpdate(order_id=id,update_desc='Your order has been placed.')
        update.save()

        param_dict = {
            'MID' : 'syRCYc29258543697479',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest',
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{ 'param_dict' : param_dict })

    elif request.method == "GET":
        isOrderPlaced = False
        id = None        
    return render(request, 'shop/checkout.html',{ 'isOrderPlaced' : isOrderPlaced, 'id' : id })


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId')
        email = request.POST.get('email')
        
        try:
            orderToBeSearched = Order.objects.filter(order_id=orderId,email=email)
            if len(orderToBeSearched) > 0:
                updatesFound = OrderUpdate.objects.filter(order_id=orderId)
                updatesToBeShown = []
                for update in updatesFound:
                    updatesToBeShown.append({ 'text' : update.update_desc , 'time' : update.timestamp })
                response = json.dumps([updatesToBeShown,orderToBeSearched[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')

        except Exception as e:
            return HttpResponse('{}')

    return render(request,'shop/tracker.html')



@csrf_exempt
def handlerequest(request):
    # Paytm will send POST request to this URL
    if request.method == 'POST':
        form = request.POST
        response_dict = {}
        for key in form.keys():
            response_dict[key] = form[key]
            if key == 'CHECKSUMHASH':
                checksum = form[key]
        verified = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
        if verified:
            if response_dict['RESPCODE'] == '01':
                print('Order Successful...')
            else:
                print('Sorry! Order was not successful because ' + response_dict['RESPMSG'])
        return render(request,'shop/paymentstatus.html',{ 'response_dict' : response_dict })

    else:
        return HttpResponse("Something went wrong...")


def searchMatch(query,item):
    query = query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    if request.method == 'POST':
        allProducts = []
        query = request.POST.get('search')
        catProducts = Product.objects.values('category', 'id')
        categories = {item['category'] for item in catProducts}
        for cat in categories:
            prodtemp = Product.objects.filter(category=cat)
            prod = [item for item in prodtemp if searchMatch(query,item)]
            n = len(prod)
            nSlides = n // 4 + ceil(n / 4 - n // 4)
            if n != 0 :
                allProducts.append([prod, range(1, nSlides), n])

        params = {
            'allProducts': allProducts,
            'msg' : ''
        }
        if len(allProducts) == 0 :
            params['msg'] = 'Please make sure to enter relevant query'
        return render(request, 'shop/search.html', params)

    else:
        allProducts = []
        catProducts = Product.objects.values('category', 'id')
        categories = {item['category'] for item in catProducts}
        for cat in categories:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil(n / 4 - n // 4)
            allProducts.append([prod, range(1, nSlides), n])
        params = {
            'allProducts': allProducts
        }
        return render(request, 'shop/index.html', params)


