import logic

# if __name__ == '__main__':

    # # ТЕСТЫ

    ##########
    # # Тест_1 метода write_html_local класса Local_read_write
    # html_write_test = logic.Local_read_write(data="123", file_name="test", path="data/html/")
    # html_write_test.write_html_local()

    ##########
    # # Тест_2 метода read_html_local класса Local_read_write
    # html_read_test = logic.Local_read_write(file_name="index_test", path="data/html/")
    # html_read_test.read_html_local()

    ##########
    # # Тест_3 метода write_json_local класса Local_read_write
    # data = {
    #         "Frage №8": {
    #             "question": "Die deutsche Hauptstadt?",
    #             "image": None,
    #             "options": {
    #                 "A": "Berlin",
    #                 "B": "Munich",
    #                 "C": "Hamburg",
    #                 "D": "Cologne"
    #             },
    #             "correct_answer": {"A": "Berlin"}
    #         },
    #         "Frage №9": {
    #             "question": "Welches Land ist das größte in Europa?",
    #             "image": None,
    #             "options": {
    #                 "A": "France",
    #                 "B": "Germany",
    #                 "C": "Russia",
    #                 "D": "Poland"
    #             },
    #             "correct_answer": {"C": "Russia"}
    #         }
    #     }
    # json_write_test = logic.Local_read_write(data=data, file_name="test_1", path="data/json/")
    # json_write_test.write_json_local()

    ##########
    # # Тест_4 метода read_json_local класса Local_read_write
    # json_read_rest = logic.Local_read_write(path="data/json/test.json")
    # print(json_read_rest.read_json_local())

    ##########
    # # Тест_5 метода read_json_local класса Local_read_write
    # json_merge_test = logic.Local_read_write(file_name="merged")
    # json_merge_test.merge_json_local(path_read="data/json/", path_write="data/json/merged/")

    ##########
    # # Тест_6 метода download_html класса Download_links
    # index_html = logic.Download_links()
    # index_html.download_html()

    ##########
    # # Тест_7 метода bs4_index класса BS4
    # bs4_index = logic.BeautifulSoup4(path="data/html/", file_name="index", path_json_data="data/json/")
    # bs4_index.bs4_index()

    ##########
    # # Тест_8 метода bs4_scraping_data класса BS4
    # bs4_scraper = logic.BeautifulSoup4(path="data/html/allgemein/", file_name="Fragen_1_–_30", path_json_data="data/json/allgemein/")
    # bs4_scraper.bs4_scraping_data()

    ##########
    # # Тест_9 метода download_img класса Download_links
    # img = logic.Download_links(url="https://www.lebenindeutschland.eu/img/questions/021.png", path="data/img/")
    # img.download_img()