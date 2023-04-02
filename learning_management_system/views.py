from django.shortcuts import redirect,render
from LmsApp.models import Categories,Course,Level,Video,UserCourse,Payments
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from time import time
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .settings import *
client = razorpay.Client(auth=(KEY_ID,KRY_SECRET))

# data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
# payment = client.order.create(data=data)


def base(request):
    return render(request,'base.html')
def Home(request):
    category=Categories.objects.all().order_by('id')[0:5]
    course=Course.objects.filter(status='PUBLISH').order_by('-id')
    print("raaw-->",category)
    all_category={
        "category":category,
        "course":course,
    }
    return render(request,'main/home.html',context=all_category)

def SingleCourse(request):
    category=Categories.get_all_category(Categories)
    courses=Course.objects.filter(status='PUBLISH').order_by('id')
    level=Level.objects.all()
    allcourses=Course.objects.all()
    free_course_count=Course.objects.filter(price=0).count()
    paid_course=Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        'courses':courses,
        'level':level,
        'Allcourses':allcourses,
        'free_course_count':free_course_count,
        'paid_course':paid_course
    }
    return render(request,'main/single_course.html',context)

def ContactUs(request):
    category=Categories.objects.all().order_by('id')
    
    print("raaw-->",category)
    all_category={
        "category":category,
        
    }
    return render(request,'main/contact_us.html',context=all_category)

def AboutUs(request):
    category=Categories.objects.all().order_by('id')
   
    print("raaw-->",category)
    all_category={
        "category":category,
        
    }
    return render(request,'main/about_us.html',context=all_category)




def filter_data(request):
    #category=Categories.objects.all().order_by('id')
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price,categories,level)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
   
    
    context = {
        'course':course,
        
    }
    return render(request,'search/search_filter.html',context)
from django.db.models import Sum
def course_detail(request,slug):
   
    category=Categories.objects.all().order_by('id')
    time_dura=Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duratiom'))


    course_id=Course.objects.get(slug = slug)
    id=Course.objects.only('id').get(slug=slug).id
    print(f"id is {id}")
    try:
        check_enroll=UserCourse(user=request.user,course = id)
        print("xyzxyz",check_enroll)
        
    except:
        check_enroll=None
        print("user doest not exist",check_enroll)
    finally:
       pass

        
   
    
    Ncourse=Course.objects.all().filter(slug=slug)
    print(f"what you learn{Ncourse}")
    if Ncourse.exists():
        Ncourse.first()
    else:
        return redirect('404')
    print(f"i am tester {Ncourse}")
    context={
        'course':Ncourse,
        'category':category,
        'time_duration':time_dura,
        'check_enroll':check_enroll,
        #'time_duration':time_dura['sum']  #this is working
    }
    print(f"i am tester {context}")
    return render(request,"course_detail_slug/course_overview_detail.html",context)




def page_not_found(request):
     
    category=Categories.objects.all().order_by('id')
   
    context={
      
        'category':category
    }
    return render(request,"Error/404.html",context)

def course_checkout(request,slug):
    order=None
    course=Course.objects.get(slug=slug)
    action=request.GET.get('action')
    if course.price==0:
        course=UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        print("{free courses save successfully}")
        messages.success(request,"Course are successfully enrolled")
        return redirect('my_course')
    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country =   request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
           
            order_comments = request.POST.get('order_comments')
            print(first_name,last_name,country,address_1,address_2,city,state,postcode,phone,email,order_comments)
            amount = course.price + 100
            currency = "INR"
            notes = {
                "name": f"{first_name} {last_name}",
                "country":country,
                "address_1":f" {address_1} {address_2}",
              
                "city":city,
                "state":state,
                "postcode":postcode,
                "phone":phone,
                "email":email,
                "order_comments":order_comments
            }

            receipt=f"Solver rahule {int(time())} "
            order = client.order.create(
                { 
                    "receipt":receipt,
                    "notes": notes,
                    "amount": amount,
                    "currency":currency

                }
            )
            payment = Payments(course=course,user = request.user,order_id=order.get('id'))
            payment.save()
    
    context={
        "course":course,
        "order":order
    }
    return render(request,"checkout_course/checkout_shop_courcse.html",context)

def MY_COURSE(request):
    course=UserCourse.objects.filter(user=request.user)
    context={
        "course":course
    }
    key="rzp_test_VlJ2VPZq1oJ059"
    secret_key="n9nopiRaZfrSn5ktb5At9r07"

    return render(request,'course/my_course.html',context)

"""
Rozar verificatin payments methods

"""


@csrf_exempt
def VerifyPayment(request):
    pass
            # only accept POST request.
    try:
        
        data=request.POST
        print(data)
        try:
           
            # get the required parameters from post request.
            client.utility.verify_payment_signature(data)
            # payment_id = request.POST.get('razorpay_payment_id', '')
            # razorpay_order_id = request.POST.get('razorpay_order_id', '')
            # signature = request.POST.get('razorpay_signature', '')
            razorpay_order_id = request.data['razorpay_order_id']
            rozarpay_payment_id = request.data['razorpay_payment_id']
           
            signature = request.data['razorpay_signature']
            # params_dict = {
            #     'razorpay_order_id': razorpay_order_id,
            #     'razorpay_payment_id': rozarpay_payment_id,
            #     'razorpay_signature': signature
            # }
            # client.utility.verify_payment_signature(params_dict)
            payment=Payments.objects.get(order_id = razorpay_order_id)
            payment.payment_id = rozarpay_payment_id
            payment.status=True

            usercourse = UserCourse(
                user = payment.user,
                course = payment.course

            )
            usercourse.save()
            payment.user_course = usercourse
            payment.save()
            print("courses are successfully enrolled")

            context = {
                "data":data,
                "payment":payment

            }
 
            
            # render success page on successful caputre of payment
            return render(request, 'verify_payment/success.html')
        except:
            print("i am exceptin post")
            # if there is an error while capturing payment.
            
            return render(request, 'verify_payment/fail.html')
    except:
          return render(request, 'verify_payment/fail.html')
        


  
