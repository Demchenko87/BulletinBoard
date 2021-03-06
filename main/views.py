import json

from django.contrib import messages
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from . import forms
from .models import AdvUser, SubRubric, Bb, Comment, Stars
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm, BbForm, CommentForm, AIFormSet, UserCommentForm, GuestCommentForm
from django.views.generic.base import TemplateView
from .utilities import signer, send_new_comment_notification
from django.db.models import Avg
import wave
import ffmpeg
import soundfile as sf


#-*- coding:UTF-8 -*-
import speech_recognition as sr
import os
import sys
import webbrowser

class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль у пользователя изменен'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

@login_required
def profile(request):
    bbs_count = Bb.objects.filter(author=request.user.pk)
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'bbs': bbs, 'bbs_count': bbs_count}
    return render(request, 'main/profile.html', context)


def index(request):
    bbs = Bb.objects.filter(is_active=True)[:100]
    bbs_count = Bb.objects.filter(author=request.user.pk)
    context = {'bbs': bbs, 'bbs_count': bbs_count}
    return render(request, 'main/index.html', context)

def voice_search(request):
    print(request)
    token = request.POST.get('token')
    print(token)
    search = blob_search_decoder(request.FILES['audio'], token)

    text = str(search)

    # filter = Bb.objects.filter(Q(title__icontains=text) | Q(content__icontains=text))
    print(text)
    context = {'search_list': text}
    return render(request, 'main/voice_search.html', context)


# def voice_search(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print(request)
#             url = 'http://127.0.0.1:8000/accounts/register/'
#             return HttpResponseRedirect(url)
#         else:
#             return HttpResponse("GET")





def blob_search_decoder(f, token):
    filename = 'media/voice_search/' + token + '.ogg'
    audio = 'media/voice_search/' + token + '.wav'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    decoder(filename, audio)
    text = audio_voice(audio)
    os.remove(filename)
    os.remove(audio)

    return text



def decoder(filename, audio):
    cmd = "ffmpeg -i "+ str(filename)+" -acodec pcm_s16le -ac 1 -ar 16000 "+ str(audio)
    os.system(cmd)

def audio_voice(filename):
    r = sr.Recognizer()
    with sr.AudioFile(str(filename)) as source:
        audio = r.listen(source)
        text = r.recognize_google(audio, language="ru_RU")

        # url = str('http://127.0.0.1:8000/search/?q=' + text).replace(' ', '+')
        # os.system("open \"\"" + url)
        return text


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BBLoginView(LoginView):
    template_name = 'main/login.html'

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)

def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    # bbs_all = Bb.objects.filter(is_active=True)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    bbs_count = Bb.objects.filter(author=request.user.pk)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list,
               'form': form, 'bbs_count': bbs_count}
    return render(request, 'main/by_rubric.html', context)


def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active=True)
    initial = {'bb': bb.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.SUCCESS, 'Комментарий не добавлен')
    bbs_count = Bb.objects.filter(author=request.user.pk)

    star_form = Comment.objects.filter(user=bb.author.username).aggregate(Avg('star'))['star__avg']
    stars = Stars.objects.all().order_by('-id')





    context = {
        'bb': bb, 'ais': ais, 'comments': comments, 'form': form, 'bbs_count': bbs_count, 'star_form': star_form, 'stars': stars
    }
    return render(request, 'main/detail.html', context)


@login_required
def profile_bb_detail(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active=True)
    bbs_count = Bb.objects.filter(author=request.user.pk)
    context = {'bb': bb, 'ais': ais, 'comments': comments, 'bbs_count': bbs_count}
    return render(request, 'main/profile_bb_detail.html', context)

@login_required
def profile_bb_add(request):
    if request.method=='POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('main:profile')
    else:
        form = BbForm(initial={'author': request.user.pk})
        formset = AIFormSet
    bbs_count = Bb.objects.filter(author=request.user.pk)
    context = {'form': form, 'formset': formset, 'bbs_count': bbs_count}
    return render(request, 'main/profile_bb_add.html', context)

@login_required
def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    print(bb)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Объявление исправлено')
                return redirect('main:profile')
    else:
        form = BbForm(instance=bb)
        formset = AIFormSet(instance=bb)
    bbs_count = Bb.objects.filter(author=request.user.pk)
    context = {'form': form, 'formset': formset, 'bbs_count': bbs_count}
    return render(request, 'main/profile_bb_change.html', context)

@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('main:profile')
    else:
        bbs_count = Bb.objects.filter(author=request.user.pk)
        context = {'bb': bb, 'bbs_count':bbs_count}
        return render(request, 'main/profile_bb_delete.html', context)

def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author
    if kwargs['created'] & author.send_messages:
        send_new_comment_notification(kwargs['instance'])
post_save.connect(post_save_dispatcher, sender=Comment)


def filter(request):
    search = request.GET['q']
    bb = Bb.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    bbs_count = Bb.objects.filter(author=request.user.pk)

    return render(request, 'main/search.html', context={
                    'bbs': bb,
                    'bbs_count': bbs_count
                    })


def profile_seller(request,pk):
    bbs_count = Bb.objects.filter(author=request.user.pk)
    bb_profile_seller = Bb.objects.filter(author=pk)
    return render(request, 'main/profile_seller.html', context={
        'bb_profile_seller': bb_profile_seller,
        'bbs_count': bbs_count
    })


@login_required
def comment_bb_change(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий исправлен')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = CommentForm(instance=comment)
    comment_change = Comment.objects.filter(author=request.user.username)
    context = {'form': form, 'comment_change': comment_change}
    return render(request, 'main/comment_bb_change.html', context)

@login_required
def comment_bb_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Комментарий удален')
        return redirect('main:index')
    else:
        context = {'comment': comment}
        return render(request, 'main/comment_bb_delete.html', context)


