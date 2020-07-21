from django.shortcuts import render, HttpResponse, redirect
from homeApp.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blogApp.models import Post

# Create your views here.
def home(request):
    allPosts = Post.objects.all()
    context = {'allPosts' : allPosts}
    return render(request, 'homeApp/home.html', context)

def contact(request):
    if request.method == 'POST':
        #name = request.POST.get('name', False)
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        print(name, email, content)

        if len(name) <1 or len(email) < 3 or len(content) <4:
            messages.error(request, 'Please enter your details correctly.')
        else:
            contact = Contact(name = name, email = email, content = content)
            contact.save()
            messages.success(request, 'It is a success!')
        

    return render(request, 'homeApp/contact.html')

def about(request):
    return render(request, 'homeApp/about.html')

def search(request):
    # Getting the search query
    query = request.GET['query']
    if len(query) > 99:
        allPosts = Post.objects.none()
    else:
        # Searching using icontains
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPostAuthor = Post.objects.filter(author__icontains=query)
        allPost = allPostTitle.union(allPostContent)
        allPosts = allPost.union(allPostAuthor)

    if allPosts.count() == 0:
        messages.warning(request, 'Oops! can not find what you are looking for.')


    param = {'allPosts' : allPosts, 'query' : query}

    return render(request, 'homeApp/search.html', param)


def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Checks for bad inputs
        if len(username) > 15:
            messages.error(request, "You username must be under 10 characters.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Your username should only contain letters and numbers.")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your tech blog account has been successfully created")
        return redirect('home')
    
    else:
        return HttpResponse(' 404 not found')



def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username = loginusername, password = loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect ('/')
        else:
            messages.error(request, "Invalid credentials, please try again")
            return redirect ('/')


def handleLogout(request):
    logout(request)
    messages.success(request, "You are successfully logged out!")
    return redirect ('/')

