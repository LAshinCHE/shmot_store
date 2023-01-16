Магазин одежды Shmot_store
============
![Заглавная страница сайта](https://github.com/LAshinCHE/shmot_store/blob/main/index.png)

Цель проекта
-------------
Создание макета интернет-магазина с возможностью редактирвоать/добавлять товары через панель админа и наличием системы аутентификации с сохранением корзины пользователя.

Выполнили:
-------------
| Студент                     | Группа             |
| --------------------------- |:------------------:| 
| Черевичин Егор Викторович   | М8О-206Б-21        | 
| Медведев Кирилл Викторович  |  М8О-206Б-21       | 
| Шуленков Илья Петрович      |  М8О-206Б-21       |   

Этапы реализации проекта:
-------------------------

- Изучение фреймворка Django
- Написание шаблона (template) представляющего логику представления в виде разметки HTML
- Написание кода для работы с данными, используемыми в приложении. Описание классов, соответсвующих таблицам в базе данных, для системы аутентификации.
- Реализация элементов View и URL dispatcher.

Описание
-----------

### Используемый паттерн MVC ###

Фреймворк Django реализует архитектурный паттерн Model-View-Template или сокращенно MVT, который по факту является модификацией распростаненного в веб-программировании паттерна MVC (Model-View-Controller). 

![MVC](https://github.com/LAshinCHE/shmot_store/blob/main/django_mvc.png)

#### Основные элементы паттерна ####
- URL dispatcher: при получение запроса на основании запрошенного адреса URL определяет, какой ресурс должен обрабатывать данный запрос.
- View: получает запрос, обрабатывает его и отправляет в ответ пользователю некоторый ответ. Если для обработки запроса необходимо обращение к модели и базе данных, то View взаимодействует с ними. Для создания ответа может применять Template или шаблоны. В архитектуре MVC этому компоненту соответствуют контроллеры (но не представления).
- Model: описывает данные, используемые в приложении. Отдельные классы, как правило, соответствуют таблицам в базе данных.
- Template: представляет логику представления в виде сгенерированной разметки html. В MVC этому компоненту соответствует View, то есть представления.

Когда к приложению приходит запрос, то URL dispatcher определяет, с каким ресурсом сопоставляется данный запрос и передает этот запрос выбранному ресурсу. Ресурс фактически представляет функцию или View, который получает запрос и определенным образом обрабатывает его. В процессе обработки View может обращаться к моделям и базе данных, получать из нее данные, или, наоборот, сохранять в нее данные. Результат обработки запроса отправляется обратно, и этот результат пользователь видит в своем браузере. Как правило, результат обработки запроса представляет сгенерированный html-код, для генерации которого применяются шаблоны (Template).

### MVC в нашем проекте ### 

При работе над нашим проектом были написаны два приложения: `authentication` (для системы аутентификации) и `store` для работы с разделами магазина.

Когда на сервер приходит запрос, он переадресуется Django, который пытается сообразить, что же конкретно от него просят. Для начала он берет адрес веб-страницы и пробует понять — что же нужно сделать. Эту часть процесса в Django выполняет urlresolver. Он берет список шаблонов и пытается сопоставить их с URL. Django сверяет шаблоны сверху вниз и, если что-то совпадает, он перенаправляет запрос соответствующей функции (которая называется view).

`shmot_store/main/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

from main import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('auth/', include('authentication.urls')),
]

```

`shmot_store/authentication/urls.py`
```python
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.RegisterView.as_view(), name='reg'),
    path('logout/', views.logout_user, name='logout'),
]
```

Реализация `Model`

```python
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='product_name')
    code = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    price = models.DecimalField(max_digits=28, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255,blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.name} - {self.price}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.user} - {self.amount}'

    @staticmethod
    def get_balance(user: User):
        balance = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
        return balance or Decimal(0)


class Order(models.Model):
    STATUS_CART = '1_in_cart'
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_CART, 'in_cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']
       # KIRILL WAS HERE
    def __str__(self):
        return f'{self.user}  - {self.creation_time} - {self.status}'

```
Демонстрация работы
====================

https://drive.google.com/file/d/1fZEviY7L-kXVvfrHiljvrKbLY94K-dyd/view?usp=sharing
