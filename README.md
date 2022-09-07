# Book CRUD with Django REST Framework
Django REST Framework(DRF), Swagger를 이용해 상품(Book)에 대한 CRUD(Create, Read, Update, Delete) API를 구현하는 프로젝트.

### Tech

- Python
- Django
- Django REST Framework
- Swagger (drf-yasg)

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