from . import utils


class AppContext(object):
    """
    A singleton object to scrape META data from HTTP Request Header

    usage:
    ip_address = AppContext.instance().ip_address
    app_version = AppContext.instance().app_version

    """
    __instance = None

    def __init__(self):
        if AppContext.__instance is not None:
            return
        self._user = None
        self._ip_address = None
        self._app_version = None
        self._is_ios = False
        self._is_android = False
        self._device_id = None
        self._request = None

        AppContext.__instance = self

    @staticmethod
    def instance():
        if AppContext.__instance is None:
            AppContext()
        return AppContext.__instance

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def app_version(self):
        return self._app_version

    @app_version.setter
    def app_version(self, value):
        self._app_version = value

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    @property
    def is_ios(self):
        return self._is_ios

    @is_ios.setter
    def is_ios(self, value):
        self._is_ios = value

    @property
    def is_android(self):
        return self._is_android

    @is_android.setter
    def is_android(self, value):
        self._is_android = value

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self._request = value


class AppContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        context = AppContext.instance()
        context.user = request.user
        context.request = request
        context.app_version = utils.get_app_version(request=request)
        context.device_id = utils.get_device_id(request=request)
        context.ip_address = utils.get_ip_address(request=request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

