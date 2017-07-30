from django.http import Http404


class MultiplesQueriesMixin(object):

    def get_queryset(self):
        filter = {}
        query_params_size = len(self.request.query_params)
        if query_params_size > 0:
            for field in self.filter_fields:
                param = self.request.query_params.get(field, None)
                if param:
                    filter[field] = param
                else:
                    pass
            if 'channel__description' in filter.keys() and query_params_size == 1:
                filter['lft'] = 1
                self.Meta.model.objects.filter(**filter)

            queryset = self.Meta.model.objects.filter(**filter)
            if not queryset.exists():
                raise Http404
            return queryset
        return self.queryset