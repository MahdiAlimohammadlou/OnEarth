from celery import shared_task
from .models import Device

@shared_task
def remove_expired_devices():
    devices = Device.objects.all()
    if devices:
        for device in devices:
            if device.is_token_expired():
                print(f"device with id {device.id} was deleted.")
            else:
                print(f"device with id {device.id} wasn't deleted.")