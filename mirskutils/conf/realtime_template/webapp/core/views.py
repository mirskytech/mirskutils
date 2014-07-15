from django import http
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template.context import Context


def server_fault(request, template_name='500.html'):
    
    t = loader.get_template(template_name)
    
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL        
    }
    
    return http.HttpResponseServerError(t.render(Context(d)))

def not_found(request, template_name='404.html'):
    
    t = loader.get_template(template_name)
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL
    }
    return http.HttpResponseNotFound(t.render(Context(d)))

def permission_denied(request, template_name='403.html'):
    
    t = loader.get_template(template_name)
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL
    }
    return http.HttpResponseNotFound(t.render(Context(d)))




from django.http import StreamingHttpResponse


# class Message(model.Model):
#     content = model.TextField()


class StreamExample1(View):
    
    streams = []
    
    def __init__(self):
        pass
    
    def _iterator(self, user):
        
        yield json.dumps({'message':'stream initialization'})
        
        while True:
            gevent.sleep(10)
            messages = Message.objects.filter(user__pk=user.pk)
            for message in messages:
                yield json.dumps({'message':message.content})
            messages.delete()


    def get(self, request, script_id, **kwargs):
        return StreamingHttpResponse(self._iterator(request.user))

# issues: lots of time spent checking a database and doing nothing. 



from gevent.queue import Queue

__streams = []

def send_message_example2(message):
    
    for stream in __streams:
        stream.put(message)

class StreamExample2(View):
        
    def __init__(self):
        pass
    
    def _iterator(self, queue):
        
        yield json.dumps({'message':'stream initialization'})
        
        while True:
            message = queue.get()
            yield json.dumps({'message':message})
            # yield self.send_msg('keepalive', 'keepalive')

    def get(self, request):
        
        queue = Queue()
        __streams.append(queue)

        return StreamingHttpResponse(self._iterator(queue))
    
# issues : not very clean api    
    
    
    
# stream3 = StreamExample3.as_views()
# stream3.send_message()
    
class StreamExample3(View):
    
    streams = {}
    
    def __init__(self):
        pass
    
    def _iterator(self, queue):
        
        yield json.dumps({'message':'stream initialization'})
        
        while True:
            message = queue.get()
            yield json.dumps({'message':message})
            # yield self.send_msg('keepalive', 'keepalive')
            
    def send_message(message):
        for queue in self.streams.values():
            queue.put(message)

    def get(self, request):
        
        queue = self.streams.get(request.user.pk, Queue())
        self.streams[request.user.pk] = queue

        return StreamingHttpResponse(self._iterator(queue))    
    
# issues : still not very clean on the api

    
    
