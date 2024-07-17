from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
	records = Record.objects.all()

	# check to see if logging in
	if request.method == 'POST':
		# username and password are ref from home.html
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# if correct
			login(request, user)
			messages.success(request, "You have been logged in!")
			return redirect('home')
		else:
			messages.success(request, "There was an error logging in, Please try again!!")
			return redirect('home')
	else:

		return render(request,'home.html',{'records':records})


def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged out!!")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST) 
		# pass whatever is passed in form
		if form.is_valid():
			form.save()
			# Authenticate and log in 
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request, user)
			messages.success(request,"You have successfully registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm() 
		# since not posting anything i.e. doesn't filling, won't pass the request
		return render(request,'register.html',{'form':form})

	return render(request,'register.html',{'form':form})

def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html',{'customer_record':customer_record})

	else:
		messages.success(request,"You must be logged in to view this page!")
		return redirect('home')


def delete_record(request,pk):
	if request.user.is_authenticated:

		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully")
		return redirect('home')

	else:
		messages.success(request, "You must be logged in to do this action!!")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request,"Record Added...")
				return redirect('home')


		return render(request, 'add_record.html',{'form':form})

	else:
		messages.success(request, "You must be logged in")
		return redirect('home')

def update_record(request,pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		# populate the records with existing value --> instance = current_record
		form = AddRecordForm(request.POST or None, instance = current_record)

		# check if form is post or get
		if form.is_valid():
			form.save()
			messages.success(request, "Record has been updated")
			return redirect('home')

		return render(request, 'update_record.html',{'form':form})

	else:
		messages.success(request, "You must be logged in")
		return redirect('home')


		





