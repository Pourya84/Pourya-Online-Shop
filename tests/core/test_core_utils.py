import pytest
from django.http import HttpRequest
from core.utils import safe_redirect_url

@pytest.mark.unit
class TestUtils:
    def test_safe_redirect_url_with_next(self):
        request = HttpRequest()
        request.GET = {"next": "/store/"}
        request.get_host = lambda: "127.0.0.1"
        result = safe_redirect_url(request, "store:store_panel")
        assert result == "/store/"

    def test_safe_redirect_url_without_next(self):
        request = HttpRequest()
        request.get_host = lambda: "127.0.0.1"
        result = safe_redirect_url(request, "store:store_panel")
        assert result == "/store/"  # resolve_url default

    def test_safe_redirect_url_block_unsafe(self):
        request = HttpRequest()
        request.GET = {"next": "https://malicious.com"}
        request.get_host = lambda: "127.0.0.1"
        result = safe_redirect_url(request, "store:store_panel")
        assert result != "https://malicious.com"
        assert result == "/store/"