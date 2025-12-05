from django.shortcuts import render, redirect
from django.db.models import Sum
from decimal import Decimal
from . import forms
from django.contrib.auth import login, authenticate, logout
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from .models import Income, Expense
def home(request):
    balance = 0
    if request.user.is_authenticated:
        total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense
    return render(request, 'reg/home.html', {'balance': balance})
def reg(request):
    form=forms.register()
    if request.method=="POST":
        form=forms.register(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    data={ 'form':form}
    return render(request, 'reg/reg.html',data)
def flogin(request):
    form=forms.loginf()
    if request.method=="POST":
        form=forms.loginf(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    data={"form":form}
    return render(request,'reg/login.html',data)
def flogout(request):
    logout(request)
    return redirect("home")


@login_required
def useage(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('useage')
    else:
        form = ExpenseForm()


    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')


    category_summary = (
        Expense.objects
        .filter(user=request.user)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )


    total_spent = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(request, 'reg/useage.html', {
        'form': form,
        'expenses': expenses,
        'category_summary': category_summary,
        'total_spent': total_spent,
    })


@login_required
def income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income_obj = form.save(commit=False)
            income_obj.user = request.user
            income_obj.save()
            return redirect('income')
    else:
        form = IncomeForm()


    incomes = Income.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reg/income.html', {'form': form, 'incomes': incomes})

# Create your views here.
