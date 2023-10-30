from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.viewsets import ViewSet
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse

from .serializers import UserSerializer, UserLoginSerializer
from .models import Document
from .serializers import DocumentSerializer
from .Llama_Pinecone import uploading_to_pinecone, chat, get_DocumentList
from .forms import UploadFileForm
from .models import Document, Pinecone_indice
import json, time
from django.http import JsonResponse


from django.shortcuts import render
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage


class UserLoginView(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    serializer_class = UserLoginSerializer


class UserCreateAPIView(CreateAPIView):
    """
    post:
        Create new user instance. Returns username, email of the created user.

        parameters: [username, email, password]
    """

    def get(self, request, *args, **kwargs):
        return render(request, "register.html")

    # permission_classes = [AllowAny]
    # def post(self, request, *args, **kwargs):
    serializer_class = UserSerializer


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("upload part")
                uploaded_file = request.FILES["file"]
                # Save the file to the database
                filter_name = "pdf_files/" + str(uploaded_file)
                print("file name", filter_name, uploaded_file)

                if Document.objects.filter(file=filter_name).exists():
                    status = "warning"
                    msg = "PDF already exist."
                    response = {"status": status, "msg": msg}
                    return JsonResponse(response)
                else:
                    fs = FileSystemStorage(location="pdf_files/")
                    name = fs.save(uploaded_file.name, uploaded_file)

                    uploaded_file_obj = Document(file=uploaded_file)
                    flag = uploaded_file_obj.save()
                    print("flag", flag, name)
                    start_time = time.time()
                    uploading_to_pinecone(filter_name, uploaded_file)
                    print(
                        "Inserting into llama index: {:.2f}s".format(
                            time.time() - start_time
                        )
                    )
                    status = "success"
                    msg = "Document is uploaded successfully."
                    response = {"status": status, "msg": msg}
                    return JsonResponse(response)
            except Exception as e:
                print(e)
                status = "error"
                msg = "Error occured."
                response = {"status": status, "msg": msg}
                return JsonResponse(response)
                # cleanup temp file

        else:
            status = "invalid"
            msg = "This file is invalid."
            response = {"status": status, "msg": msg}
            return JsonResponse(response)
    else:
        return render(request, "upload.html")


def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "upload.html", context)


def get_documents(request):
    print("sdfdsf")
    if request.method == "GET":
        file_names = Pinecone_indice.objects.values_list("pinecone_title", flat=True)
        namespace_list = list(file_names)
        response = {"list": namespace_list}
        print("list", response)
        return JsonResponse(response)


def ChatWithDocs(request):
    if request.method == "POST":
        print("entered")
        data = json.loads(request.body)
        query_text = data.get("query")
        query_pdf_name = data.get("pdf_name")
        print(query_text, query_pdf_name)
        if query_text is None:
            return JsonResponse({"error": "No text found"}, status=400)

        print("query", query_text)
        # response = chat(query_text, query_pdf_name)
        print("response")
        return JsonResponse({"text": str("response")})
    else:
        return render(request, "chat.html")
