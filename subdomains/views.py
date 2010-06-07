from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from urllib2 import urlparse

from subdomains import paypal

class PaypalStart(object):
    """
    This class is a class based - generic view, which makes handling paypal simple.
    To use this view, at the minimum, you need to Subclass PaypalStart and override its
    __init__, and add `success_url`, `failure_url` and `amount` to self.
    You should also override `process_request` to do your application specific action,
    However at this point you should not do things like generate a license key, as you have been authorised, but not paid.
    `process_request` should return a dictionary.
    """
    
    
    def __init__(self):
        super(PaypalStart, self).__init__()
    
    def get_success_url(self, request, *args, **kwargs):
        return _url_to_absolute_uri(self.success_url, request)
    
    def get_failure_url(self, request, *args, **kwargs):
        try:
            return _url_to_absolute_uri(self.failure_url, request)
        except AttributeError:
            return request.build_absolute_uri()
    
    def get_amount(self, request, *args, **kwargs):
        return self.amount
    
    def get_template(self, request, *args, **kwargs):
        return self.template
    
    def do_get(self, request, *args, **kwargs):
        success_url = self.get_success_url(request, *args, **kwargs)
        failure_url = self.get_failure_url(request, *args, **kwargs)
        amount = self.get_amount(request, *args, **kwargs)
        pp = paypal.PayPal()
        token = pp.SetExpressCheckout(amount, success_url, failure_url, )
        paypal_url = pp.PAYPAL_URL + token
        return {'token': token, 'paypal_url': paypal_url}
    
    def process_request(self, request, *args, **kwargs):
        """Extra things which you might want to pass to the template,
        do proces would take the arguments passed to the view function
        Ahd return a dictionary"""
        return {}
        
    def __call__(self, request, *args, **kwargs):
        payload = self.do_get(request)
        payload.update(self.process_request(request, *args, **kwargs))
        return render_to_response(self.get_template(request), payload, RequestContext(request))
    
class PaypalResponse(object):
    """
    This is a class based genric view to Handle the GetExpressCheckoutDetails and DoExpressCheckoutPayment.
    At the minimum you should Subclass this class and add the variables in __init__
    template_GET = ''
    redirect_url_GET_success = ''
    redirect_url_GET_failure = ''
    amount = 0#A non zero number
    
    This view proceeds in two stages.
    A. GET to show user's details. During POST do actual checkout.
    
    A. GET
    1. This must be called after PaypalStart based class has been used to do SetExpressCheckOut.
    2. Populate the first_name, last_name, amount, token and payer_ID in templates. Get this data from GetExpressCheckOutDetails.
    3. Render the template referred to be template_GET.
    
    B. POST
    1. After user confirms the data in GET, do the post.
    2. Do CheckOut  by calling DoExpressCheckoutPayment on Paypal.
    3. If Paypal returns an ack of success, call process_request_POST.
    4. process_request_POST should be the main application login in your app.
    Here you do things like genrate a license key, activate emembership etc.
    5. On Suceess redirect to values returned by get_redirect_url_POST_success.
    6. On failure return to get_redirect_url_POST_failure.
    """
    def __init__(self):
        super(PaypalResponse, self).__init__()
        
    def get_token(self, request, *args, **kwargs):
        "Get token by getting it out of GET/POST. Should not generally Override this."
        token = request.GET.get('token', '')
        if token:
            return token
        else:
            return request.POST.get('token', '')
    
    def get_PayerID(self, request, *args, **kwargs):
        "Get PayerID by getting it out of GET/POST. Should not generally Override this."
        PayerID = request.GET.get('PayerID', '')
        if PayerID:
            return PayerID
        else:
            return request.POST.get('PayerID', '')
    
    def get_template_GET(self, request, *args, **kwargs):
        "Get the template to use during GET. Override if you need to do something _interesting_ with the template to be rendred."
        return self.template_GET
    
    def get_redirect_url_POST_success(self, request, *args, **kwargs):
        "Get the url to redirect after POST results in successful checkout."
        return self.redirect_url_GET_success
    
    def get_redirect_url_POST_failure(self, request, *args, **kwargs):
        "Get the url to redirect if POST does not results in successful checkout."
        return self.redirect_url_POST_failure
    
    def get_amount(self, request, *args, **kwargs):
        "Return the amount. In simple cases it would be easiest to set this in __init__"
        return self.amount
    
    def do_get(self, request, *args, **kwargs):
        "Do GetExpressCheckoutDetails on PayPal, and populate details in a dictionary."
        token = self.get_token(request, *args, **kwargs)
        PayerID = self.get_PayerID(request, *args, **kwargs)
        pp = paypal.PayPal()
        paypal_details = pp.GetExpressCheckoutDetails(token, return_all = True)
        payload = {}
        if 'Success' in paypal_details['ACK']:
            payload['ack'] = True
            token = paypal_details['TOKEN'][0]
            first_name = paypal_details['FIRSTNAME'][0]
            last_name = paypal_details['LASTNAME'][0]
            amt = paypal_details['AMT'][0]
            payload_update  = {'first_name':first_name, 'last_name':last_name, 'amt':amt, 'token': token, 'PayerID': PayerID}
            payload.update(payload_update)
        else:
            payload['ack'] = False
        return payload
    
    def do_post(self, request, *args, **kwargs):
        "Do DoExpressCheckoutPayment on Paypal to get the money and populate the respons ein a dictionary."
        token = self.get_token(request, *args, **kwargs)
        PayerID = self.get_PayerID(request, *args, **kwargs)
        amount = self.get_amount(request, *args, **kwargs)
        pp = paypal.PayPal()
        payment_details = pp.DoExpressCheckoutPayment(token = token, payer_id = PayerID, amt = amount)
        return payment_details     
        
    def process_request_GET(self, request, *args, **kwargs):
        "Override this if you want to populate any extra items in your templates, or want to take any extra action in GET"
        return {}
    
    def process_request_POST(self, request, *args, **kwargs):
        """Most of the time you would want to override this.
        This would only be called if your checkout was succesful and Paypal has paid you money.
        Here do thngs like generate license key etc.
        """
        return {}
    
    def __call__(self, request, *args, **kwargs):
        "Call appropriate methods. Do not overide this."
        if request.method == 'GET':
            payload = self.do_get(request, *args, **kwargs)
            payload.update(self.process_request_GET(request, *args, **kwargs))
            return render_to_response(self.get_template_GET(request), payload, RequestContext(request))
        if request.method == 'POST':
            payload = self.do_post(request, *args, **kwargs)
            if 'Success' in payload['ACK']:
                self.process_request_POST(request, *args, **kwargs)
                return HttpResponseRedirect(self.get_redirect_url_POST_success(request, *args, **kwargs))
            else:
                return HttpResponseRedirect(self.get_redirect_url_POST_failure(request, *args, **kwargs))
            return render_to_response(self.get_template_GET(request), payload, RequestContext(request))
        
def _url_to_absolute_uri(url, request):
    """Convert /bar/baz/ to maybe http://bar.foo.tld/bar/baz/
    Does not modify if starts with http/https.
    """
    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        bits = urlparse.urlparse(request.build_absolute_uri())
        absolute_uri = '%s://%s%s '% (bits.scheme, bits.netloc, url)
        return absolute_uri
    
