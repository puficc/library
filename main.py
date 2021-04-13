from flask import Flask, request, url_for, render_template
import requests
import sqlite3
import sys

email, name, surname, age, sex, choice = '', '', '', 0, '', ''
for_stat = []
text = []
files = {'для начальных классов': 'kids.txt', 'для подготовки к огэ': 'oge.txt',
         'для подготовки к егэ': 'ege.txt', 'что-то для души': 'must_read.txt'}

app = Flask(__name__)


class Work_with_database:
    def __init__(self, email, name, surname, age, sex, categ):
        self.email = email
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
        self.chc = categ
        self.add_db()

    def add_db(self):
        print(self.chc)
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        if self.sex == 'female':
            self.sex = 0
        else:
            self.sex = 1
        self.age = int(self.age[:2])
        self.cho, = cur.execute("""SELECT id FROM u_choice
                                    WHERE category = ?""", (self.chc,))
        cur.execute("""INSERT INTO web_users VALUES(?,?,?,?,?,?)""",
                    (self.email, self.name, self.surname, self.age, bool(self.sex), self.cho[0]))

        con.commit()
        con.close()

    def stat(self):
        try:
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            kol_first = cur.execute("""SELECT category FROM web_users
                                        WHERE category = 1""")
            kol_second = cur.execute("""SELECT category FROM web_users
                                        WHERE category = 2""")
            kol_third = cur.execute("""SELECT category FROM web_users
                                        WHERE category = 3""")
            kol_fourth = cur.execute("""SELECT category FROM web_users
                                        WHERE category = 4""")

            self.data = [len(kol_first), len(kol_second), len(kol_third), len(kol_fourth)]

            return True
        except Exception as ex:
            print(ex)


@app.route('/hello', methods=['POST', 'GET'])
def hello():
    if request.method == 'GET':
        return f'''<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                         <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>  
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/hat_style.css')}"/>
                                <title>Библиотека рекомендаций</title>
                              </head>
                         <body>                            
                          <div class = "top-menu">
                            <ul class="menu-main">
                                <li class="one-item"><a href="/hello">  Главная  </a></li>
                                <li class="two-item"><a href="/help">  Помощь  </a></li>
                                <li class="three-item"><a href="/test">  Тестик  </a></li>
                                <li class="four-item"><a href="/where"> Где с нами связываться </a></li>	
                                <li class="five-item"><a href="/stat"> Статистика </a></li>
                            </ul>
                          </div>
                                <h1>Форма для доступа к подборке</h1>
                                <div>
                                    <form class="login_form" method="post">
                                        <input type="text" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                                        <input type="text" class="form-control" id="name" placeholder="Введите имя" name="name">
                                        <br>
                                        <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">                                        
                                        <br>
                                        <label for="classSelect">Какая подборка книг вас интересует?</label>
                                        <select class="form-control" id="book_type" name="w_books">
                                          <option>для начальных классов</option>
                                          <option>для подготовки к огэ</option>
                                          <option>для подготовки к егэ</option>
                                          <option>что-то для души</option>
                                        </select>

                                    <div class="form-group">
                                        <label for="form-check">Выберите возрстную категорию</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="age" id="child" value="6">
                                            6+           
                                    </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="radio" name="age" id="mid" value="12">          
                                            12+
                                    </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="radio" name="age" id="teen" value="16">
                                            16+   
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <br>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Запомнить меня</label>
                                    </div>
                                    <br>
                                    <button type="submit" class="btn btn-primary"</button>Отправить</button>
                                </form>
                            </div>
                            </body>
                            </html>'''
    elif request.method == 'POST':
        global email, name, surname, age, sex, choice
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']  # по name=' '
        choice = request.form['w_books']
        age = request.form['age']
        sex = request.form['sex']
        flag = False
        try:
            Work_with_database(email, name, surname, age, sex, choice)
        except sqlite3.IntegrityError as er:
            if er:
                flag = True
            else:
                flag = False
        title = 'Наши предложения'
        with open(f'{files[choice]}', encoding='UTF-8', mode='r') as f:
            for i in f.readlines():
                text.append(i)
        return render_template('second_page.html', title=title, surname=surname, name=name,
                               choice=choice, mark=flag, text=text)


@app.route('/where')
def where():
    map_request = "http://static-maps.yandex.ru/1.x/?ll=39.204123,51.657847&spn=0.002,0.002&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open('static/img/map.jpg', 'wb') as file:
        file.write(response.content)

    title = "Прятаться смысла нет"
    return render_template('where.html', title=title)


@app.route('/help')
def help():
    title = 'Помощь/руководство'
    with open('help.txt', encoding='UTF-8', mode='r') as f:
        for i in f.readlines():
            text.append(i)
    return render_template('help.html', title=title, text=text)


@app.route('/test', methods=['POST', 'GET'])
def test():
    kol = 0
    title = 'Тест для книжных червей'
    intro = 'Тест на знание произведений и литературных авторов'
    lim = 'Рекомендутся прохождение при возрастной категории 12+'
    if request.method == 'GET':
        return render_template('test.html', title=title, intro=intro, lim=lim,
                               first_q='Как звали главного героя произведения Ф.М.Достоевсого "Преступление и наказание?"',
                               second_q='Кто из перечисленных авторов НЕ погиб на(из-за) дуэле(-я)?',
                               third_q='Из-за чего Герасиму пришлось утопить Му-му?',
                               fourth_q='Продолжите название книги Булгакова "Мастер и ..."',
                               fiveth_q='Чей это портрет?',
                               sixth_q='В каком из нижеперечисленных городов родился С.Я.Маршак?',
                               seventh_q='Отметьте произведение, которое было написано по историческим событиям',
                               eigth_q='Какое стихотворение Лермонтова начинается со слов "Скажи-ка, дядя, ведь не даром Москва, спаленная пожаром"',
                               nineth_q='Вышла ли замуж за Балконского Наташа Ростова?',
                               tenth_q='Невероятно сложный вопрос: Как звали ассистента хирурга из "Собачьего сердца"?')
    elif request.method == 'POST':
        print('no')
        if request.method['answ_f'] == 'Раскольников':
            kol += 1
        if request.method['answ_s'] == 'Платонов':
            kol += 1
        if request.method['answ_t'] == 'заставила хозяйка':
            kol += 1
        if request.method['answ_fo'] == 'Маргарита':
            kol += 1
        if request.method['answ_fi'] == 'Толстой':
            kol += 1
        if request.method['answ_si'] == 'Воронеж':
            kol += 1
        if request.method['answ_se'] == 'А.С.Пушкин "Капитанская дочка"':
            kol += 1
        if request.method['answ_e'] == 'Бородино':
            kol += 1
        if request.method['answ_n'] == 'Нет':
            kol += 1
        if request.method['answ_te'] == 'Иван Арнольдович Борменталь':
            kol += 1
        if kol > 5:
            return "Поздравляем, Вы отлично справились"
        else:
            return "Полагаем, Вам стоит лучше изучить эти темы"


@app.route('/stat')
def stat():
    result = Work_with_database.stat
    title = 'Немного статистики сайта'
    h1_p = 'На этой странице представлена статистика нашего сайта'
    print(result)
    first_param = f'Чаще всего ищут литературу {popular}'
    second_param = f'Наименее популярный раздел {no_popular}'
    return render_template('stat.html', title=title, h1_p=h1_p)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
