from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Coursera microservice / proxy endpoints at root
    path('fetchDealers', app_views.fetch_dealers_direct, name='fetch_dealers_root'),
    path('fetchDealers/<str:state>', app_views.fetch_dealers_direct, name='fetch_dealers_by_state_root'),
    path('fetchDealer/<int:dealer_id>', app_views.fetch_dealer_by_id_direct, name='fetch_dealer_by_id_root'),
    path('fetchReviews/dealer/<int:dealer_id>', app_views.fetch_reviews_by_dealer_direct, name='fetch_reviews_by_dealer_root'),
    path('analyze/<path:text>', app_views.analyze_review_direct, name='analyze_review_root'),
    path('analyze', app_views.analyze_review_direct, name='analyze_review_query_root'),

    # Frontend routes
    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
