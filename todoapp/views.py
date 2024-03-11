from django.shortcuts import render,redirect

from django.views.generic import View
from todoapp.models import Todo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.views.decorators.cache import never_cache




# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]


class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=("created_date","user_object",)
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control form-select"}),
        }
        
class Registrationform(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
        

# VIEW FOR LISTING ALL TODOS
# URL       :localhost:8000/todos/all/
# METHOD      : get 
@method_decorator(decs,name="dispatch")
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(user_object=request.user)
        return render(request,"todo_list.html",{"data":qs})
    

# VIEW FOR CREATING A NEW TODOS
# URL :   localhost:8000/todos/add/
# MRTHOD : get , post
@method_decorator(decs,name="dispatch")
class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            # form.save()
            data=form.cleaned_data
            Todo.objects.create(**data,user_object=request.user)
            messages.success(request,"Todo's has been added successfully")
            return redirect("todo-list")
        else:
            messages.error(request,"failed to add todo's")
            return render(request,"todo_add.html",{"form":form})


# VIEW FOR DETAILING A TODOS
# URL :   localhost:8000/todos/{id}/
# MRTHOD : get 
@method_decorator(decs,name="dispatch")
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})
    
# VIEW FOR DELETE A TODOS
# URL :   localhost:8000/todos/{id}/remove/
# MRTHOD : get 
@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.filter(id=id).delete()
        messages.success(request,"todo's has been removed successfully")
        return redirect("todo-list")

# VIEW FOR UPDATE A TODOS
# URL :   localhost:8000/todos/{id}/change/
# MRTHOD : get , post
@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(instance=todo_objects)
        return render(request,"todo_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(request.POST,instance=todo_objects)
        if form.is_valid():
            form.save()
            messages.success(request,"todo's has been updated successfully")
            return redirect("todo-list")
        else:
            messages.error(request,"failed to update todo's")
            return render(request,"todo_edit.html",{"form":form})
        
        
# VIEW   : FOR SIGNUP 
# url    : localhost:8000/signup/
# method : get , post
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=Registrationform()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=Registrationform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("account created")
            return redirect("signup")
        else:
            print("registration failed")
            return render(request,"register.html",{"form":form})
        
# VIEW   : FOR SIGNIN
# url    : localhost:8000/signin/
# method : get , post

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            #  cheack valid or invalid
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print("credentials are valid")
                login(request,user_object)  # to start session   
                return redirect("todo-list")
        print("invalid")
        return render(request,"signin.html",{"form":form})
 
@method_decorator(decs,name="dispatch")   
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


      