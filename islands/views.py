# islands/views.py
from django.db.models import F, Func, ExpressionWrapper, FloatField, Value
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Island
from .serializers import IslandSerializer

@extend_schema(
    methods=['GET'],
    tags=['islands'],
    description='Retrieve island list sorted by distance',
    parameters=[
        OpenApiParameter(
            name='current_latitude',
            type=OpenApiTypes.NUMBER,
            location=OpenApiParameter.QUERY,
            description='Current latitude',
        ),
        OpenApiParameter(
            name='current_longitude',
            type=OpenApiTypes.NUMBER,
            location=OpenApiParameter.QUERY,
            description='Current longitude',
        ),
    ],
    responses={status.HTTP_200_OK: IslandSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def retrieve_island_list(request):
    try:
        current_latitude = float(request.query_params.get('current_latitude', 0))
        current_longitude = float(request.query_params.get('current_longitude', 0))

        # Calculate distance using Haversine formula
        earth_radius_km = 6371.0  # Earth radius in kilometers
        lat_diff = ExpressionWrapper(F('latitude') - current_latitude, output_field=FloatField())
        lon_diff = ExpressionWrapper(F('longitude') - current_longitude, output_field=FloatField())

        # Haversine formula
        hav_formula = (
            Func(lat_diff, Value(2), function='POW', output_field=FloatField()) +
            Func(Func(F('latitude'), function='COS') * Func(Value(current_latitude), function='COS'), function='*') *
            Func(lon_diff, Value(2), function='POW', output_field=FloatField()) +
            Func(Func(F('longitude'), function='SIN') * Func(Value(current_latitude), function='SIN'), function='*')
        )

        distance_expr = ExpressionWrapper(
            Func(Value(2 * earth_radius_km), function='ATAN2', arg_pos=[hav_formula]), output_field=FloatField()
        )

        islands = Island.objects.annotate(distance=distance_expr).order_by('distance')

        serializer = IslandSerializer(islands, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
