from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Bill, Comment, Category
from .forms import CommentForm, BillForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User
from .tasks import respond_send_email, respond_accept_send_email
from protect.views import BillFilter


class BillList(ListView):
    model = Bill
    template_name = 'bill_list.html'
    context_object_name = 'bills'
    ordering = '-bill_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BillDetail(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'bill_detail.html'
    context_object_name = 'bill_detail'

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #comments = Comment.objects.filter(comment=True, comment_bill_id=self.kwargs['pk']).order_by('date_in')
        #context['comment_bill'] = comments
        #return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Comment.objects.filter(author_id=self.request.user.id).filter(comment_bill_id=self.kwargs.get('pk')):
            context['respond'] = "Откликнулся"
        elif self.request.user == Bill.objects.get(pk=self.kwargs.get('pk')).author:
            context['respond'] = "Мое_объявление"
        return context

class BillCreate(LoginRequiredMixin, CreateView):
    form_class = BillForm
    model = Bill
    template_name = 'bill_edit.html'
    context_object_name = 'bill'
    success_url = reverse_lazy('bill_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    #def form_valid(self, form):
        #bill = form.save(commit=False)
        #bill.author = User.objects.get(id=self.request.user.id)
        #bill.save()
        #return redirect(f'/bills/{bill.id}')

    #def dispatch(self, request, *args, **kwargs):
        #if not self.request.user.has_perm('bills.add_bill'):
            #return HttpResponseRedirect(reverse('account_profile'))
        #return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/bill/{post.id}')
    #def add_bill(request):
        #if request.method == 'POST':
            #form = BillForm(request.POST)
            #if form.is_valid():
                #bill_item = form.save(commit=False)
                #bill_item.save()
                #return redirect('/')
            #else:
                #form = BillForm()
            #return render(request, 'bill_edit.html', {'form': form})


class BillUpdate(LoginRequiredMixin, UpdateView):
    form_class = BillForm
    model = Bill
    template_name = 'bill_edit.html'
    success_url = '/create/'

    #def get_object(self, **kwargs):
        #my_id = self.kwargs.get('pk')
        #return Bill.objects.get(pk=my_id)

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #return context

    def dispatch(self, request, *args, **kwargs):
        author = Bill.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только его автор")

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Bill.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/bill/' + str(self.kwargs.get('pk')))


class BillDelete(LoginRequiredMixin, DeleteView):
    model = Bill
    template_name = 'bill_delete.html'
    success_url = reverse_lazy('bill_list')

    def dispatch(self, request, *args, **kwargs):
        author = Bill.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только его автор")


class CommentList(ListView):
    model = Comment
    template_name = 'comments.html'
    ordering = '-date_in'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BillFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('comments')

    def form_valid(self, form):
        comment = form.save(commit=False)
        bill = Bill.objects.get(pk=self.kwargs['pk'])
        comment.author = self.request.user
        comment.bill = bill
        comment.save()
        return super().form.valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_list'] = Bill.objects.get(pk=self.kwargs['pk']).title
        return context

        #self.object = form.save(commit=False)
        #self.object.comment = Comment.objects.get(pk=self.kwargs['pk'])
        #current_user = self.request.user
        #self.object.user = current_user
        #return super().form_valid(form)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('comments')

    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Comment.objects.get(pk=my_id)


class CategoryList(BillList):
    model = Bill
    template_name = 'category_list.html'
    context_object_name = 'category_bills_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Bill.objects.filter(category=self.category).order_by('-bill_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class Respond(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'respond.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = User.objects.get(id=self.request.user.id)
        respond.bill = Bill.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        respond_send_email.delay(respond_id=respond.id)
        return redirect(f'/bill/{self.kwargs.get("pk")}')


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'invalid_code.html')
        return redirect('account_login')


@login_required
def accept_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.accepted = True
    comment.save()
    comment.send_accepted_email()
    return HttpResponseRedirect(reverse('comments'))


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('bill_cat_list', pk)