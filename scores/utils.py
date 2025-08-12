from django.core.paginator import Paginator

def paginate_if_needed(queryset, request, per_page=25, threshold=25):
    """
    Add pagination if queryset has more than threshold items.
    Returns (paginated_items, page_obj) tuple.
    """
    if queryset.count() > threshold:
        paginator = Paginator(queryset, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj
    else:
        return queryset, None
