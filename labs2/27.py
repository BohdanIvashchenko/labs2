
from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "lab4_secret_key"

# Наперед задані логіни та паролі
USERS = {
    "admin": "1234",
    "student": "student"
}


# ============================================================
# Допоміжні функції
# ============================================================

def check_auth():
    return "username" in session


def page(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                background: #f5f5f5;
            }}

            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}

            input {{
                padding: 8px;
                margin: 5px;
                border: 1px solid #aaa;
                border-radius: 5px;
            }}

            button {{
                padding: 10px 18px;
                margin: 8px 3px;
                border: none;
                border-radius: 5px;
                background: #1976d2;
                color: white;
                cursor: pointer;
            }}

            button:hover {{
                background: #125aa0;
            }}

            a {{
                color: #1976d2;
            }}

            .error {{
                color: red;
                font-weight: bold;
            }}

            .success {{
                color: green;
                font-weight: bold;
            }}

            table {{
                border-collapse: collapse;
                margin: 15px 0;
            }}

            td {{
                border: 1px solid #555;
                padding: 8px;
                text-align: center;
            }}

            .matrix-input {{
                width: 70px;
                text-align: center;
            }}

            .task {{
                border: 1px solid #ddd;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """


def matrix_html(matrix):
    result = "<table>"

    for row in matrix:
        result += "<tr>"

        for value in row:
            # Красивий вивід цілих чисел
            if isinstance(value, float) and value.is_integer():
                value = int(value)

            result += f"<td>{value}</td>"

        result += "</tr>"

    result += "</table>"

    return result


# ============================================================
# 1. Авторизація
# ============================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("tasks"))

        content = """
        <h1>Лабораторна робота №4</h1>
        <h2>Авторизація</h2>

        <p class="error">Неправильний логін або пароль!</p>

        <form method="post">
            <p>
                <label>Логін:</label><br>
                <input type="text" name="username" required>
            </p>

            <p>
                <label>Пароль:</label><br>
                <input type="password" name="password" required>
            </p>

            <button type="submit">Увійти</button>
        </form>

        <p>
            Тестовий логін: <b>admin</b><br>
            Пароль: <b>1234</b>
        </p>
        """

        return page("Авторизація", content)

    content = """
    <h1>Лабораторна робота №4</h1>

    <h2>Авторизація</h2>

    <form method="post">

        <p>
            <label>Логін:</label><br>
            <input type="text" name="username" required>
        </p>

        <p>
            <label>Пароль:</label><br>
            <input type="password" name="password" required>
        </p>

        <button type="submit">Увійти</button>

    </form>

    <p>
        Тестовий користувач:<br>
        Логін: <b>admin</b><br>
        Пароль: <b>1234</b>
    </p>
    """

    return page("Авторизація", content)


# ============================================================
# Вихід
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# 2. Вибір задачі
# ============================================================

@app.route("/tasks")
def tasks():

    if not check_auth():
        return redirect(url_for("login"))

    username = session["username"]

    content = f"""
    <h1>Лабораторна робота №4</h1>

    <p>
        Користувач: <b>{username}</b>
    </p>

    <h2>Виберіть задачу</h2>

    <div class="task">

        <h3>Задача 27.4</h3>

        <p>
            Задана непорожня послідовність ненульових цілих чисел,
            за якою йде 0. Визначити кількість змін знаку
            в цій послідовності.
        </p>

        <a href="/task274">
            <button>Розв'язати задачу 27.4</button>
        </a>

    </div>

    <div class="task">

        <h3>Задача 27.10</h3>

        <p>
            Ввести дві матриці та обчислити їх добуток.
            Матриці вводяться на окремих сторінках.
            Перед введенням задаються їх розміри.
        </p>

        <a href="/dimensions">
            <button>Розв'язати задачу 27.10</button>
        </a>

    </div>

    <hr>

    <a href="/logout">Вийти</a>
    """

    return page("Вибір задачі", content)


# ============================================================
# 3. Задача 27.4
# ============================================================

@app.route("/task274")
def task274():

    if not check_auth():
        return redirect(url_for("login"))

    # Початок нової послідовності
    session["sequence"] = []
    session["changes"] = 0

    return render_274()


def render_274(error=""):

    sequence = session.get("sequence", [])
    changes = session.get("changes", 0)

    sequence_text = ", ".join(map(str, sequence))

    error_html = ""

    if error:
        error_html = f"""
        <p class="error">{error}</p>
        """

    content = f"""
    <h1>Задача 27.4</h1>

    <p>
        Вводьте ненульові цілі числа послідовності.
        Для завершення введіть <b>0</b>.
    </p>

    {error_html}

    <form method="post" action="/task274/process">

        <label>Наступний елемент:</label>

        <input
            type="number"
            name="number"
            autofocus
            required
        >

        <button type="submit">
            Обробити
        </button>

    </form>

    <h3>Поточна послідовність:</h3>

    <p>
        {sequence_text if sequence_text else "Ще немає введених чисел."}
    </p>

    <p>
        Поточна кількість змін знаку:
        <b>{changes}</b>
    </p>

    <hr>

    <a href="/task274/reset">Почати спочатку</a>
    <br><br>

    <a href="/tasks">До вибору задач</a>
    """

    return page("Задача 27.4", content)


@app.route("/task274/process", methods=["POST"])
def process_274():

    if not check_auth():
        return redirect(url_for("login"))

    value = request.form.get("number", "").strip()

    try:
        number = int(value)
    except ValueError:
        return render_274("Введіть ціле число.")

    # Якщо введено 0 — завершення послідовності
    if number == 0:

        sequence = session.get("sequence", [])
        changes = session.get("changes", 0)

        sequence_text = ", ".join(map(str, sequence))

        content = f"""
        <h1>Результат задачі 27.4</h1>

        <h3>Введена послідовність:</h3>

        <p>{sequence_text}</p>

        <h2>
            Кількість змін знаку: {changes}
        </h2>

        <p class="success">
            Послідовність завершена.
        </p>

        <hr>

        <a href="/task274/reset">
            <button>Розв'язати ще раз</button>
        </a>

        <br>

        <a href="/tasks">
            До вибору задач
        </a>
        """

        return page("Результат 27.4", content)

    sequence = session.get("sequence", [])
    changes = session.get("changes", 0)

    # Нульові елементи не допускаються
    if number == 0:
        return render_274("Число 0 завершує послідовність.")

    # Перевірка зміни знаку
    if len(sequence) > 0:

        previous = sequence[-1]

        if (previous > 0 and number < 0) or \
           (previous < 0 and number > 0):

            changes += 1

    sequence.append(number)

    session["sequence"] = sequence
    session["changes"] = changes

    # Повертаємо сторінку.
    # Поле введення буде очищене.
    return render_274()


@app.route("/task274/reset")
def reset_274():

    if not check_auth():
        return redirect(url_for("login"))

    session["sequence"] = []
    session["changes"] = 0

    return redirect(url_for("task274"))


# ============================================================
# 4. Задача 27.10 — розміри матриць
# ============================================================

@app.route("/dimensions", methods=["GET", "POST"])
def dimensions():

    if not check_auth():
        return redirect(url_for("login"))

    error = ""

    if request.method == "POST":

        try:
            n1 = int(request.form["n1"])
            m1 = int(request.form["m1"])

            n2 = int(request.form["n2"])
            m2 = int(request.form["m2"])

        except (ValueError, KeyError):

            error = "Розміри повинні бути цілими числами."

        else:

            if n1 <= 0 or m1 <= 0 or n2 <= 0 or m2 <= 0:

                error = "Розміри повинні бути більшими за 0."

            elif m1 != n2:

                error = (
                    "Неможливо перемножити матриці. "
                    "Кількість стовпців першої матриці "
                    "повинна дорівнювати кількості рядків "
                    "другої матриці."
                )

            else:

                session["n1"] = n1
                session["m1"] = m1

                session["n2"] = n2
                session["m2"] = m2

                return redirect(url_for("matrix1"))

    error_html = ""

    if error:
        error_html = f"""
        <p class="error">{error}</p>
        """

    content = f"""
    <h1>Задача 27.10</h1>

    <p>
        Введіть розміри двох матриць.
    </p>

    {error_html}

    <form method="post">

        <h3>Перша матриця A</h3>

        <p>
            Кількість рядків:
            <input
                type="number"
                name="n1"
                min="1"
                required
            >
        </p>

        <p>
            Кількість стовпців:
            <input
                type="number"
                name="m1"
                min="1"
                required
            >
        </p>

        <h3>Друга матриця B</h3>

        <p>
            Кількість рядків:
            <input
                type="number"
                name="n2"
                min="1"
                required
            >
        </p>

        <p>
            Кількість стовпців:
            <input
                type="number"
                name="m2"
                min="1"
                required
            >
        </p>

        <button type="submit">
            Перейти до введення матриць
        </button>

    </form>

    <br>

    <a href="/tasks">
        До вибору задач
    </a>
    """

    return page("Розміри матриць", content)


# ============================================================
# 5. Введення першої матриці
# ============================================================

@app.route("/matrix1", methods=["GET", "POST"])
def matrix1():

    if not check_auth():
        return redirect(url_for("login"))

    n = session.get("n1")
    m = session.get("m1")

    if n is None or m is None:
        return redirect(url_for("dimensions"))

    if request.method == "POST":

        matrix = []

        for i in range(n):

            row = []

            for j in range(m):

                value = request.form.get(
                    f"a_{i}_{j}",
                    ""
                ).strip()

                if value == "":
                    return render_matrix1(
                        n,
                        m,
                        f"Поле [{i + 1}, {j + 1}] не заповнено."
                    )

                try:
                    number = float(value)

                except ValueError:
                    return render_matrix1(
                        n,
                        m,
                        f"Поле [{i + 1}, {j + 1}] "
                        f"повинно містити число."
                    )

                row.append(number)

            matrix.append(row)

        session["matrix1"] = matrix

        return redirect(url_for("matrix2"))

    return render_matrix1(n, m)


def render_matrix1(n, m, error=""):

    error_html = ""

    if error:
        error_html = f"""
        <p class="error">{error}</p>
        """

    table = "<table>"

    for i in range(n):

        table += "<tr>"

        for j in range(m):

            table += f"""
            <td>
                <input
                    class="matrix-input"
                    type="number"
                    step="any"
                    name="a_{i}_{j}"
                    required
                >
            </td>
            """

        table += "</tr>"

    table += "</table>"

    content = f"""
    <h1>Введення першої матриці A</h1>

    <p>
        Розмір матриці:
        <b>{n} × {m}</b>
    </p>

    {error_html}

    <form method="post">

        {table}

        <button type="submit">
            Зберегти та перейти до другої матриці
        </button>

    </form>
    """

    return page("Перша матриця", content)


# ============================================================
# 6. Введення другої матриці
# ============================================================

@app.route("/matrix2", methods=["GET", "POST"])
def matrix2():

    if not check_auth():
        return redirect(url_for("login"))

    n = session.get("n2")
    m = session.get("m2")

    if n is None or m is None:
        return redirect(url_for("dimensions"))

    if request.method == "POST":

        matrix = []

        for i in range(n):

            row = []

            for j in range(m):

                value = request.form.get(
                    f"b_{i}_{j}",
                    ""
                ).strip()

                if value == "":
                    return render_matrix2(
                        n,
                        m,
                        f"Поле [{i + 1}, {j + 1}] не заповнено."
                    )

                try:
                    number = float(value)

                except ValueError:
                    return render_matrix2(
                        n,
                        m,
                        f"Поле [{i + 1}, {j + 1}] "
                        f"повинно містити число."
                    )

                row.append(number)

            matrix.append(row)

        session["matrix2"] = matrix

        return redirect(url_for("matrix_result"))

    return render_matrix2(n, m)


def render_matrix2(n, m, error=""):

    error_html = ""

    if error:
        error_html = f"""
        <p class="error">{error}</p>
        """

    table = "<table>"

    for i in range(n):

        table += "<tr>"

        for j in range(m):

            table += f"""
            <td>
                <input
                    class="matrix-input"
                    type="number"
                    step="any"
                    name="b_{i}_{j}"
                    required
                >
            </td>
            """

        table += "</tr>"

    table += "</table>"

    content = f"""
    <h1>Введення другої матриці B</h1>

    <p>
        Розмір матриці:
        <b>{n} × {m}</b>
    </p>

    {error_html}

    <form method="post">

        {table}

        <button type="submit">
            Обчислити добуток
        </button>

    </form>
    """

    return page("Друга матриця", content)


# ============================================================
# 7. Результат множення матриць
# ============================================================

@app.route("/matrix-result")
def matrix_result():

    if not check_auth():
        return redirect(url_for("login"))

    A = session.get("matrix1")
    B = session.get("matrix2")

    if A is None or B is None:
        return redirect(url_for("dimensions"))

    n = len(A)
    m = len(A[0])
    p = len(B[0])

    # Створення результуючої матриці
    C = []

    for i in range(n):

        row = []

        for j in range(p):

            value = 0

            for k in range(m):

                value += A[i][k] * B[k][j]

            row.append(value)

        C.append(row)

    content = f"""
    <h1>Результат множення матриць</h1>

    <h2>Матриця A</h2>

    {matrix_html(A)}

    <h2>Матриця B</h2>

    {matrix_html(B)}

    <h2>Результат A × B</h2>

    {matrix_html(C)}

    <hr>

    <a href="/matrix-reset">
        <button>Ввести нові матриці</button>
    </a>

    <br>

    <a href="/tasks">
        До вибору задач
    </a>
    """

    return page("Результат", content)


# ============================================================
# Очищення даних матриць
# ============================================================

@app.route("/matrix-reset")
def matrix_reset():

    if not check_auth():
        return redirect(url_for("login"))

    keys = [
        "n1",
        "m1",
        "n2",
        "m2",
        "matrix1",
        "matrix2"
    ]

    for key in keys:
        session.pop(key, None)

    return redirect(url_for("dimensions"))


# ============================================================
# Запуск сервера
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
