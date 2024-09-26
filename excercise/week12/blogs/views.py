from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from blogs.forms import BlogForm
from django.core.exceptions import PermissionDenied
from django import views
from blogs.models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def is_my_blog(user, author):
    if user == author:
        return True
    return False


class BlogListView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/authen/"
    permission_required = ['blogs.view_blog']
    
    def get(self, request: HttpRequest):
        blog_qs = Blog.objects.all()
        context = {
            "blogs": blog_qs,
            "can_add_blog": request.user.has_perm('blogs.add_blog'),
            "can_change_blog": request.user.has_perm('blogs.change_blog'),
            "can_delete_blog": request.user.has_perm('blogs.delete_blog'),
            "can_add_category": request.user.has_perm('category.add_category'),
        }
        return render(request, 'blog_list.html', context)


class BlogDetailView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/authen/"
    permission_required = ['blogs.view_blog']
    def get(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        form = BlogForm(instance=blog)
        check_delete = False
        if request.user.is_staff or is_my_blog(request.user, blog.author):
            check_delete = True
        context = {
            "blog": blog,
            "form": form,
            "can_change_blog": request.user.has_perm('blogs.change_blog'),
            "can_delete_blog": request.user.has_perm('blogs.delete_blog'),
            "owner_check": is_my_blog(request.user, blog.author),
            "check_delete": check_delete
        }
        return render(request, "blog_detail.html", context)
    

class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/authen/"
    permission_required = ['blogs.add_blog']
    def get(self, request: HttpRequest):
        form = BlogForm()
        context = {
            "form": form
        }
        return render(request, 'blog_create.html', context)
    
    def post(self, request: HttpRequest):
        form = BlogForm(request.POST)
        
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()
            return redirect('blog-list')
        else:
            return render(request, "blog_create.html", {"form": form})
            

class BlogEditView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/authen/"
    permission_required = ['blogs.change_blog']
    def post(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        print(request.user, blog.author)
        if not is_my_blog(request.user, blog.author):
            raise PermissionDenied("Only for the blog owner.")
        
        form = BlogForm(request.POST, instance=blog)
        
        if form.is_valid():
            form.save()
            return redirect('blog-detail', pk=blog.id)
        else:
            context = {
                "blog": blog,
                "form": form  
            }
            return render(request, "blog_detail.html", context)
        
        
class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    login_url = "/authen/"
    permission_required = ['blogs.delete_blog']
    def get(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        
        if not is_my_blog(request.user, blog.author):
            if not request.user.is_staff:
                raise PermissionDenied("Only for the blog owner.")
        blog.delete()
        return redirect('blog-list')
        
