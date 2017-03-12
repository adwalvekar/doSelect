from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.Index.as_view()),
	url(r'^gen_token', views.Gen_Token.as_view()),
	url(r'^view_image', views.ImageView.as_view()),
]
