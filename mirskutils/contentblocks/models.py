from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from mirskutils.models import Konstants,K
from mirskutils.templatetags.mirskutils_img import srcThumbnail
from mirskutils.shortcuts import sign_s3_url

from jsonfield.fields import JSONField

from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe as ms


class ContentBlock(models.Model):
    
    KINDS = Konstants(
        K(hidden=1, label='hidden'),
        K(video=2, label='video'),
        K(text=3, label='text'),
        K(container=4, label='container'),
        K(photo=5, label='photo')
    )
    
    CATEGORY = Konstants(
        K(none=0, label='none'),
        K(type2type=1, label='type-to-type'),
        K(resource=2, label='resource'),
        K(coaching=3, label='coaching'),
        K(info=4, label='info'),
        K(verifier=5, label='verifier'),
        K(public=6, label='public'),
        K(testimonial=7, label='testimonial'),
        K(landing=8, label='landing')
        
    )
    
    SIZES = Konstants(
        K(original=0, label='original'),
        K(small=150, label='small'),
        K(medium=300, label='medium'),
        K(large=500, label='large'))
    
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    kind = models.IntegerField(choices=KINDS.choices(), default=KINDS.text)
    category = models.IntegerField(choices=CATEGORY.choices(), default=CATEGORY.none)
    
    content = JSONField(default=lambda:{'text':'', 'video':''})

    blocks = models.ManyToManyField('ContentBlock', through='ContentLink')
        
    def save(self, *args, **kwargs):        
        self.slug = slugify(self.title)
        super(ContentBlock, self).save(*args, **kwargs)     
        
    def __unicode__(self):
        if self.kind == self.KINDS.container:
            return "%s (%s : %s)" % (self.title, self.KINDS[self.kind], self.blocks.count())
        return "%s (%s, %s)" % (self.title, self.CATEGORY[self.category], self.KINDS[self.kind])
    
    def is_empty(self):
        return not self.get('text','') and not len(self.get('video',[])) and self.get('content','') and len(self.contains.all())
    
    def get_url(self):
        return reverse('accelerator-block', kwargs={'slug':self.slug})
    
    def render(self):
        
        photo = None
        if self.kind in [self.KINDS.text, self.KINDS.photo, self.KINDS.video] and self.content.get('photo',''):
            path = "%s%s" % (settings.MEDIA_URL, self.content['photo'])
            if int(self.content.get('size',self.SIZES.original)) != self.SIZES.original:
                path = srcThumbnail(path, int(self.content['size'])+65, 0)
            photo = { 'slug':self.slug, 'media':settings.MEDIA_URL, 'path': path }
            
        if self.kind == self.KINDS.text:
            rendered = """<p>%(text)s</p>""" % {'text':self.content.get('text','')}
            if photo:
                rendered = "<img src='%(path)s' />" % photo + rendered
            return ms(rendered)
        elif self.kind == self.KINDS.video:
            videos = self.content.get('video_url','').split(',')
            js = ["{url:'mp4:%s', autoPlay:%s}" % (sign_s3_url(v,10000), 'false' if not i else 'true') for i, v in enumerate(videos) if v]
            if photo:
                splash = "{url:'%(path)s', scaling:'orig', autoPlay:true}" % photo
                js.insert(0,splash)
            
            rendered = """<a href='#' class='video-container' id='video-%(id)s'></a>
            <div class="clips" style="display:none"><a href="${url}">video</a></div>
            <script>window.onload = function() { typecoach.player_init('video-%(id)s', [%(array)s]); }</script>
            """ % { 'id':self.pk, 'array': ','.join(js) }
            return ms(rendered)
        
        elif self.kind == self.KINDS.container:
            return ms("".join([b.contained.render() for b in self.contains.order_by('rank')]))
        elif self.kind == self.KINDS.photo:
            return ms("<img src='%(path)s' />" % photo)
        return ""

    def as_divs(self):
        if self.kind == self.KINDS.container:
            items = [b.as_divs() for b in self.blocks.order_by('containers__rank') ] 
            
            #items = [ms("<div class='tc%(kind)s' id='%(slug)s'>%(render)s</div>" % p) for p in params]
            return ms("<div class='tc-container' id='%s'>%s</div>" % (self.slug, ("".join(items))))
        return ms("<div class='%(kind)s' id='%(slug)s'>%(render)s</div><div class='%(kind)s spacer'></div>" % { 'kind' : self.KINDS[self.kind],
                                                                                                                'slug' : self.slug,
                                                                                                                'render':self.render() })
        
    def as_ul(self):
        if self.kind == self.KINDS.container:
            items = [ms("<li id='%s'>%s</li>" % (b.slug, b.render())) for b in self.blocks.all()]
            return ms("".join(items))
        return ms("<li id='%s'>%s</li>" % (self.slug, self.render()))
    
    def as_toc(self):
        if self.kind == self.KINDS.container:
            items = [ms("<li id='%s'><a href='%s'>%s</a></li>" % (b.slug, b.get_url(), b.title)) for b in self.blocks.all()]
            return ms("".join(items))
        return ms("<li id='%s'>%s</li>" % (self.slug, self.render()))       
    
    #def as_elems(self):
        #if self.kind == self.KINDS.container:
            #return [b.as_elems() for b in self.blocks.all()]
        #elif self.kind == self.KINDS.photo:
            #return { 'kind':'photo', 'photo':self.content['photo'], 'rendered':self.render() }
        #elif self.kind == self.KINDS.video:
            #return { 'kind':'video', 'video':self.content['photo'], self.conteint[''])
        


class ContentLink(models.Model):
    
    container = models.ForeignKey('ContentBlock', related_name="contains")
    contained = models.ForeignKey('ContentBlock', related_name="containers")
    rank = models.PositiveIntegerField(default=0)

    