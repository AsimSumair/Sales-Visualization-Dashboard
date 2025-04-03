import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg, Max, Min
from .models import DataPoint 
from .serializers import DataPointSerializer


class DataPointViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer


def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


@api_view(['GET'])
def get_filters(request):
    """Get all possible filter values from the database"""
    end_years = DataPoint.objects.values_list('end_year', flat=True).distinct().order_by('end_year')
    end_years = [year for year in end_years if year is not None]

    topics = DataPoint.objects.values_list('topic', flat=True).distinct().order_by('topic')
    topics = [topic for topic in topics if topic]

    sectors = DataPoint.objects.values_list('sector', flat=True).distinct().order_by('sector')
    sectors = [sector for sector in sectors if sector]

    regions = DataPoint.objects.values_list('region', flat=True).distinct().order_by('region')
    regions = [region for region in regions if region]

    pestles = DataPoint.objects.values_list('pestle', flat=True).distinct().order_by('pestle')
    pestles = [pestle for pestle in pestles if pestle]

    sources = DataPoint.objects.values_list('source', flat=True).distinct().order_by('source')
    sources = [source for source in sources if source]

    countries = DataPoint.objects.values_list('country', flat=True).distinct().order_by('country')
    countries = [country for country in countries if country]


    return Response({
        'end_years': end_years,
        'topics': topics,
        'sectors': sectors,
        'regions': regions,
        'pestles': pestles,
        'sources': sources,
        'countries': countries,
    })


@api_view(['GET'])
def get_filtered_data(request):
    """Get data with applied filters"""
    queryset = DataPoint.objects.all()
    print(f"Initial data count: {queryset.count()}")

    end_year = request.GET.get('end_year')
    if end_year and end_year != 'all':
        queryset = queryset.filter(end_year=end_year)
        print(f"After end_year filter: {queryset.count()}")

    topic = request.GET.get('topic')
    if topic and topic != 'all':
        queryset = queryset.filter(topic=topic)
        print(f"After topic filter: {queryset.count()}")

    sector = request.GET.get('sector')
    if sector and sector != 'all':
        queryset = queryset.filter(sector=sector)
        print(f"After sector filter: {queryset.count()}")

    region = request.GET.get('region')
    if region and region != 'all':
        queryset = queryset.filter(region=region)
        print(f"After region filter: {queryset.count()}")

    pestle = request.GET.get('pestle')
    if pestle and pestle != 'all':
        queryset = queryset.filter(pestle=pestle)
        print(f"After pestle filter: {queryset.count()}")

    source = request.GET.get('source')
    if source and source != 'all':
        queryset = queryset.filter(source=source)
        print(f"After source filter: {queryset.count()}")

    country = request.GET.get('country')
    if country and country != 'all':
        queryset = queryset.filter(country=country)
        print(f"After country filter: {queryset.count()}")

    serializer = DataPointSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_dashboard_stats(request):
    """Get statistical information for the dashboard"""
    queryset = DataPoint.objects.all()
    
    end_year = request.GET.get('end_year')
    if end_year and end_year != 'all':
        queryset = queryset.filter(end_year=end_year)

    topic = request.GET.get('topic')
    if topic and topic != 'all':
        queryset = queryset.filter(topic=topic)

    sector = request.GET.get('sector')
    if sector and sector != 'all':
        queryset = queryset.filter(sector=sector)

    region = request.GET.get('region')
    if region and region != 'all':
        queryset = queryset.filter(region=region)

    pestle = request.GET.get('pestle')
    if pestle and pestle != 'all':
        queryset = queryset.filter(pestle=pestle)

    source = request.GET.get('source')
    if source and source != 'all':
        queryset = queryset.filter(source=source)


    country = request.GET.get('country')
    if country and country != 'all':
        queryset = queryset.filter(country=country)

    intensity_avg = queryset.aggregate(Avg('intensity'))['intensity__avg'] or 0
    intensity_max = queryset.aggregate(Max('intensity'))['intensity__max'] or 0
    intensity_min = queryset.aggregate(Min('intensity'))['intensity__min'] or 0

    likelihood_avg = queryset.aggregate(Avg('likelihood'))['likelihood__avg'] or 0
    likelihood_max = queryset.aggregate(Max('likelihood'))['likelihood__max'] or 0
    likelihood_min = queryset.aggregate(Min('likelihood'))['likelihood__min'] or 0

    relevance_avg = queryset.aggregate(Avg('relevance'))['relevance__avg'] or 0
    relevance_max = queryset.aggregate(Max('relevance'))['relevance__max'] or 0
    relevance_min = queryset.aggregate(Min('relevance'))['relevance__min'] or 0

    year_data = list(queryset.values('end_year').annotate(count=Count('id')).order_by('end_year'))
    country_data = list(queryset.values('country').annotate(count=Count('id')).order_by('-count')[:10])
    topic_data = list(queryset.values('topic').annotate(count=Count('id')).order_by('-count')[:10])
    region_data = list(queryset.values('region').annotate(count=Count('id')).order_by('-count')[:10])

    intensity_by_region = list(queryset.values('region').annotate(
        avg_intensity=Avg('intensity')
    ).order_by('-avg_intensity')[:10])

    likelihood_by_topic = list(queryset.values('topic').annotate(
        avg_likelihood=Avg('likelihood')
    ).order_by('-avg_likelihood')[:10])

    relevance_by_sector = list(queryset.values('sector').annotate(
        avg_relevance=Avg('relevance')
    ).order_by('-avg_relevance')[:10])

    return Response({
        'count': queryset.count(),
        'intensity': {
            'avg': round(intensity_avg, 2),
            'max': intensity_max,
            'min': intensity_min
        },
        'likelihood': {
            'avg': round(likelihood_avg, 2),
            'max': likelihood_max,
            'min': likelihood_min
        },
        'relevance': {
            'avg': round(relevance_avg, 2),
            'max': relevance_max,
            'min': relevance_min
        },
        'year_data': year_data,
        'country_data': country_data,
        'topic_data': topic_data,
        'region_data': region_data,
        'intensity_by_region': intensity_by_region,
        'likelihood_by_topic': likelihood_by_topic,
        'relevance_by_sector': relevance_by_sector
    })



