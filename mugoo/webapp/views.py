from django.shortcuts import render
from django.http import JsonResponse
from .models import Area


# Create your views here.
def create_areas(request):
    areas = open(r"webapp\Area.csv", mode="r")
    context1 = str(areas.read()).split("\n")
    location = {}
    for i in context1:
        if i != "":
            x = i.split(",")
            v = Area(x[1], x[0])
            v.save()
    return JsonResponse(location)


def index(request):
    return render(request, template_name="index.html")


import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
from .models import Book,BookInstance
from django.views import generic

class BookList(generic.ListView):
    model = BookInstance
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        context['search_term'] = self.request.GET['q']
        return context

    def get_queryset(self):
        query=self.request.GET['q']
        return BookInstance.objects.filter(book__title__icontains=query)

# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#
#         entry_query = get_query(query_string, ['title', 'isbn',])
#
#         found_entries = Book.objects.filter(entry_query).order_by('title')
#
#     return render(request,template_name='search.html', context={"books":found_entries} ,)
