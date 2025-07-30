from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('Register.html', views.Register, name="Register"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),	
	       path('AddAuction', views.AddAuction, name="AddAuction"),
	       path('AddAuctionAction', views.AddAuctionAction, name="AddAuctionAction"),
	       path('ViewParticipate', views.ViewParticipate, name="ViewParticipate"),
	       path('BrowseList', views.BrowseList, name="BrowseList"),
	       path('ParticipateAction', views.ParticipateAction, name="ParticipateAction"), 	
	       path('DonateAction', views.DonateAction, name="DonateAction"), 
	       path('Donate', views.Donate, name="Donate"), 
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	
]
