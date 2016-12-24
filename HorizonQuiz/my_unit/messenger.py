from push_notifications.models import APNSDevice, GCMDevice
# from HorizonBackEnd import *


def send_this_message(msg, apns_token='68409f9f2fad8bf4cbd5d1e13a559d756d4a1d23'):
    device = APNSDevice.objects.get(registration_id=apns_token)
    device.send_message(msg)  # Alert message may only be sent as text.
    device.send_message(None, badge=5)  # No alerts but with badge.
    device.send_message(None, badge=1, extra={"foo": "bar"})  # Silent message with badge and added custom data.
