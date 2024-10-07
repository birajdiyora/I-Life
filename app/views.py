from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .models import *
from django.http import JsonResponse
from .forms import RegistrationForm,ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db.models import Count
import json
from django.template.loader import render_to_string
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import UploadedFile


def index(request):
    products = Product.objects.all().order_by('-id')[:3]
   
    context = {
        'products': products
    }
    return render(request, 'app/index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({'success': False, 'message': 'All fiels are required.'})

       
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email does not exist.'})

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_superuser: 
                auth_login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful.'})
            else:
                return JsonResponse({'success': False, 'message': 'Superuser accounts cannot log in through this form.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid password.'})

    return render(request,'app/login.html')

# def register(request):
#     return render(request,'app/register.html')

def about(request):
    return render(request,'app/about.html')

def contact(request):
    return render(request,'app/contact.html')

def service(request):
    return render(request,'app/service.html')

def show_product(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    print(product)
    context = {
        'product': product
    }
    
    return render(request, 'app/show_product.html', context)

def product(request):
    products = Product.objects.all()

    print("hello")
   
    context = {
        'products': products
    }   
    return render(request,'app/product.html',context)

def products_list(request):
    products = Product.objects.all()
    print("Hello india..............")
    # print(products)
    context = {
        'products': products
    }
    return render(request, 'app/product.html', context)

def sum_view(request):
    sum_result = None  
    products = Product.objects.all()
    if request.method == 'POST':
        print("Form submitted successfully")  
        
        entry1 = request.POST.get('entry1', None)
        entry2 = request.POST.get('entry2', None)

        print(f"Entry1: {entry1}, Entry2: {entry2}")  

        if entry1 is not None and entry2 is not None:
            try:
                entry1 = int(entry1)
                entry2 = int(entry2)
                sum_result = entry1 + entry2  
                print(f"Calculated Sum: {sum_result}")  
            except ValueError:
                print("Invalid input. Ensure both fields are numbers.")  
        
    context = {
        'sum': sum_result,
        'products':products
    }
    return render(request, 'app/product.html', context)

# def add_contact_detail(request):
#     if request.method == 'POST':
#         customer_name = request.POST.get('name')
#         contact_number = request.POST.get('phone')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         question = request.POST.get('description')

    
#         contact = ContactUs(
#             customer_name=customer_name,
#             contact_number=contact_number,
#             email=email,
#             subject=subject,
#             question=question
#         )
#         contact.save()
#     return render(request, 'app/contact.html')

def add_contact_detail(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        contact_number = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        question = request.POST.get('description')

        
        if not all([customer_name, contact_number, email, subject, question]):
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        try:
           
            contact = ContactUs(
                customer_name=customer_name,
                contact_number=contact_number,
                email=email,
                subject=subject,
                question=question
            )
            contact.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    return render(request, 'app/contact.html')

def add_inquiry(request):
    if request.method == 'POST':
        
        product_id = request.POST.get('product_id')
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')

        if not all([product_id,name, email, phone, description]):
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        
        inquiry = Inquiry(
            product_id=product_id,
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            description=description
        )
        inquiry.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# def register_view(request):
#     user = request.user
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             # Create a new user
#             print("valid...................................................")
#             user = User.objects.create_user(
#                 username=form.cleaned_data['email'],
#                 first_name=form.cleaned_data['first_name'],
#                 last_name=form.cleaned_data['last_name'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password']
#             )
#             # Log the user in
#             login(request, user)
#             return redirect('home')  # Redirect to the homepage or another page
#     else:
#         form = RegistrationForm()

#     return render(request, 'app/register.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)
        
        if password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Passwords do not match.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists.'}, status=400)

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()
        Profile.objects.get_or_create(user=user)

        return JsonResponse({'success': True, 'message': 'Registration successful.'})

    return render(request, 'app/register.html')

def logout(request):
    # print("in logout.................")
    # auth_logout(request,user)
    # return redirect('app/index.html') 
    if request.method == 'POST':
        print("in logout...............")
        auth_logout(request)
        return redirect('home')  
    return HttpResponse(status=405) 

def submit_feedback(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        description = request.POST.get('description')
        rating = request.POST.get('rating')

        if not description or not rating:
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        try:
            feedback = Feedback(
                user_id=user_id,
                username = username,
                description=description,
                rating=rating
            )
            feedback.save()
            return JsonResponse({'success': True, 'message': 'Feedback submitted successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)



# ------------------------------admin----------------------------------------------------------------------------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = authenticate(username = username,password = password)

        if user_obj.is_superuser is True:
            auth_login(request,user_obj)
            return redirect('dashboard') 
    return render(request,'app/admin/login.html')

def dashboard(request):
    
    inquiry_month_data = Inquiry.objects.values('created_at__month').annotate(count=Count('id')).order_by()
    imonths = [0] * 12  
    for data in inquiry_month_data:
        imonths[data['created_at__month'] - 1] = data['count']

   
    feedback_month_data = Feedback.objects.values('created_at__month').annotate(count=Count('id')).order_by()
    fmonths = [0] * 12  
    for data in feedback_month_data:
        fmonths[data['created_at__month'] - 1] = data['count']

    # # Combine the data into a dictionary and convert it to JSON
    # data = json.dumps([{
    #     'inquiry': imonths,
    #     'feedback': fmonths
    # }])
    total_users = User.objects.filter(is_superuser=False).count()  
    total_inquiries = Inquiry.objects.count()
    total_feedback = Feedback.objects.count()
    total_products = Product.objects.count()  

    data = json.dumps([{
        'inquiry': imonths,
        'feedback': fmonths
    }])

    context = {
        'data': data,
        'total_users': total_users,
        'total_inquiries': total_inquiries,
        'total_feedback': total_feedback,
        'total_products': total_products,
    }

    return render(request, 'app/admin/dashboard.html', context)

def user_list(request):
    users = User.objects.filter(is_superuser=False).all()
    return render(request, 'app/admin/user.html',{'users':users})

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        try:
            user.delete()
            return JsonResponse({'success': True, 'message': 'User deleted successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed to delete user.'}, status=500)
    return redirect('user_list')

def product_list(request):
    products = Product.objects.all()

    return render(request, 'app/admin/product/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    data = {
        'form': render_to_string('app/admin/product/edit.html', {'form': form, 'product': product}, request=request),
    }
    return JsonResponse(data)

def store_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        

        if not name or not price or not description:
            return JsonResponse({'success': False, 'message': 'All field are required'}, status=400)
        
        try:
            price = float(price)  
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Price must be a valid number'}, status=400)

        if not image:
            return JsonResponse({'success': False, 'message': 'Product image is required'}, status=400)
        else:
            if not isinstance(image, UploadedFile):
                return JsonResponse({'success': False, 'message': 'Uploaded file is not valid'}, status=400)
            else:
                if not image.content_type.startswith('image/'):
                    return JsonResponse({'success': False, 'message': 'Only image file are allowed'}, status=400)
                if image.size > 5 * 1024 * 1024:
                    return JsonResponse({'success': False, 'message': 'Image size is lessthan 5MB'}, status=400)
        product = Product(
            name=name,
            price=price,
            description=description,
            image=image
        )
        try:
            product.save()
        except Exception as e:
            return JsonResponse({'success': False, 'errors': ['Failed to save the product.']}, status=500)
        
        return JsonResponse({'success': True, 'message': 'Product added successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

# def update_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')  # Adjust the redirect as needed
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'app/admin/product/edit.html', {'form': form, 'product': product})

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image') if 'image' in request.FILES else None

        if not name or not price or not description:
            return JsonResponse({'success': False, 'message': 'All fields are required'}, status=400)
        
        try:
            price = float(price)  
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Price must be a valid number'}, status=400)

        if image:
            if not isinstance(image, UploadedFile):
                return JsonResponse({'success': False, 'message': 'Uploaded file is not valid'}, status=400)
            else:
                if not image.content_type.startswith('image/'):
                    return JsonResponse({'success': False, 'message': 'Only image files are allowed'}, status=400)
                if image.size > 5 * 1024 * 1024:
                    return JsonResponse({'success': False, 'message': 'Image size should be less than 5MB'}, status=400)

        product.name = name
        product.price = price
        product.description = description
        
        if image:  
            product.image = image

        try:
            product.save()
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed to update the product.'}, status=500)
        
        return JsonResponse({'success': True, 'message': 'Product updated successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return JsonResponse({'success': True})

def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'app/admin/inquiries.html', {'inquiries': inquiries})

def delete_inquiry(request, pk):
    if request.method == 'POST':
        inquiry = get_object_or_404(Inquiry, pk=pk)
        inquiry.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def feedback_list(request):
    feedbacks = Feedback.objects.all() 
    return render(request, 'app/admin/feedback.html', {'feedbacks': feedbacks})

def delete_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.delete()
            return JsonResponse({'success': True})
        except Feedback.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Feedback not found'})
    return HttpResponse(status=405)




