from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense, Income
from .form import ExpenseForm, IncomeForm


def home(request):
    # =====================
    # HANDLE FORMS (POST)
    # =====================
    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            expense_form = ExpenseForm()
            if income_form.is_valid():
                income_form.save()
                return redirect('home')

        elif 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            income_form = IncomeForm()
            if expense_form.is_valid():
                expense_form.save()
                return redirect('home')
    else:
        income_form = IncomeForm()
        expense_form = ExpenseForm()

    # =====================
    # EXPENSE LIST + FILTER
    # =====================
    expenses = Expense.objects.all().order_by('-date')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    # =====================
    # TOTALS
    # =====================
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    # =====================
    # CATEGORY WISE TOTAL
    # =====================
    category_data = (
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
    )

    # =====================
    # PIE CHART DATA
    # =====================
    labels = []
    data = []

    for c in category_data:
        labels.append(c['category'])
        data.append(float(c['total']))

    context = {
        'income_form': income_form,
        'expense_form': expense_form,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_data': category_data,
        'labels': labels,
        'data': data,
    }

    return render(request, 'home.html', context)


def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('home')


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit.html', {'form': form})

      