from django.shortcuts import render
from django.db.models import Q, Count, Avg, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import GPPractices, GPDetails, GPPopulations
import json

def dashboard(request):
    """
    Main dashboard view with postcode search functionality
    """
    # Get postcode search parameter
    postcode_search = request.GET.get('postcode_search', '').strip()
    
    # Get page size parameter
    page_size = request.GET.get('page_size', '5')
    try:
        page_size = int(page_size)
        if page_size not in [5, 10, 20, 30, 50, 100]:
            page_size = 5
    except (ValueError, TypeError):
        page_size = 5
    
    # Base queryset
    practices = GPPractices.objects.all()
    
    # Apply postcode search filter
    if postcode_search:
        practices = practices.filter(
            Q(postcode__icontains=postcode_search) |
            Q(address__icontains=postcode_search)
        )
    
    # Sort by practice name for consistent results
    practices = practices.order_by('name')
    
    # Setup pagination with dynamic page size
    paginator = Paginator(practices, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Calculate additional metrics for practices on current page
    practices_data = []
    for practice in page_obj:
        # Count GPs
        gp_count = GPDetails.objects.filter(practice=practice).count()
        
        # Calculate patient-to-GP ratio
        ratio = practice.list_size / gp_count if gp_count > 0 else 0
        
        # Get population data
        populations = GPPopulations.objects.filter(practice=practice)
        total_population = 0
        for pop in populations:
            total_population += (
                pop.ages00to04 + pop.ages05to09 + pop.ages10to14 + pop.ages15to19 +
                pop.ages20to24 + pop.ages25to29 + pop.ages30to34 + pop.ages35to39 +
                pop.ages40to44 + pop.ages45to49 + pop.ages50to54 + pop.ages55to59 +
                pop.ages60to64 + pop.ages65to69 + pop.ages70to74 + pop.ages75to79 +
                pop.ages80to84 + pop.ages85plus
            )
        
        # Get gender breakdown
        male_pop = GPPopulations.objects.filter(practice=practice, sex='Male').first()
        male_population = 0
        if male_pop:
            male_population = (
                male_pop.ages00to04 + male_pop.ages05to09 + male_pop.ages10to14 + male_pop.ages15to19 +
                male_pop.ages20to24 + male_pop.ages25to29 + male_pop.ages30to34 + male_pop.ages35to39 +
                male_pop.ages40to44 + male_pop.ages45to49 + male_pop.ages50to54 + male_pop.ages55to59 +
                male_pop.ages60to64 + male_pop.ages65to69 + male_pop.ages70to74 + male_pop.ages75to79 +
                male_pop.ages80to84 + male_pop.ages85plus
            )
        
        female_pop = GPPopulations.objects.filter(practice=practice, sex='Female').first()
        female_population = 0
        if female_pop:
            female_population = (
                female_pop.ages00to04 + female_pop.ages05to09 + female_pop.ages10to14 + female_pop.ages15to19 +
                female_pop.ages20to24 + female_pop.ages25to29 + female_pop.ages30to34 + female_pop.ages35to39 +
                female_pop.ages40to44 + female_pop.ages45to49 + female_pop.ages50to54 + female_pop.ages55to59 +
                female_pop.ages60to64 + female_pop.ages65to69 + female_pop.ages70to74 + female_pop.ages75to79 +
                female_pop.ages80to84 + female_pop.ages85plus
            )
        
        practices_data.append({
            'practice': practice,
            'gp_count': gp_count,
            'patient_to_gp_ratio': round(ratio, 2),
            'total_population': total_population,
            'male_population': male_population,
            'female_population': female_population,
        })
    
    # Calculate totals for all practices (not just current page)
    all_practices = GPPractices.objects.all()
    if postcode_search:
        all_practices = all_practices.filter(
            Q(postcode__icontains=postcode_search) |
            Q(address__icontains=postcode_search)
        )
    
    total_practices = all_practices.count()
    total_gps = GPDetails.objects.filter(practice__in=all_practices).count()
    total_patients = sum(practice.list_size for practice in all_practices)
    avg_ratio = round(total_patients / total_gps, 1) if total_gps > 0 else 0
    
    context = {
        'practices_data': practices_data,
        'page_obj': page_obj,
        'total_practices': total_practices,
        'total_gps': total_gps,
        'total_patients': total_patients,
        'avg_ratio': avg_ratio,
        'current_filters': {
            'postcode_search': postcode_search,
        }
    }
    
    return render(request, 'catalog/dashboard.html', context)

def practice_detail(request, practice_code):
    """
    Detailed view for a single practice
    """
    practice = GPPractices.objects.get(practice_code=practice_code)
    gps = GPDetails.objects.filter(practice=practice)
    populations = GPPopulations.objects.filter(practice=practice)
    
    # Calculate detailed statistics
    gp_count = gps.count()
    patient_to_gp_ratio = practice.list_size / gp_count if gp_count > 0 else 0
    
    # Age group data for charts
    age_groups = ['00to04', '05to09', '10to14', '15to19', '20to24', '25to29', '30to34', '35to39',
                  '40to44', '45to49', '50to54', '55to59', '60to64', '65to69', '70to74', '75to79', '80to84', '85plus']
    
    age_data = []
    male_pop = populations.filter(sex='Male').first()
    female_pop = populations.filter(sex='Female').first()
    
    for age_group in age_groups:
        male_value = getattr(male_pop, f'ages{age_group}', 0) if male_pop else 0
        female_value = getattr(female_pop, f'ages{age_group}', 0) if female_pop else 0
        total_value = male_value + female_value
        
        age_data.append({
            'age_group': age_group.replace('to', '-'),
            'male': male_value,
            'female': female_value,
            'total': total_value
        })
    
    context = {
        'practice': practice,
        'gps': gps,
        'populations': populations,
        'gp_count': gp_count,
        'patient_to_gp_ratio': round(patient_to_gp_ratio, 2),
        'age_data': age_data,
    }
    
    return render(request, 'catalog/practice_detail.html', context)

def analytics_api(request):
    """
    API endpoint for analytics data
    """
    # Overall statistics
    total_practices = GPPractices.objects.count()
    total_gps = GPDetails.objects.count()
    total_patients = GPPractices.objects.aggregate(total=Sum('list_size'))['total'] or 0
    
    # Health board statistics
    health_board_stats = []
    for hb in GPPractices.objects.values_list('health_board', flat=True).distinct():
        if hb:
            practices = GPPractices.objects.filter(health_board=hb)
            gp_count = GPDetails.objects.filter(practice__health_board=hb).count()
            patient_count = practices.aggregate(total=Sum('list_size'))['total'] or 0
            ratio = patient_count / gp_count if gp_count > 0 else 0
            
            health_board_stats.append({
                'health_board': hb,
                'practices': practices.count(),
                'gps': gp_count,
                'patients': patient_count,
                'ratio': round(ratio, 2)
            })
    
    # Top practices by size
    top_practices = GPPractices.objects.order_by('-list_size')[:10]
    top_practices_data = []
    for practice in top_practices:
        gp_count = GPDetails.objects.filter(practice=practice).count()
        ratio = practice.list_size / gp_count if gp_count > 0 else 0
        top_practices_data.append({
            'name': practice.name,
            'list_size': practice.list_size,
            'gp_count': gp_count,
            'ratio': round(ratio, 2)
        })
    
    data = {
        'total_practices': total_practices,
        'total_gps': total_gps,
        'total_patients': total_patients,
        'health_board_stats': health_board_stats,
        'top_practices': top_practices_data
    }
    
    return JsonResponse(data)
