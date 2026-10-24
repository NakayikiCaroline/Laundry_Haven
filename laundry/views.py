from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from .models import Customer, LaundryOrder, Payment, Service, BusinessInformation
from .forms import CustomerForm, LaundryOrderForm, ServiceForm, PaymentForm, BusinessInformationForm

# Create your views here.

def home(request):
    paid_payments = Payment.objects.filter(paid=True)

    context = {
        "customer_count": Customer.objects.count(),
        "order_count": LaundryOrder.objects.count(),
        "payment_count": paid_payments.count(),
        "revenue": paid_payments.aggregate(
            total=Sum('amount_paid')
        )['total'] or Decimal('0.00'),
        "recent_orders": LaundryOrder.objects.select_related(
            'customer',
            'service',
        ).order_by('-order_date')[:5],
    }

    return render(request, "laundry/home.html", context)


def customer_list(request):
    customers = Customer.objects.all().order_by('-id')

    return render(request,
                  'laundry/customer_list.html',
                  {'customers': customers})


def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('customer_list')

    else:
        form = CustomerForm()

    return render(request,
                  'laundry/add_customer.html',
                  {'form': form})

# Removed broken update_customer helper (duplicate of edit_customer) to avoid NameError bugs


def delete_customer(request, pk):
    # Use the Customer model (not a lowercase variable) when fetching the object
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')

    return render(request,
                  'laundry/delete_customer.html',
                  {'customer': customer})


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'laundry/edit_customer.html', {
        'form': form})


def order_list(request):

    orders = LaundryOrder.objects.select_related(
        'customer',
        'service'
    ).order_by('-id')

    context = {

        'orders': orders,

        'pending_count':
            orders.filter(
                status='Pending'
            ).count(),

        'processing_count':
            orders.filter(
                status='Processing'
            ).count(),

        'completed_count':
            orders.filter(
                status='Completed'
            ).count(),
    }

    return render(
        request,
        'laundry/order_list.html',
        context
    )


def add_order(request):

    if request.method == 'POST':

        form = LaundryOrderForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('order_list')

    else:

        form = LaundryOrderForm()

    return render(
        request,
        'laundry/add_order.html',
        {
            'form': form
        }
    )


def edit_order(request, pk):
    order = get_object_or_404(LaundryOrder, pk=pk)

    if request.method == 'POST':
        form = LaundryOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = LaundryOrderForm(instance=order)

    return render(
        request,
        'laundry/edit_order.html',
        {
            'form': form,
            'order': order,
        }
    )


def delete_order(request, pk):
    order = get_object_or_404(LaundryOrder, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('order_list')

    return render(
        request,
        'laundry/delete_order.html',
        {
            'order': order,
        }
    )


def service_list(request):

    services = Service.objects.all().order_by('-id')

    return render(
        request,
        'laundry/service_list.html',
        {
            'services': services
        }
    )
def add_service(request):

    if request.method == 'POST':

        form = ServiceForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('service_list')

    else:

        form = ServiceForm()

    return render(
        request,
        'laundry/add_service.html',
        {
            'form': form
        }
    )
def edit_service(request, pk):

    service = get_object_or_404(
        Service,
        pk=pk
    )

    if request.method == 'POST':

        form = ServiceForm(
            request.POST,
            instance=service
        )

        if form.is_valid():

            form.save()

            return redirect('service_list')

    else:

        form = ServiceForm(
            instance=service
        )

    return render(
        request,
        'laundry/edit_service.html',
        {
            'form': form,
            'service': service
        }
    )
def delete_service(request, pk):

    service = get_object_or_404(
        Service,
        pk=pk
    )

    if request.method == 'POST':

        service.delete()

        return redirect('service_list')

    return render(
        request,
        'laundry/delete_service.html',
        {
            'service': service
        }
    )
# =========================
# PAYMENT LIST
# =========================

def payment_list(request):
   payments = Payment.objects.select_related(
       'order__customer',
       'order__service',
   ).order_by('-id')
   revenue = payments.aggregate(total=Sum('amount_paid'))['total'] or 0

   return render(
       request,
       'laundry/payments.html',
       {
           'payments': payments,
           'payment_count': payments.count(),
           'revenue': revenue,
           'cash_count': payments.filter(payment_method='Cash').count(),
           'mobile_count': payments.filter(
               payment_method='Mobile Money'
           ).count(),
       }
   )


def payment_receipt(request, pk):
    payment = get_object_or_404(
        Payment.objects.select_related(
            'order__customer',
            'order__service',
        ),
        pk=pk
    )
    balance_due = max(
        payment.order.total_amount - payment.amount_paid,
        Decimal('0.00')
    )
    business = BusinessInformation.objects.filter(pk=1).first()
    return render(
        request,
        'laundry/receipt.html',
        {
            'payment': payment,
            'balance_due': balance_due,
            'business': business,
        }
    )

# =========================
# ADD PAYMENT
# =========================

def add_payment(request):

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('payment_list')

    else:
        form = PaymentForm()

    return render(
        request,
        'laundry/add_payment.html',
        {'form': form}
    )


# =========================
# EDIT PAYMENT
# =========================

def edit_payment(request, pk):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():
            form.save()
            return redirect('payment_list')

    else:
        form = PaymentForm(
            instance=payment
        )

    return render(
        request,
        'laundry/edit_payment.html',
        {
            'form': form,
            'payment': payment
        }
    )


# =========================
# DELETE PAYMENT
# =========================

def delete_payment(request, pk):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    if request.method == 'POST':

        payment.delete()

        return redirect('payment_list')

    return render(
        request,
        'laundry/delete_payment.html',
        {
            'payment': payment
        }
    )  
def reports(request):
    valid_report_types = {'customers', 'orders', 'payments', 'revenue'}
    report_type = request.GET.get('type', 'payments')
    if report_type not in valid_report_types:
        report_type = 'payments'

    # Read the selected date range
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    report_errors = []

    parsed_start_date = None
    parsed_end_date = None
    if start_date:
        try:
            parsed_start_date = datetime.strptime(
                start_date, '%Y-%m-%d'
            ).date()
        except ValueError:
            report_errors.append('Enter a valid start date.')

    if end_date:
        try:
            parsed_end_date = datetime.strptime(
                end_date, '%Y-%m-%d'
            ).date()
        except ValueError:
            report_errors.append('Enter a valid end date.')

    if (
        parsed_start_date
        and parsed_end_date
        and parsed_start_date > parsed_end_date
    ):
        report_errors.append(
            'The start date must be on or before the end date.'
        )
        parsed_start_date = None
        parsed_end_date = None

    orders = LaundryOrder.objects.select_related(
        'customer', 'service'
    ).all().order_by('-order_date')

    payments = Payment.objects.select_related(
        'order', 'order__customer'
    ).all().order_by('-payment_date')

    customers = Customer.objects.all().order_by('full_name')

    # Apply date filters to orders and payments.
    if parsed_start_date:
        orders = orders.filter(order_date__date__gte=parsed_start_date)
        payments = payments.filter(
            payment_date__date__gte=parsed_start_date
        )

    if parsed_end_date:
        orders = orders.filter(order_date__date__lte=parsed_end_date)
        payments = payments.filter(
            payment_date__date__lte=parsed_end_date
        )

    # Only confirmed paid records contribute to money received
    paid_payments = payments.filter(paid=True)

    total_revenue = (
        paid_payments.aggregate(total=Sum('amount_paid'))['total']
        or Decimal('0.00')
    )

    payment_count = paid_payments.count()

    revenue_by_method = (
        paid_payments.values('payment_method')
        .annotate(total=Sum('amount_paid'), count=Count('id'))
        .order_by('payment_method')
    )

    # Order status summary
    order_statuses = (
        orders.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    context = {
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
        'report_errors': report_errors,

        'customers': customers,
        'orders': orders,
        'payments': payments,

        'customer_count': customers.count(),
        'order_count': orders.count(),
        'payment_count': payment_count,
        'total_revenue': total_revenue,

        'revenue_by_method': revenue_by_method,
        'order_statuses': order_statuses,
    }

    return render(request, 'laundry/reports.html', context)
def settings_page(request):
    business, created = BusinessInformation.objects.get_or_create(
        pk=1,
        defaults={
            'business_name': 'Laundry Haven',
            'receipt_footer': (
                'Thank you for choosing Laundry Haven!'
            ),
        }
    )

    if request.method == 'POST':
        form = BusinessInformationForm(
            request.POST,
            instance=business
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Business information saved successfully!'
            )
            return redirect('settings')
        else:
            messages.error(
                request,
                'Please correct the errors in the form.'
            )
    else:
        form = BusinessInformationForm(instance=business)

    return render(
        request,
        'laundry/settings.html',
        {'form': form, 'business': business}
    )


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
   
