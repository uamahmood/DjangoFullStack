from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book, Review, Author
from django.contrib import messages
import bcrypt, re
# Create your views here.

def index(request):
    return render(request, 'app_one/index.html')

def success(request):
    # to be deleted later
    return HttpResponse('Success!')

def join(request):
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/')
    else:
        hash=bcrypt.hashpw(request.POST['pass'].encode(),bcrypt.gensalt())
        create=User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password=hash.decode())
        request.session['user']=create.id
        print(request.session['user'])
        messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
        return redirect('/books')
def verify(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['id']):
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/')
    elif len(request.POST['id'])<1:
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/')
    else:
        filtered=User.objects.filter(email=request.POST['id'])
        if filtered:
            result=User.objects.get(email=request.POST['id'])
            if bcrypt.checkpw(request.POST['pass'].encode(), result.password.encode()):
                request.session['user']=result.id
                messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
                return redirect('/books')
            else:
                messages.error(request, 'User could not be logged in',extra_tags="login")
                return redirect('/')
        else:
            messages.error(request, 'User could not be logged in',extra_tags="login")
            return redirect('/')
def reset(request):
    request.session.clear()
    messages.error(request, 'You have been logged out',extra_tags="out")
    return redirect('/')
def wall(request):
    if 'user' in request.session:
        user=User.objects.get(id=request.session['user'])
        all_books=Book.objects.all()
        all_reviews=Review.objects.all().order_by('-created_at')
        context={
            "profile":user,
            "books":all_books,
            "reviews":all_reviews,
        }
        return render(request,'app_one/wall.html',context)
    else:
        messages.error(request, 'You must be logged in to access site',extra_tags="out")
        return redirect('/')
def add_book(request):
    if 'user' in request.session:
        user=User.objects.get(id=request.session['user'])
        all_books=Book.objects.all()
        all_authors=Author.objects.all()
        context={
            "profile":user,
            "books":all_books,
            "authors":all_authors,
        }
        return render(request,'app_one/add.html',context)
    else:
        messages.error(request, 'You must be logged in to access site',extra_tags="out")
        return redirect('/')
def add(request):
    errors=Book.objects.book_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/books/add')
    elif len(request.POST['new'])<1:
        author=Author.objects.get(id=request.POST['existing'])    
    else:
        author=Author.objects.create(name = request.POST['new'])
        
    review=f"{request.POST['text']}"
    book=Book.objects.create(title=request.POST['title'],author=author)
    poster=User.objects.get(id=request.session['user'])
    Review.objects.create(review=review,subject=book,poster=poster,rating=request.POST['rating'])
    
    # return redirect('/')
    return redirect('/books/'+str(book.id))
def review(request):
    book=Book.objects.get(id=request.POST['source'])
    poster=User.objects.get(id=request.session['user'])
    review=f"{request.POST['review']}"
    Review.objects.create(subject=book,review=review, poster=poster,rating=request.POST['rating'])
    return redirect('/books/'+str(book.id))

def destroy(request):
    book=request.POST['location']
    number=int(request.POST['review'])
    row_to_delete=Review.objects.get(id=number)
    row_to_delete.delete()
    return redirect('/books/'+book)
def book(request,num):
    if 'user' in request.session:
        number=int(num)
        user=User.objects.get(id=request.session['user'])
        select_book=Book.objects.get(id=number)
        select_reviews=Review.objects.filter(subject=select_book).order_by('-created_at')
        context={
            "book":select_book,
            "reviews":select_reviews,
            "user":user
        }
        return render(request, 'app_one/book.html', context)
    else:
        messages.error(request, 'You must be logged in to access site',extra_tags="out")
        return redirect('/')
def user(request,num):
    if 'user' in request.session:
        number=int(num)
        user=User.objects.get(id=number)
        select_reviews=Review.objects.filter(poster=user).order_by('-created_at')
        total=0
        for i in select_reviews:
            total +=1
            
        context={
            "profile":user,
            "reviews":select_reviews,
            "review_total":total
        }
        return render(request, 'app_one/user.html',context)
    else:
        messages.error(request, 'You must be logged in to access site',extra_tags="out")
        return redirect('/')
def author(request,num):
    if 'user' in request.session:
        number=int(num)
        user=User.objects.get(id=request.session['user'])
        author=Author.objects.get(id=number)
        books=Book.objects.filter(author=author)

        # select_reviews=Review.objects.filter(subject=books).order_by('-created_at')
        book_total=0
        print(books)
        for i in books:
            book_total +=1
            
        context={
            "profile":user,
            # "reviews":select_reviews,
            "book_total":book_total,
            "author":author,
            "books":books
        }
        return render(request, 'app_one/author.html',context)
    else:
        messages.error(request, 'You must be logged in to access site',extra_tags="out")
        return redirect('/')