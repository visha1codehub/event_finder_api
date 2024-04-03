from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):


    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('events', data),
            ('page', self.page.number),
            ('pageSize', self.page_size),
            ('totalEvents', self.page.paginator.count),
            ('totalPages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ]))
