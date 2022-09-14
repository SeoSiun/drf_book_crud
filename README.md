# Book CRUD with Django REST Framework
Django REST Framework(DRF), Swagger를 이용해 상품(Book)에 대한 CRUD(Create, Read, Update, Delete) API를 구현하는 프로젝트.

### Tech

- Python
- Django
- Django REST Framework
- Swagger (drf-yasg)

### API

- API에 대한 자세한 설명을 보려면 runserver 후 http://localhost:8000/swagger/ 에 접속하세요.

| HTTP Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | books/ | 책 목록 조회 / title, author로 검색하거나, title, author, price를 기준으로 정렬된 책 목록을 한 페이지(3개)씩 가져옴. |
| POST | books/ | parameter로 받은 title, author, introduction, price 정보를 갖는 책 생성. |
| GET | books/{id} | id에 해당하는 책의 정보를 가져옴. |
| PUT | books/{id} | id에 해당하는 책의 title, author, introduction, price를 request로 받은 값으로 수정 |
| PATCH | books/{id} | id에 해당하는 책의 title, author, introduction, price 중 request body에서 받은 값을 수정 |
| DELETE | books/{id} | id에 해당하는 책을 삭제 |
 | POST | users/ | email, password, name, address 정보를 갖는 유저 생성 (email 중복 불가) / 해당 유저의 token을 반환함.|
 | POST | users/login/ | email, password와 일치하는 유저의 token을 반환 |

### How To Run

1. clone the project
    
    ```bash
    git clone https://github.com/SeoSiun/drf_book_crud.git
    cd drf_book_crud
    ```
    
2. installation
    
    ```bash
    python3 -m venv env
    source env/bin/activate
    
    pip install django
    pip install djangorestframework
    pip install drf-yasg
    ```
    
3. Run server
    
    ```bash
    cd book_crud
    python manage.py migrate
    python manage.py runserver
    ```