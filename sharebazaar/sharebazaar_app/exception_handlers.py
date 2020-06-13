from django.shortcuts import render
from rest_framework.views import exception_handler


def handler400(request, exception):
    return render(request, template_name='bad_request_error.html')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == 403:
            return render(request=context.get("request"), template_name="authentication_error.html")
    return response
