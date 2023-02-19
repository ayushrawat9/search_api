from django.shortcuts import render
import requests
from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit


# @ratelimit(key='ip', rate='5/m')
# @ratelimit(key='ip', rate='100/d')
def search_questions(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'relevance')
    order = request.GET.get('order', 'desc')
    accepted = request.GET.get('accepted','')
    answers = request.GET.get('answers',0)
    title = request.GET.get('title')
    results = []
    if query:
        # Check if the data is already in cache
        cache_key = f"{query}"
        cache_data = cache.get(cache_key)
        if cache_data:
            print("CACHED")
            results = cache_data
        else:
            # Make a request to the API
            api_key = 'api-key'
            url = f'https://api.stackexchange.com/2.3/search/advanced?key={api_key}&site=stackoverflow&q={query}&sort={sort}&order={order}&accepted={accepted}&answers={answers}&title={title}'
            response = requests.get(url)
            # response = requests.get('https://s3.us-east-2.wasabisys.com/akshit/dataset-django/ft_assignment.json')
            data = response.json()
            print(data)
            results=data['items']
            # Cache the results for 5 minutes
            cache.set(cache_key, results, 300)

        # Show 10 search results per page
        paginator = Paginator(results, 10)  
        page_number = request.GET.get("page")
        page_size = int(request.GET.get("page_size", 1))
        page_obj = paginator.get_page(page_number)
        context = {
            'query': query,
            'results': [
                        obj for obj in page_obj
            ],
            'page':page_number,
            'page_size':page_size,
            'num_pages':paginator.num_pages,
            'total_results':paginator.count,
        }
        print(context)

    return JsonResponse(context,safe=False)











@ratelimit(key='ip', rate='5/m')
@ratelimit(key='ip', rate='100/d')
def search_questions1(request):
    query = request.GET.get('q', '')
    
    results = []
    if query:
        # Check if the data is already in cache
        cache_key = f"{query}"
        cache_data = cache.get(cache_key)
        if cache_data:
            print("CACHED")
            results = cache_data
        else:
            # check the search limit per minute
            # search_limit_per_min = request.session.get('search_limit_per_min', 0)
            # request.session['search_limit_per_min'] = search_limit_per_min + 1

            # print(search_limit_per_min)
            # if search_limit_per_min >= SEARCH_LIMIT_PER_MIN:
            #     return JsonResponse({'error': 'Search limit per minute exceeded.'})
            # Make a request to the API
            api_key = 'your-api-key'
            url = f'https://api.stackexchange.com/2.3/search/advanced?key={api_key}&site=stackoverflow&q={query}'
            # response = requests.get(url)
            # response = requests.get('https://s3.us-east-2.wasabisys.com/akshit/dataset-django/ft_assignment.json')
            # data = response.json()
            results = {
                "package_id": "com.sharekaro.shareit",
                "app_name": "Share Karo",
                "date_wise_metrics": {
                "daily_active_users": {
                "12-07-2022": 35602,
                "11-07-2022": 66595,
                "10-07-2022": 28767,
                "09-07-2022": 22944,
                "08-07-2022": 54836,
                "12-07-2022": 35602,
                "11-07-2022": 66595,
                "10-07-2022": 28767,
                "09-07-2022": 22944,
                "08-07-2022": 54836,
                "12-07-2022": 35602,
                "11-07-2022": 66595,
                "10-07-2022": 28767,
                "09-07-2022": 22944,
                "08-07-2022": 54836,}
                        }   }
            # search = Search(query=query, data=data)
            # search.save()
            # return render(request,'search_result.html',{'data':data})
            # Cache the results for 5 minutes
            cache.set(cache_key, results, 300)
        # Show 10 search results per page
        results = ["results {}".format(i) for i in range(20)]
        paginator = Paginator(results, 5)  
        print(paginator)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'query': query,
            'results': page_obj,
        }

        
    return render(request, 'search_form.html', context)

def search_questions2(request):
    # Get query parameters
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'relevance')
    order = request.GET.get('order', 'desc')
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)

    # Check if the data is already in cache
    cache_key = f"{query}-{sort}-{order}-{page}-{pagesize}"
    cached_data = cache.get(cache_key)
    if cached_data:
        questions = cached_data['items']
        total_count = cached_data['total']
    else:
        # Make a request to the StackOverflow API
        url = f"{settings.STACK_OVERFLOW_API_BASE_URL}/search/advanced"
        params = {
            'q': query,
            'sort': sort,
            'order': order,
            'page': page,
            'pagesize': pagesize,
            'site': 'stackoverflow'
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Cache the data
        cache.set(cache_key, data, settings.CACHE_TIMEOUT)

        questions = data['items']
        total_count = data['total']

    # Paginate the results
    paginator = Paginator(questions, pagesize)
    page_obj = paginator.get_page(page)

    context = {
        'query': query,
        'sort': sort,
        'order': order,
        'page': page,
        'pagesize': pagesize,
        'page_obj': page_obj,
        'total_count': total_count
    }
    return render(request, 'search_results.html', context)