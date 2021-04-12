# book_rental

## Description

Book store mangement
### Functions 
* add book
* rent book
* return book 
* charge for book rent



### Documentation
https://documenter.getpostman.com/view/10026788/TzCV45QS

### Application Link
https://booksrental.herokuapp.com/


<br>

### API 

| Routes                                   | Methods Allowed |   Actions               |
| ------------------------------------------ | -------| ------------------------|
| `/api/users/register`                         |`POST`  | REGISTER CUSTOMER |
| `/api/users/login`                         |`POST`  | LOGIN & SET COOKIE |
| `/api/books/`             |`POST, GET`  | ADD & GET BOOKS           |
| `/api/books/rent/`             |`POST`   | RENT BOOK        |
| `/api/books/rents/`             |`GET`   | GET ALL RENTS        |
| `/api/books/return/<int:book_id>/<int:customer_id>`       |`GET`  | RETURN BOOK     |
| `/api/books/rent_charge/<int:customer_id>`                    |`GET`   |  CHARGE CUSTOMER  | 
| `/api/books/<int:book_id>`                    |`GET, PUT, PATCH, DELETE,`   |  BOOK GET, UPDATE, DELETE  | 

### SET UP DATABASE
```
psql postgres 
CREATE DATABASE <YOUR-DATABASE-NAME>
```

### SET ENV VARIABLES
.env
```
export DATABASE='YOUR-DATABASE-NAME>'
export PASSWORD='<YOUR-DATABASE-PASSWORD>'
export USER='<YOUR-DATABASE-USER>'
```

### SET UP APP

This assumes you have python and postgres installed 

```bash
cd books_rental
virtuanlenv venv
source venv/bin/activate
source .env
pip install -r requirements.txt
python3 manage.py runserver
python3 manage.py migrate
```


# Tests
 $ python3 manage.py test --with-coverage

 ## coverage report
 [coverage_.txt](coverage_.txt)
 



