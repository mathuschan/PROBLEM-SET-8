from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .models import Artist, Museum, Painting
from django.utils.html import escape

# index
def list_museums(request):
    museums = Museum.objects.all()
    return render(request, 'app/index.html', { 'museums': museums })

# museum/<museum_id>
def list_museum_paintings(request, museum_id):
    museum = get_object_or_404(Museum, pk=museum_id)
    paintings = Painting.objects.filter(museum=museum)
    context = {
        'paintings': paintings,
        'museum': museum.name if museum else None,  # Modification
    }
    return render(request, 'app/paintings.html', context)

# search for painting or artist
def search(request):
    q = request.GET.get('q')
    paintings = Painting.objects.filter(title__icontains=q)
    return render(request, 'app/paintings.html', { 'q': q, 'paintings': paintings })


# return json data of painting
def painting_info(request, painting_id):
    painting = get_object_or_404(Painting, pk=painting_id)
    return JsonResponse({
        'title': escape(painting.title),
        'description': escape(painting.description),
        'creation_year': painting.creation_year,
        'image': painting.image.url,
        'value': painting.value,
        'is_on_display': painting.is_on_display,
        'artist': f'{painting.artist.first_name} {painting.artist.last_name}',
        'museum': painting.museum.name
    })

