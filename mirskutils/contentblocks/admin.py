
import os
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.conf import settings
from tinymce.widgets import TinyMCE

from accelerator.models import ContentBlock, ContentLink


class TitleWithSlugWidget(forms.TextInput):

    class Media:
        js = ('js/lib/jquery-1.8.3.min.js', 'js/lib/jquery.slugify.js', 'js/lib/jquery-ui-1.9.2.custom.js',)    

    def render(self, name, value, attrs=None):
        slug = ''
        if value:
            slug = slugify(value)

        field = super(TitleWithSlugWidget,self).render(name, value, attrs)
        slug = '<p><em>Slug: </em><span id="slug-%(name)s">%(init)s</span></p><script>$(function(){ $("#slug-%(name)s").slugify("#id_%(name)s"); });</script>' % {'name':name, 'init':slug}

        return mark_safe("%s %s" % (field, slug))



        #@property
        #def media(self):
            #return forms.Media(js=('/static/js/lib/jquery.slugify.js'))      



class ContentBlockAdminForm(forms.ModelForm):

    title = forms.CharField(widget=TitleWithSlugWidget())
    #kind = forms.ChoiceField(widget=forms.RadioSelect, choices=ContentBlock.KINDS.choices(), )

    video = forms.CharField(widget=forms.TextInput, required=False)
    #text = forms.CharField(widget=TinyMCE(attrs={'cols': 200, 'rows': 100}, mce_attrs={'height':'300','width':'375'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':80, 'rows':40}), required=False)

    photo = forms.ImageField(required=False)
    
    size = forms.ChoiceField(widget=forms.RadioSelect(), choices=ContentBlock.SIZES.choices(), initial=ContentBlock.SIZES.original)

    order = []

    class Meta:
        model = ContentBlock
        exclude = ('slug','content',)

    # from :: http://stackoverflow.com/questions/2854350/django-admin-many-to-many-listbox-doesnt-show-up-with-a-through-parameter
    contains = forms.ModelMultipleChoiceField(required=False,
                                              queryset=ContentBlock.objects.all(),
                                              #widget=FilteredSelectMultiple(_('contains'), False, attrs={'rows':'10'})
                                              )    

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault('initial', {})
        
        if 'instance' in kwargs:
            initial['contains'] = [b.contained.pk for b in kwargs['instance'].contains.order_by('rank', 'contained__title')]
            if kwargs['instance'].kind == ContentBlock.KINDS.video:
                initial['video'] = kwargs['instance'].content.get('video_url','')
            if kwargs['instance'].kind == ContentBlock.KINDS.text:
                initial['text'] = kwargs['instance'].content.get('text','')
            if kwargs['instance'].kind in [ContentBlock.KINDS.photo, ContentBlock.KINDS.video, ContentBlock.KINDS.text] and kwargs['instance'].content.get('photo',''):
                class FakeField(object):
                    storage = default_storage
                initial['photo'] = FieldFile(None, FakeField, kwargs['instance'].content.get('photo',''))
                initial['size'] = kwargs['instance'].content.get('size',ContentBlock.SIZES.original)
        forms.ModelForm.__init__(self, *args, **kwargs)        
        self.fields['contains'].queryset = ContentBlock.objects.exclude(pk=self.instance.id).exclude(kind=ContentBlock.KINDS.container)
        if initial.get('contains',[]):
            ranking = 'FIELD(`id`, %s)' % ','.join(str(id) for id in initial['contains'])            
            self.fields['contains'].queryset = self.fields['contains'].queryset.extra( select={'ranking':ranking}, order_by=('ranking',))

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit)

        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()

            blocks = [b for b in self.cleaned_data['contains']]

            for bf in instance.contains.all():
                if bf.contained not in blocks:
                    bf.delete()
                else:
                    blocks.remove(bf.contained)

            for b in blocks:
                ContentLink.objects.create(container=instance, contained=b)

        self.save_m2m = save_m2m
        
        instance.content = instance.content or {}

        if self.cleaned_data['kind'] == ContentBlock.KINDS.video:
            instance.content.update({'video_url':self.cleaned_data['video']})
        if self.cleaned_data['kind'] == ContentBlock.KINDS.text:
            instance.content.update({'text':self.cleaned_data['text']})
        if self.cleaned_data['kind'] in [ContentBlock.KINDS.photo, ContentBlock.KINDS.video, ContentBlock.KINDS.text]:
            #instance.content = { 'photo':'' }
            path = instance.content.get('photo','')
            size = self.cleaned_data['size']
            if self.cleaned_data['photo'] and 'photo' in self.changed_data:
                fn = os.path.basename(self.cleaned_data['photo'].name)
                path = default_storage.save("content/%s" % fn, self.cleaned_data['photo'])
            elif not self.cleaned_data['photo']:
                path = ''
                size = ContentBlock.SIZES.original
            instance.content.update({ 'photo':path, 'size': size})
        return instance

    def clean_title(self):
        title = self.cleaned_data['title']
        if ContentBlock.objects.exclude(pk=self.instance.id).filter(slug=slugify(title)).exists():
            raise forms.ValidationError("Title produces a slug that already exists")
        return title



class ContentBlockAdmin(admin.ModelAdmin):

    #filter_horizontal = ('blocks',)
    form = ContentBlockAdminForm
    radio_fields = {'kind':admin.HORIZONTAL}


    change_form_template = 'accelerator/admin/content_block_change_form.html'
    list_filter = ('kind','category',)
    search_fields = ('title',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        ranking = request.POST.getlist('contains')
        result = super(ContentBlockAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

        cb = self.model.objects.get(pk=object_id)

        for i in range(0,len(ranking)):
            if cb.contains.filter(contained__pk=ranking[i]).exists():
                elem = cb.contains.get(contained__pk=ranking[i])
                elem.rank = i
                elem.save()
        return result


    class Meta:
        model = ContentBlock


admin.site.register(ContentBlock, ContentBlockAdmin)




