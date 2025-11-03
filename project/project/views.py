from django.http import JsonResponse
from .celery import debug_task


def test_celery(request):
    debug_task.apply_async()
    return JsonResponse({"status": "Task sent to Celery"})
