from django.urls import path
from LlamaApp import views 

app_name = "LlamaApp"

urlpatterns = [
    path("", views.UserLoginView.as_view(), name="chat_docs"),
    path("register", views.UserCreateAPIView.as_view(), name="user_create"),
    path("chat", views.ChatWithDocs, name="chat_docs"),
    path("upload", views.upload_file, name="upload"),
    path("getDocuments", views.get_documents, name="getDocumentsList")
]
