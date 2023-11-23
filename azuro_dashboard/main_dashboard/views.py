from django.shortcuts import render

from .models import DashboardRows


# Create your views here.
def index(request):
    all_rows = DashboardRows.objects.all().order_by('-points')
    data = {
        'all_rows': all_rows,
        'places': [x+1 for x in range(all_rows.count())]
    }

    return render(request, 'index.html', data)
