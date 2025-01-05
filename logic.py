from bs4 import BeautifulSoup
import requests
import os
import lxml
import json

class Download_links:
    """Выгрузка HTML страниц"""

    def __init__(self, url="https://www.lebenindeutschland.eu/fragenkatalog", file_name="index", path="data/html/"):
        self.url = url
        self.file_name = file_name
        self.path = path
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
        }

    # Выгрузка html страниц
    def download_html(self):
        request = requests.get(url=self.url, headers=self.headers) # отправляем запрос на сервер
        result = request.text # переводим полученный ответ от сервера в текст

        # записываем в локальный html файл
        writer = Local_read_write(file_name=self.file_name, data=result, path=self.path)
        writer.write_html_local()

        return result

    # Выгрузка img к вопросам
    def download_img(self):
        # Создаем директорию, если она не существует
        os.makedirs(self.path, exist_ok=True)

        # Определяем имя файла из URL
        file_name = os.path.basename(self.url)
        file_path = os.path.join(self.path, file_name)

        # Загружаем изображение
        response = requests.get(self.url, stream=True)
        response.raise_for_status()  # Проверяем успешность запроса

        # Сохраняем файл
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

class Local_read_write:
    """Чтение и запись локальных html и json файлов"""

    def __init__(self, data=None, file_name=None, path=None):
        self.data = data # данные для записи
        self.file_name = file_name # имя создаваемого файла
        self.path = path # путь к файлу

    # Запись локальных html файлов
    def write_html_local(self):
        # Создаем директорию
        os.makedirs(self.path, exist_ok=True)  # Создаст директорию, но не файл

        # Создаем полный путь для записи файла
        full_path_write = os.path.join(f"{self.path}{self.file_name}.html")

        with open(full_path_write, "w", encoding="utf-8") as file:
            file.write(self.data)

    # Чтение локальных html файлов
    def read_html_local(self):
        # Объеденяем путь и имя файла
        path_html = os.path.join(self.path, f"{self.file_name}.html")

        # Открываем файл
        with open(path_html, "r", encoding="utf-8") as file:
            html_content = file.read()  # Читаем содержимое файла

        return html_content

    # Запись локальных json файлов
    def write_json_local(self):
        # Создаем директорию
        os.makedirs(self.path, exist_ok=True)  # Создаст директорию, но не файл

        # Создаем полный путь для записи файла
        full_path_write = os.path.join(f"{self.path}{self.file_name}.json")

        # Записываем данные в JSON файл
        with open(full_path_write, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)  # ensure_ascii=False для сохранения юникода

    # Чтение локальных json файлов
    def read_json_local(self):
        # Открываем JSON файл
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Извлекаем ключи и значения
        result = [(key, value) for key, value in data.items()]
        # Возвращаем в формате [(Номер вопроса:{Данные})]
        return result

    # Объединение нескольких json в один общий
    def merge_json_local(self, file_name="Dafault", path_read=None, path_write="data/json/merged"):
        merged_data = {} # временный общий словарь
        self.path_read = path_read # путь к json файлам которые нужно объединить
        self.path_write = path_write # путь для сохранения объединенного json
        self.file_name = file_name # имя для конечного файла

        # Перебираем все файлы в папке
        for file_name in os.listdir(path_read): # получаем имена файлов по указанному пути
            file_path = os.path.join(path_read, file_name) # объединяем путь и имя файла

            # Проверяем, что это JSON файл
            if os.path.isfile(file_path) and file_name.endswith(".json"):
                # Устанавливаем текущий путь для чтения
                self.path = file_path
                # Чтение данных из файла
                data = self.read_json_local()
                # Добавляем данные в общий словарь
                merged_data.update(data)

            # Сортировка временного словаря по номеру вопроса (извлекаем числа из ключей)
            sorted_data = dict(sorted(merged_data.items(), key=lambda item: int(item[0].split('№')[1].strip())))

            # Записываем объединенные данные из временного словаря в json
            self.data = sorted_data
            self.path = path_write
            self.write_json_local()

class BeautifulSoup4(Local_read_write):

    # Сбор данных с HTML страниц
    def __init__(self, path="data/html/", file_name="index", path_json_data="data/json/"):
        self.path = path
        self.file_name = file_name
        self.path_json_data = path_json_data

        # Наследование класса Local_read_write
        super().__init__(path=self.path, file_name=self.file_name)  # Вызываем конструктор родительского класса

    def bs4_index(self):
        """Выгружаем категории из index.html"""

        # Получаем содержимое HTML файла из родительского класса
        html = self.read_html_local()

        soup_index = BeautifulSoup(html, "lxml")

        # Собираем блоки с категориями
        all_category_blocks = soup_index.find_all("ul", class_="flex flex-wrap")

        # Собираем все категории по блокам и сохраняем в словарь
        category_dikt = {"Allgemein": {}, "Bundesland": {}}  # Создаем пустые словари для Allgemein и Bundesland

        for block in all_category_blocks:  # Перебираем блоки
            category = block.find_all("a")  # Непосредственно ищем <a> в блоке

            for a in category:
                url = a.get("href")  # Получаем ссылку
                name = f"{((a.text).strip()).replace(' ', '_')}"  # Название категории (очищаем от пробелов и заменяем на "_")

                if url:  # Проверяем, что ссылка не None
                    # Проверяем, содержит ли название слова "Fragen"
                    if "Fragen" in name:
                        # Если содержит "Fragen", добавляем в Allgemein
                        category_dikt["Allgemein"][name] = url
                    else:
                        # Если не содержит "Fragen", добавляем в Bundesland
                        category_dikt["Bundesland"][name] = url

        # Записываем полученные даныне в json
        self.path = self.path_json_data
        self.data = category_dikt
        self.write_json_local()

    def bs4_scraping_data(self):
        """Выгружаем данные из html страниц категорий"""
        # Получаем html текст
        html = self.read_html_local()

        soup_html = BeautifulSoup(html, "lxml")

        # Ищем все блоки вопросов
        question_blocks = soup_html.find_all("div", class_="p-4 mb-8 bg-white dark:bg-gray-900 shadow rounded-lg max-w-lg")

        # Парсим вопросы
        questions_dict = {}

        for block in question_blocks:
            # Извлекаем ключ (например, "Frage №1")
            header = block.find("h3")
            if header:
                # Извлекаем текст заголовка
                header_text = header.get_text(strip=True)
                key, question = header_text.split(":", 1)  # Разделяем на ключ и текст вопроса

                # Ищем изображение
                image_tag = block.find("img")
                image_url = f"https://www.lebenindeutschland.eu{image_tag.get('src')}" if image_tag else None

                # Извлекаем варианты ответов
                options_tags = block.find_all("div", class_="mb-4")
                options = {}
                correct_answer = None

                option_keys = ["A", "B", "C", "D"]  # Метки вариантов
                for idx, option_tag in enumerate(options_tags):
                    # Извлекаем текст варианта ответа
                    span = option_tag.find("span")
                    if span:
                        option_text = span.get_text(strip=True).strip("✓—").strip()  # Убираем лишние символы

                        # Если это правильный ответ (проверяем класс фона)
                        if "bg-green-100" in span.get("class", "") or "dark:bg-green-800" in span.get("class", ""):
                            correct_answer = {option_keys[idx]: option_text}

                        # Добавляем вариант в словарь
                        if idx < len(option_keys):
                            options[option_keys[idx]] = option_text

                # Добавляем данные в словарь
                questions_dict[key.strip()] = {
                    "question": question.strip(),
                    "image": image_url,
                    "options": options,
                    "correct_answer": correct_answer
                }

            # Записываем полученные даныне в json
            self.path = self.path_json_data
            self.data = questions_dict
            self.write_json_local()

class Main(BeautifulSoup4, Download_links, Local_read_write):
    ## Получаем index.html
    index_html = Download_links()
    index_html.download_html()
    print("Файл index.html успешно выгружен.")

    ## Собираем ссылки категорий в json
    bs4_index_html = BeautifulSoup4()
    bs4_index_html.bs4_index()
    print("Ссылки на категории успешно сохранены в index.json.")

    ## Выгружаем html страницы категорий

    # Создаем экземпляр класса и читаем JSON данные
    local_rw = Local_read_write(path="data/json/index.json")
    json_data = local_rw.read_json_local()

    # Итарации и сбор переменных
    for key, value in json_data:
        path = "data/html/"
        category = key  # Назначаем текущий ключ в переменную category

        # Вложенный цикл для обработки вопросов внутри категории
        for file_name, url in value.items():
            category_path = os.path.join(path, f"{category}/")

            category_html = Download_links(url=url, file_name=file_name, path=category_path)
            category_html.download_html()
    print("HTML файлы категорий успешно выгружены.")

    ## Собираем данные в json по категориям
    folder_paths = [
        "data/html/Allgemein/",
        "data/html/Bundesland/"
    ]
    # Итерация по каждому пути в списке
    for folder_path in folder_paths:
        # Получаем список всех файлов в текущей папке
        files = os.listdir(folder_path)

        # Итерация по каждому файлу в папке
        for file_name in files:
            # Если файл имеет расширение .html
            if file_name.endswith(".html"):
                file_path = os.path.join(folder_path, file_name)
                print(f"Собираем данные из файла: {file_path}")

                # Заменяем "html" на "json" в пути
                path_json_category = folder_path.replace("html", "json")
                file_name = file_name.replace(".html", "")
                scraping_data_allgeemein = BeautifulSoup4(path=folder_path, file_name=file_name,
                                                                path_json_data=path_json_category)
                scraping_data_allgeemein.bs4_scraping_data()
    print("Все данные успешно собраны и сохранены.")

    ## Объеденяем json файлы (Allgemein, Bundesland и All_categories)
    folder_paths = [
        "data/json/Allgemein/",
        "data/json/Bundesland/",
        "data/json/merged/"
    ]
    for folder_path in folder_paths:
        category = os.path.basename(folder_path.rstrip('/'))
        category_name = f"{category}_merged"
        if category == "merged":
            category = "All_categories"
            category_name = "All_categories"
        merge = Local_read_write()
        merge.merge_json_local(file_name=category_name, path_read=folder_path, path_write="data/json/merged/")
        print(f"Категория {category} успешно объединена.")

    # Загружаем изображения
    json_links = Local_read_write(path="data/json/merged/All_categories.json")
    json = json_links.read_json_local()

    # Перебираем все элементы списка
    for frage, data in json:
        # Проверяем, есть ли изображение
        url = data.get('image')
        if url:
            # Если изображение есть, выводим ссылку (а не None), выполняем следующее действие
            img = Download_links(url=url, path="data/img/")
            img.download_img()
    print("Все изображения успешно загружены!")
    print("Все данные успешно обновлены и готовы к использованию.")