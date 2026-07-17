# from django.urls import path

# from .views import passenger_list
# from .views import latest_passenger

# urlpatterns = [

#     path("passengers/", passenger_list),

#     path("latest/", latest_passenger),

# ]
########new..................... New///////////////////

# from django.urls import path

# from .views import dashboard_data

# urlpatterns = [

#     path("dashboard/", dashboard_data),

# ]

########new..................... New///////////////////

from django.urls import path

from .views import dashboard_data

urlpatterns = [

    path("dashboard/", dashboard_data),

]