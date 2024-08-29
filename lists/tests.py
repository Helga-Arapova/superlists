from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from lists.views import home_page


def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddleware[^>]*>', '', text)
# Create your tests here.


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  #
        response = home_page(request)  #
        expected_html = render_to_string('home.html')
        decoded_response_without_csrf=remove_csrf_tag(response.content.decode())
        self.assertEqual(decoded_response_without_csrf, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request=HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('home.html',
                                         {'new_item_text': 'A new list item'})
        decoded_response_without_csrf=remove_csrf_tag(response.content.decode())
        self.assertEqual(decoded_response_without_csrf,expected_html)

