from .models import User
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if user.account_locked_until:
                if timezone.now() < user.account_locked_until:
                    return render(request, "login.html", {
                        "error": "Your account is locked for 1 hour. Please try again later."
                    })
                else:
                    user.failed_attempts = 0
                    user.account_locked_until = None
                    user.save()
            if check_password(password, user.password):
                user.failed_attempts = 0
                user.account_locked_until = None
                user.save()
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                return redirect("home")
            else:
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.account_locked_until = timezone.now() + timedelta(hours=1)
                    user.save()
                    return render(request, "login.html", {
                        "error": "Your account has been locked for 1 hour due to 5 failed login attempts."
                    })
                user.save()
                return render(request, "login.html", {
                    "error": f"Invalid password. Attempt {user.failed_attempts}/5"
                })
        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "User not found."
            })
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        mobile = request.POST["mobile"]
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if len(mobile) != 10 or not mobile.isdigit():
         return render(request, "signup.html", {
        "error": "Mobile number must contain exactly 10 digits."
    })
        if len(password) < 8:
            return render(request, 'signup.html', {
                'error': 'Password must contain at least 8 characters.'
            })  
        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match.'
            })
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists.'
            })
        user = User.objects.create(
    username=username,
    mobile=mobile,
    password=make_password(password)
)
        from django.contrib import messages
        return render(request, "signup.html", {
    "success": "Account created successfully.",
    "clear": True
})
    return render(request, 'signup.html')

from django.shortcuts import render
from .models import User
from django.shortcuts import render, redirect
from .models import User

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        mobile = request.POST.get("mobile")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            return render(request, "forgot_password.html", {
                "error": "Passwords do not match."
            })
        try:
            user = User.objects.get(username=username, mobile=mobile)
            user.password = new_password
            user.save()
            return render(request, "forgot_password.html", {
                "success": "Password updated successfully."
            })

        except User.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "Username or Mobile Number is incorrect."
            })
    return render(request, "forgot_password.html")
def home(request):
    return render(request, "home.html")

from .models import UserFile
def home(request):
    if "user_id" not in request.session:
        return redirect("login")
    files = UserFile.objects.filter(
        user_id=request.session["user_id"]
    ).order_by("-uploaded_at")
    return render(request, "home.html", {
        "files": files
    })


from .models import User, UserFile
import os
def upload_file(request):
    if "user_id" not in request.session:
        return redirect("login")
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        file = request.FILES.get("file")
        if not file:
            return render(request, "upload.html", {
                "error": "Please select a file."
            })

        allowed_extensions = [
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
            ".doc",
            ".docx"
        ]

        extension = os.path.splitext(file.name)[1].lower()

        if extension not in allowed_extensions:

           return render(request, "upload.html", {
    "error": "❌ Invalid file type. Only PDF, JPG, PNG, DOC and DOCX files are allowed."
})
            
        max_size = 10 * 1024 * 1024
        if file.size > max_size:
            return render(request, "upload.html", {
    "error": "❌ File size is too large. Maximum allowed size is 10 MB."
})

        user = User.objects.get(id=request.session["user_id"])
        new_file = UserFile.objects.create(
            user=user,
            username=user.username,
            title=title,
            category=category,
            description="",
            file=file
        )
        return render(request, "upload.html", {
            "success": "File uploaded successfully."
        })
    
    return render(request, "upload.html")

from .models import UserFile
import os
from django.shortcuts import get_object_or_404
def view_file(request, file_id):
    if "user_id" not in request.session:
        return redirect("login")

    file = get_object_or_404(
        UserFile,
        id=file_id,
        user_id=request.session["user_id"]
    )

    extension = os.path.splitext(file.file.name)[1].lower()

    is_pdf = extension == ".pdf"
    is_image = extension in [".jpg", ".jpeg", ".png", ".gif", ".webp"]

    file_url = request.build_absolute_uri(file.file.url)

    return render(request, "view_file.html", {
        "file": file,
        "is_pdf": is_pdf,
        "is_image": is_image,
        "file_url": file_url,
    })
import os
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import get_object_or_404
def delete_file(request, file_id):
    if "user_id" not in request.session:
        return redirect("login")
    file = get_object_or_404(
        UserFile,
        id=file_id,
        user_id=request.session["user_id"]
    )
    file.delete()
    return redirect("home")


from django.shortcuts import render, redirect
def logout_view(request):
    request.session.flush()
    return redirect("login")
from django.shortcuts import redirect
from .models import User, UserFile

def edit_username(request):
    if request.method == "POST":
        old_username = request.session.get("username")
        new_username = request.POST.get("username").strip()
        if User.objects.filter(username=new_username).exists():
            return redirect("home")
        User.objects.filter(username=old_username).update(
            username=new_username
        )
        UserFile.objects.filter(username=old_username).update(
            username=new_username
        )
        request.session["username"] = new_username
    return redirect("home")

from django.shortcuts import redirect
from .models import User
from django.http import JsonResponse
from .models import User

def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            return JsonResponse({
                "status": "error",
                "message": "Passwords do not match."
            })
        user = User.objects.get(
            id=request.session["user_id"]
        )
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({
            "status": "success",
            "message": "Password Updated Successfully"
        })
    return JsonResponse({
        "status": "error"
    })

