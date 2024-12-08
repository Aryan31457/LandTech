from django.core.management.base import BaseCommand
from core.proxy_server import start_proxy_server

class Command(BaseCommand):
    help = 'Starts the socket-based proxy server.'

    def handle(self, *args, **kwargs):
        start_proxy_server()
