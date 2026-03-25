import requests
import re
from html.parser import HTMLParser

class ArchNewsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True
        elif tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        elif tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        text = data.strip()
        if text:
            self.texts.append(text)

def is_likely_title(text):
    # Пропускаємо короткі меню, розділи, дати та час
    if len(text) < 20:
        return False
    if re.match(r"\d{1,2}:\d{2}", text):
        return False
    if re.match(r"\d+ [а-яА-Я]+", text):
        return False
    # Заголовком вважаємо, якщо є хоча б одне слово з великої літери
    return bool(re.search(r"\b[А-ЯЇІЄҐ][а-яїієґ]+\b", text))

def main():
    date = input("Введіть дату (dd.mm.yyyy): ")
    url = f"https://www.pravda.com.ua/archives/date_{date.replace('.', '')}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    parser = ArchNewsParser()
    parser.feed(response.text)

    # Вибираємо тільки фрагменти, що виглядають як заголовки
    titles = [t for t in parser.texts if is_likely_title(t)]

    # Підрахунок слів з великої літери
    words = []
    for title in titles:
        words += re.findall(r"\b[А-ЯЇІЄҐ][а-яїієґ]+\b", title)

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # Сортуємо по частоті
    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

    print("\nЗаголовки:")
    for t in titles:
        print("-", t)

    print("\nНайчастіші слова:")
    for w, c in top:
        print(f"{w}: {c}")

if __name__ == "__main__":
    main()