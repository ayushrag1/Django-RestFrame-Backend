from django.urls import path

from base import views

url_pattern = [
    path("", views.HealthCheck.as_view()),
    path('contract/summarization/', views.ContractSummarization.as_view()),
    path('contract/authoring/', views.ContractAuthoring.as_view()),
    path('contract/comparison/', views.ContractStandardComparison.as_view()),
    path('contract/spend-analytics/', views.ContractSpendAnalytics.as_view()),
    path('contract/conversational/', views.ContractConversational.as_view())
]
