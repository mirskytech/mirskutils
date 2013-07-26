import os

from PIL import Image, ImageOps, ImageFile, ImageFilter
from StringIO import StringIO
#from cStringIO import StringIO as cStringIO
from django.conf import settings
from django.core.files.storage import default_storage
from django import template
from urllib import urlopen, urlencode, quote, unquote
from django.core.files.base import ContentFile

register = template.Library()

@register.simple_tag
def srcThumbnail(image_url, width, height, quality=95, rotate=0, blur=0):
    
    storage = getattr(settings, 'THUMB_STORAGE', default_storage)
    storage_url = getattr(settings, 'THUMB_MEDIA_URL', settings.MEDIA_URL)
    local = default_storage
    
    if not image_url:
        return ""
    
    image_url = unquote(unicode(image_url))
    
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
        
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")    
    #if we're rotating, needs to be transparent ie png
    if rotate:
        image_ext = ".png"
        filetype = "PNG"
    
    thumb_uri = "%s/%s-%sx%s-%s-%s%s" % (image_dir, image_prefix, width, height, rotate, blur, image_ext)
    
    # if the thumbnail exists, then return the full url path
    if storage.exists(thumb_uri):
        return '%s%s' % (storage_url, quote(thumb_uri))
        
    # if not, let's find the original image    
    image = None

    # check locally
    if local.exists(image_url):
        image = Image.open(local.open(image_url))
    else:        
        # check on s3 ( TODO: we should really check the url to see if it
        #is a playbook url or coming from somewhere else. eg. youtube api image)
        if storage.exists(image_url):
            # image on s3
            file = StringIO()
            k.get_file(file)
            file.seek(0)
            image = Image.open(file)        
            
    if not image:
        # can't find the image, just return the original url
        return '%s%s' % (settings.MEDIA_URL, image_url)
    
    # let's resize! (from mezzanine tags)
    image_info = image.info    
    width = int(width)
    height = int(height)
    rotate = int(rotate)
    blur = int(blur)

    # Set dimensions.
    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    try:
        if image.mode not in ("L", "RGBA"):
            image = image.convert("RGBA")
        # Required for progressive jpgs.
        ImageFile.MAXBLOCK = image.size[0] * image.size[1]    
        
        # instead of saving locally, upload it to s3
        thumb_io = StringIO()
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)    
        if rotate:
            image = image.rotate(rotate, resample=Image.BILINEAR, expand=1)
        if blur:
            image = image.filter(BlurImageFilter(radius=blur))
        #image.save('/home/andrew/temp/myimg.jpg', filetype, quality=quality, **image_info)
        image.save(thumb_io, filetype, quality=quality)
        #thumb_file = InMemoryUploadedFile(thumb_io, None, image_name, 'image/%s' % filetype.lower(), thumb_io.len, None)
        thumb_file = ContentFile(thumb_io.getvalue())
        thumb_uri = storage.save(thumb_uri, thumb_file)
    except Exception as e:    
        ## if an error occured for some reason, no cleanup necessary (?)
        return '%s%s' % (settings.MEDIA_URL, image_url)
    
    return '%s%s' % (storage_url, quote(thumb_uri))


@register.simple_tag
def cssThumbnail(image_url, width, height, quality=95, rotate=0, blur=0):
    
    thumb_url = srcThumbnail(image_url, width, height, quality, rotate, blur)
    
    return "style=\"background-image:url('%s')\"" %  thumb_url if thumb_url else ""