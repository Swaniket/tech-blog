from django.shortcuts import render, HttpResponse, redirect, render
from blogApp.models import Post, blogComment
from django.contrib import messages
from blogApp.templatetags import extras

# Create your views here.
def blogHome(request):
    # To pull all the objects
    allPosts = Post.objects.all()
    context = {'allPosts' : allPosts}
    return render(request, 'blogApp/blogHome.html', context)

def blogPost(request, slug):
    # To get the object drom the query set
    post = Post.objects.filter(slug = slug).first()
    # Get the comments for the corrosponding posts
    comments = blogComment.objects.filter(post = post, parent = None)
    replies = blogComment.objects.filter(post = post).exclude(parent = None)
    # counting the views
    post.views = post.views + 1
    post.save()

    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)


    context = {'post' : post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blogApp/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno = postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "" :
            comment = blogComment(comment = comment, user = user, post = post)
            comment.save()
            messages.success(request, "Your comment has been posted")
        else:
            parent = blogComment.objects.get(sno = parentSno)
            comment = blogComment(comment = comment, user = user, post = post, parent = parent)
            comment.save()
            messages.success(request, "Your reply has been posted")

        
    # To get the object drom the query set
    return redirect(f'/blog/{post.slug}')
    

