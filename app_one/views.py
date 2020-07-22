from django.shortcuts import render, HttpResponse, redirect
from app_one.models import *
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    if "userid" not in request.session:
        return render(request, 'index.html', {"FoodTypes": FoodType.objects.all()})
    context = {
        "name": request.session['first_name'],
        "FoodTypes": FoodType.objects.all()
    }
    return render(request, 'index.html', context)


def login(request):
    if request.method == "POST":
        result = User.objects.filter(email=request.POST["email"])
        if not result.exists():
            messages.error(request, "This user doesn't exists! Please register instead")
            return redirect('/login')
        result = result[0]
        if not bcrypt.checkpw(request.POST["password"].encode(), result.hash_password.encode()):
            messages.error(request, "Wrong email/password combination!")
            return redirect('/login')
        request.session['userid'] = result.id
        request.session['first_name'] = result.first_name
        return redirect('/')
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/signup')

        hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST["first_name"],
                            last_name=request.POST["last_name"],
                            email=request.POST["email"],
                            hash_password=hashed_pw
                            )
        # request.session['userid'] = a.id
        # request.session['first_name'] = a.first_name
        # return redirect('/dashboard')
        # masi qe te regjistrohet useri, imella edhe passwordi i tij ekziston hala ne variablen request
        # tash qet request mujna me qu direkt te metoda login, edhe tani ajo metoda e kryn punen e logimit
        # nbaz tvariablave qe ekzistojn ne request.
        return login(request)
        # return redirect('/login')
    else:  # eshte GET request.
        return render(request, 'signup.html')


# def dashboard(request):
#     return render(request, 'index.html')

def footer(request):
    return render(request, 'footer.html')

def recipes(request, type):
    if not FoodType.objects.filter(type=type).exists():
        return HttpResponse("Error 404")
    recipes = FoodType.objects.filter(type=type).first().recipes.all()
    context = {
        "recipes": recipes,
        "type": type,
        "FoodTypes": FoodType.objects.all()
    }
    return render(request, 'recipes.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def search(request):
    if "q" in request.GET:
        a = Recipe.objects.filter(recipe_name__contains=request.GET["q"])
        b = Recipe.objects.filter(ingredients__contains=request.GET["q"])
        c = Recipe.objects.filter(recipe_description__contains=request.GET["q"])
        context = {
            "recipes": a.union(b,c)
        }
        return render(request, "searchresult.html", context)
    else:
        return redirect('/')
def addRecipe(request):
    if not "userid" in request.session:
        return redirect('/login')
    if request.method == "POST":
        errors = Recipe.objects.validate(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/addRecipe')
        recipe = Recipe.objects.create(
            recipe_name=request.POST["recipe_name"],
            ingredients=request.POST["ingredients"],
            recipe_description=request.POST["recipe_description"],
            food_type=FoodType.objects.filter(id=int(request.POST["food_type"]))[0]
        )
        if len(request.FILES) > 0:
            recipe.photo = request.FILES['file']
            recipe.save()
        return redirect('/recipes/' + str(recipe.id))
    context = {
        "food_types": FoodType.objects.all()
    }
    return render(request, 'addRecipe.html', context)