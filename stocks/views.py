# stocks/views.py
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Min, Max
from django.utils.datetime_safe import datetime
from .models import Index, DailyPrice
from .serializers import DailyPriceSerializer


class DailyPriceDateRangeView(generics.ListAPIView):
    serializer_class = DailyPriceSerializer

    def get_queryset(self):
        index_id = self.kwargs['index_id']

        # Parse start_date and end_date in the required format (YYYY-MM-DD)
        start_date_str = self.kwargs['start_date']
        end_date_str = self.kwargs['end_date']
        start_date = datetime.strptime(start_date_str, '%d-%b-%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%d-%b-%Y').strftime('%Y-%m-%d')

        queryset = DailyPrice.objects.filter(index_id=index_id, date__range=[start_date, end_date])

        # Apply filters for each column
        filters = {
            'open': self.request.query_params.get('open', None),
            'high': self.request.query_params.get('high', None),
            'low': self.request.query_params.get('low', None),
            'close': self.request.query_params.get('close', None),
            'shares_traded': self.request.query_params.get('shares_traded', None),
            'turnover': self.request.query_params.get('turnover', None),
        }

        for key, value in filters.items():
            if value is not None:
                # Use case-insensitive contains for string columns and exact match for numeric columns
                column_name = f'{key}_price' if key in ['open', 'high', 'low', 'close'] else key
                queryset = queryset.filter(**{f'{column_name}__exact': value})

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Calculate data ranges
        ranges = {
            "open": {"lowest": queryset.aggregate(lowest=Min('open_price'))['lowest'],
                     "highest": queryset.aggregate(highest=Max('open_price'))['highest']},
            "high": {"lowest": queryset.aggregate(lowest=Min('high_price'))['lowest'],
                     "highest": queryset.aggregate(highest=Max('high_price'))['highest']},
            "low": {"lowest": queryset.aggregate(lowest=Min('low_price'))['lowest'],
                    "highest": queryset.aggregate(highest=Max('low_price'))['highest']},
            "close": {"lowest": queryset.aggregate(lowest=Min('close_price'))['lowest'],
                      "highest": queryset.aggregate(highest=Max('close_price'))['highest']},
            "shares_traded": {"lowest": queryset.aggregate(lowest=Min('shares_traded'))['lowest'],
                              "highest": queryset.aggregate(highest=Max('shares_traded'))['highest']},
            "turnover": {"lowest": queryset.aggregate(lowest=Min('turnover'))['lowest'],
                         "highest": queryset.aggregate(highest=Max('turnover'))['highest']}
        }

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                "start-date": self.kwargs['start_date'],
                "end-date": self.kwargs['end_date'],
                "data": serializer.data,
                "pagination": {
                    "page": self.page.paginator.page,
                    "total_pages": self.page.paginator.num_pages,
                    "total_rows": self.page.paginator.count
                },
                "ranges": ranges
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "start-date": self.kwargs['start_date'],
            "end-date": self.kwargs['end_date'],
            "data": serializer.data,
            "pagination": {
                "page": 1,  # Assuming no pagination for non-paginated response
                "total_pages": 1,
                "total_rows": len(serializer.data)
            },
            "ranges": ranges
        }
        return Response(response_data)
