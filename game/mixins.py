import logging


class LoggingMixin:
    """
    Provides full logging of requests.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('django.request')

    def initial(self, request, *args, **kwargs):
        try:
            self.logger.debug(f"{request.method} {request.get_full_path()}")

        except Exception:
            self.logger.exception("Error logging request data")
        super().initial(request, *args, **kwargs)
