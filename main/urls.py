from django.urls import path
from .views import index, other_page, BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, by_rubric, detail, profile_bb_detail, profile_bb_add, profile_bb_delete, profile_bb_change, filter, profile_seller, comment_bb_change,comment_bb_delete, voice_search

app_name = 'main'
urlpatterns = [



    path('search/', filter, name='search'),
    path('', index, name='index'),

    path('voice_search/', voice_search, name='voice_search'),

    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),

    path('change/comment/<int:pk>/', comment_bb_change, name='comment_bb_change'),
    path('delete/comment/<int:pk>/', comment_bb_delete, name='comment_bb_delete'),

    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('profile/seller/<int:pk>/', profile_seller, name='profile_seller')
]
