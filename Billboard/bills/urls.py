from django.urls import path
from .views import *

urlpatterns = [
   path('', BillList.as_view(), name='bills'),
   path('bill/<int:pk>', BillDetail.as_view(), name='bill_detail'),
   path('categories/<int:pk>', CategoryList.as_view(), name='bill_cat_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('create/', BillCreate.as_view(), name='bill_create'),
   path('bills/<int:pk>/update/', BillUpdate.as_view(), name='bill_edit'),
   path('bills/<int:pk>/delete/', BillDelete.as_view(), name='bill_delete'),
   path('bills/<int:pk>/comments/', CommentCreate.as_view(), name='comment_edit'),
   path('comments/', CommentList.as_view(), name='comments'),
   path('comments/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
   path('comments/<int:pk>/accept/', accept_comment, name='accept_comment'),
   path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
]
