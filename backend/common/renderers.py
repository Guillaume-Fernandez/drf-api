from rest_framework import renderers

class CommonRenderer(renderers.AdminRenderer):
    template = 'common/admin.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        """
            Add non_field_errors to context. It will be reused by templates. 
        """
        context = super().get_context(data, accepted_media_type, renderer_context)
        context['non_field_errors'] = getattr(self, 'non_field_errors', None)
        return context

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
            Create a self.non_field_errors attribute before rendering.
            data['non_field_errors'] is defined by serializers.ValidationError(_error)
            By default AdminRenderer do not display this exception. It display only field specific exceptions thought error_form in template.
        """
        if isinstance(data, dict): # data is a list in ListView and a dict in DetailView
            error_detail = data.get('non_field_errors', None)
            if error_detail != None:
                self.non_field_errors = error_detail[0]

        ret = super().render(data, accepted_media_type, renderer_context)
        return ret

