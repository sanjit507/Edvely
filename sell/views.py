from django.shortcuts import render, redirect
from django.http import HttpResponse
from sell.models import Course, Profile, UserCourse, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .form import ProfileForm
from course.settings import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
        form = ProfileForm(instance=profile)
    except Profile.DoesNotExist:
        form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=getattr(request.user, 'profile', None))
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')

    return render(request, 'sell/profile_form.html', {'form': form})

@login_required
def dashboard(request):
    user_courses = request.user.usercourse_set.select_related('Course')
    return render(request, 'sell/dashboard.html', {'user_courses': user_courses})


def home(request):
    courses = Course.objects.all()
    return render(request, 'sell/home.html', {'courses': courses})


def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    # pass videos ordered by serial_number for predictable ordering in the template
    videos = course.videos.order_by('serial_number')
    
    # Check permissions: if not logged in, user can only see the course if the first video is a preview
    if not request.user.is_authenticated:
        first_video = videos.first()
        if not first_video or not first_video.is_preview:
            return HttpResponse("You are not allowed to view this course")
            
    has_access = False
    if request.user.is_authenticated:
        has_access = request.user.usercourse_set.filter(Course=course).exists()
    return render(request, 'sell/course_detail.html', {'course': course, 'videos': videos, 'has_access': has_access})

#Login and Register and Dashboard




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})




def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    if not request.user.is_authenticated:
        return redirect('login')
    action=request.GET.get('action')
    order=None
    if action == 'checkout':
        amount = int(course.discounted_price * 100)
        # Create Razorpay client at request time to ensure env vars are loaded
        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            return HttpResponse("Razorpay keys not configured", status=500)
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })
    
    context = {
        'course': course,
        'order': order,
        'RAZORPAY_KEY_ID': RAZORPAY_KEY_ID,
    }

    return render(request, 'sell/checkout.html', context)

@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        course_id = request.POST.get('course_id')
        user = request.user
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Course not found'}, status=404)
        # Create UserCourse
        user_course, created = UserCourse.objects.get_or_create(user=user, Course=course)
        # Create Payment
        Payment.objects.create(
            order_id=order_id,
            payment_id=payment_id,
            user_course=user_course,
            Course=course,
            user=user,
            status=True
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




