from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import PaymentForm
from .models import (
    BusinessInformation,
    Customer,
    LaundryOrder,
    Payment,
    Service,
)


class LoginTests(TestCase):
    def test_login_redirects_to_dashboard_and_authenticates_user(self):
        user = get_user_model().objects.create_user(
            username='login-test',
            password='test-password-123'
        )

        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'test-password-123',
        })

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(
            str(self.client.session['_auth_user_id']),
            str(user.pk)
        )

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'unknown-user',
            'password': 'incorrect-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Invalid username or password. Please try again.'
        )


class PaymentTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            full_name='Test Customer',
            phone='0700000000'
        )
        self.service = Service.objects.create(
            service_name='Wash',
            price='10000.00'
        )
        self.order = LaundryOrder.objects.create(
            customer=self.customer,
            service=self.service,
            quantity=1,
            total_amount='15000.00'
        )
        self.payment = Payment.objects.create(
            order=self.order,
            amount_paid='10000.00',
            payment_method='Cash'
        )

    def test_payment_form_accepts_datetime_local_value(self):
        order = LaundryOrder.objects.create(
            customer=self.customer,
            service=self.service,
            quantity=1,
            total_amount='5000.00'
        )
        form = PaymentForm(data={
            'order': order.pk,
            'amount_paid': '10000.00',
            'payment_method': 'Cash',
            'payment_date': '2026-10-24T14:04',
            'reference': '',
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.fields['payment_date'].widget.input_type,
            'datetime-local'
        )

    def test_payment_list_displays_statistics(self):
        response = self.client.get(reverse('payment_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_count'], 1)
        self.assertEqual(response.context['revenue'], Decimal('10000.00'))
        self.assertEqual(response.context['cash_count'], 1)
        self.assertEqual(response.context['mobile_count'], 0)
        self.assertContains(response, self.customer.full_name)

    def test_payment_receipt_route_renders_receipt(self):
        response = self.client.get(
            reverse('receipt', args=[self.payment.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Official Payment Receipt')
        self.assertContains(response, self.customer.full_name)
        self.assertContains(response, 'images/logo.jpg')
        self.assertContains(response, 'BALANCE DUE')
        self.assertContains(response, '5000.00')

    def test_home_revenue_uses_recorded_payments(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_count'], 1)
        self.assertEqual(response.context['revenue'], Decimal('10000.00'))
        self.assertContains(response, 'id="dashboardDateTime"')

    def test_home_excludes_unpaid_payments_from_statistics(self):
        unpaid_order = LaundryOrder.objects.create(
            customer=self.customer,
            service=self.service,
            quantity=1,
            total_amount='20000.00'
        )
        Payment.objects.create(
            order=unpaid_order,
            amount_paid='20000.00',
            payment_method='Cash',
            paid=False,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.context['order_count'], 2)
        self.assertEqual(response.context['payment_count'], 1)
        self.assertEqual(response.context['revenue'], Decimal('10000.00'))

    def test_home_shows_real_recent_orders(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, self.customer.full_name)
        self.assertContains(response, self.service.service_name)
        self.assertContains(response, 'UGX 15000.00')
        self.assertNotContains(response, 'John Doe')
        self.assertNotContains(response, 'Dry Cleaning')

    def test_reports_page_opens_from_navigation_and_shows_payments(self):
        response = self.client.get(reverse('reports'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['report_type'], 'payments')
        self.assertEqual(response.context['payment_count'], 1)
        self.assertEqual(response.context['total_revenue'], Decimal('10000.00'))
        self.assertContains(response, 'Business Reports')
        self.assertContains(response, reverse('reports'))
        self.assertContains(response, self.customer.full_name)

    def test_reports_date_range_filters_payment_results(self):
        response = self.client.get(reverse('reports'), {
            'type': 'payments',
            'start_date': '2026-10-25',
            'end_date': '2026-10-26',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_count'], 0)
        self.assertEqual(response.context['total_revenue'], Decimal('0.00'))

    def test_reports_invalid_dates_show_filter_error(self):
        response = self.client.get(reverse('reports'), {
            'type': 'revenue',
            'start_date': 'not-a-date',
            'end_date': '2026-10-01',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid start date.')

    def test_reports_unknown_type_falls_back_to_payments(self):
        response = self.client.get(reverse('reports'), {'type': 'unknown'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['report_type'], 'payments')

    def test_settings_page_loads_and_is_linked_in_navigation(self):
        response = self.client.get(reverse('settings'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Business Information')
        self.assertContains(response, reverse('settings'))
        self.assertEqual(BusinessInformation.objects.count(), 1)

    def test_settings_save_updates_receipt_business_details(self):
        response = self.client.post(reverse('settings'), {
            'business_name': 'Fresh Laundry',
            'phone': '0712345678',
            'email': 'hello@example.com',
            'address': '123 Clean Street',
            'receipt_footer': 'Thanks for your business.',
        })

        self.assertRedirects(response, reverse('settings'))
        business = BusinessInformation.objects.get(pk=1)
        self.assertEqual(business.business_name, 'Fresh Laundry')

        receipt_response = self.client.get(
            reverse('receipt', args=[self.payment.pk])
        )
        self.assertContains(receipt_response, 'Fresh Laundry')
        self.assertContains(receipt_response, '123 Clean Street')
        self.assertContains(receipt_response, 'Thanks for your business.')

    def test_logout_clears_authenticated_session_and_redirects_home(self):
        user = get_user_model().objects.create_user(
            username='logout-test',
            password='test-password'
        )
        self.client.force_login(user)

        response = self.client.post(reverse('logout'), follow=True)

        self.assertEqual(
            response.redirect_chain,
            [(reverse('home'), 302)]
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(
            response,
            'You have been logged out successfully.'
        )

    def test_logout_rejects_get_requests(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)

    def test_sidebar_renders_logout_button_as_post_form(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'method="post"')
        self.assertContains(response, f'action="{reverse("logout")}"')
        self.assertContains(response, 'class="logout-button"')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'Logout')
