from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import resolve_url

def safe_redirect_url(request, default_url):
    """
    بازگرداندن یک URL امن برای ریدایرکت.
    اولویت به پارامتر 'next' در GET یا POST داده می‌شود.
    اگر وجود نداشت یا امن نبود، default_url استفاده می‌شود.
    """

    # 1. بررسی پارامتر 'next' در GET یا POST
    next_url = request.GET.get("next") or request.POST.get("next")

    # 2. بررسی امن بودن URL
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    # 3. اگر next_url نبود یا امن نبود، default_url را استفاده کن
    return resolve_url(default_url)