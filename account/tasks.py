from celery import shared_task
from .models import Device
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_devices():
    logger.info("HElooooo - Task started")
    print("HElooooo")
    logger.info("HElooooo - Task completed")
    # devices = Device.objects.all()
    # for device in devices:
    #     if device.is_token_expired():
    #         device.delete()
    #         print(f"Deleted device {device.id} for user {device.user.email}")
    #     else:
    #         print(f"Didn't delete device {device.id} for user {device.user.email}")

@shared_task
def add(x, y):
    print(x + y) 