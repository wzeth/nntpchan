from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Post, Newsgroup

class BoardView(generic.ListView):
    template_name = 'frontend/board.html'
    model = Post

    def get_queryset(self):
        newsgroup = self.kwargs['name']
        page = int(self.kwargs['page'] or "0")
        try:
            group = Newsgroup.objects.get(name=newsgroup)
        except Newsgroup.DoesNotExist:
            raise Http404("no such board")
        else:
            begin = page * group.posts_per_page
            end = begin + group.posts_per_page
            return get_object_or_404(self.model, newsgroup=group)[begin:end]
        
        
class ThreadView(generic.ListView):
    template_name = 'frontend/thread.html'
    model = Post

    def get_queryset(self):
        return get_object_or_404(self.model, posthash=self.kwargs['op'])
    


class FrontPageView(generic.ListView):
    template_name = 'frontend/frontpage.html'
    model = Post

    def get_queryset(self):
        return self.model.objects.order_by('posted')[:10]
    
    
def modlog(request, page):
    if page is None:
        page = 0
    return HttpResponse('mod log page {}'.format(page))
