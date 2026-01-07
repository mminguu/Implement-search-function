from django.urls import path
from .views import ask_question, main_page, serve_css

urlpatterns = [
    path("", main_page, name="main"),  # 메인 페이지
    path("ask/", ask_question, name="ask"),
    path("main.css", serve_css, name="css"),  # CSS 파일
]
