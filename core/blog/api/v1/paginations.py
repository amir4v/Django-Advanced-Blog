from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MyPaginator(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total-objects": self.page.paginator.count,
                "total-pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
