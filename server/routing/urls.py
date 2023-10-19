from django.urls import path, include

from routing import views

app_name = "routing"

urlpatterns = [
    path("api/html/", views.sendHTML, name="routing_html"),
    path("api/data/", views.get_post_data, name="routing_data"),
    path("api/create/", views.create_link_data, name="create_link"),
    path("api/delete/<int:id>", views.delete_link_data, name="delete_link"),
    path("api/data/<str:identifier>", views.get_link, name="get_link"),
    path("api/data/<int:id>", views.get_link_id, name="get_link"),
    # path("<str:short_name>/", views.follow_url, name="follow"),
]
