from healthCareManagement import views
from django.urls import path

urlpatterns = [
    path('test',views.test),
    path('login', views.login),
    path('doctorRegister', views.doctorRegister),
    path('nutritionistRegister', views.nutritionistRegister),
    path('nutritionistProfile', views.nutritionistProfile),
    path('patReportUpload', views.patReportUpload),
    path("patientReportHistory", views.patientReportHistory),
    path('doctorSpecialist', views.doctorSpecialist),
    path('doctorProfile/<id>', views.doctorProfile),
    path("patientSearchNutritionist", views.patientSearchNutritionist),
    path('patientRegister', views.patientRegister),
    path('patientProfile/<id>', views.patientProfile),
    path('patientPhysicalActivity', views.physicalActivity),
    path('patientSearchDoctor/<id>', views.patientSearchDoctor),
    path('patDocChat', views.patDocChat),
    path('patDocGetChat', views.patDocGetChat),
    path('patChats/<id>', views.patChats),
    path('docChats/<id>', views.docChats),
    path("prescribeMedicine", views.prescribeMedicine),  
    path("doctorPrescribedMedicines", views.doctorPrescribedMedicines),
    path("patientPrescribedMedicines", views.patientPrescribedMedicines),
]