# https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
# https://stackoverflow.com/questions/1263451/python-decorators-in-classes

import requests
import functools

class Singleton_Strict:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton_Strict, cls).__new__(cls)
        return cls.instance

class KivyApi(Singleton_Strict):
    result = None
    error = None
    
    # if there was error in some method this decorator is called.
    def catch_exception(f):
        @functools.wraps(f)
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                KivyApi.instance.error = e
                return KivyApi.instance
        return func

    def catch(self, func):
        if not self.error:
            return ''
        return func(self.error)

    def clear_properties(self):
        self.error = None
        self.result = None

    @catch_exception
    def get(self, **kwargs):
        """
            variables:
            - headers, content, text, encoding, status_code, url, ok, links
            methods:
            - json, 
            other objects:
            - cookies, request, raw
        """
        self.clear_properties()
        url = kwargs.get('url', '')
        headers = kwargs.get('headers', {})
        params = kwargs.get('params', {})

        self.result = requests.get(**kwargs)
        # self.result = requests.get('8.8.8.8')

        return self.instance

    @catch_exception
    def post(self, **kwargs):
        self.clear_properties()
        self.result = requests.post(**kwargs)
        return self.instance
    
    @catch_exception
    def put(self, **kwargs):
        self.clear_properties()
        self.result = requests.put(**kwargs)
        return self.instance

    @catch_exception
    def delete(self, **kwargs):
        self.clear_properties()
        self.result = requests.delete(**kwargs)
        return self.instance

    @catch_exception
    def head(self, **kwargs):
        self.clear_properties()
        self.result = requests.head(**kwargs)
        return self.instance

    @catch_exception
    def options(self, **kwargs):
        self.clear_properties()
        self.result = requests.options(**kwargs)
        return self.instance

    @catch_exception
    def before(self, func):
        if not self.error:
            func(self.result)        
        return self.instance

    @catch_exception
    def after(self, func):
        if not self.error:
            func(self.result)        
        return self.instance

################## EXAMPLE ###################
kivyapi = KivyApi()

# github api get
# url_get = "https://api.github.com/users/VictorManhani"
# kivyapi.get(
#     url = url_get
# ).after(
#     lambda response: print(response.json()['login'])
# ).catch(
#     lambda error: print(error)
# )

# jsonplaceholder api post
# url_post = "https://jsonplaceholder.typicode.com/posts"
# kivyapi.post(
#     url_post
# ).after(
#     lambda response: print(response.json())
# ).catch(
#     lambda error: print(error)
# )
