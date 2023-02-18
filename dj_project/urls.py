from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from dj_project import settings
from first.views import voting_page, list_of_votings_page, index_page, add_voting, registration, redact_voting, profile, \
    redact_profile, complaint, view_complaint, admin_panel, change_complaint_status, delete_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('voting/<int:voting_id>/', voting_page, name='voting_details'),
    path('list/', list_of_votings_page),
    path('login/', auth_views.LoginView.as_view(
        extra_context={
            "pagetitle": "Auth",
            "pageheader": "Авторизация"
        }
    )),
    path('registration/', registration),
    path('logout/', auth_views.LogoutView.as_view()),
    path('add_voting/', add_voting),
    path('redact/<int:voting_id>/', redact_voting),
    path('profile/<int:profile_id>/', profile),
    path('redact_profile/<int:redact_profile_id>/', redact_profile),
    path('complaint/', complaint),
    path('view_complaint/', view_complaint),
    path('admin_panel/', admin_panel),
    path('change_complaint_status/<int:complaint_id>/', change_complaint_status),
    path('delete_user/', delete_user)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

