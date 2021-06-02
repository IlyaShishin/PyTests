import requests
import json


documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def check_document_existance(user_doc_number):
    doc_founded = False
    for current_document in documents:
        doc_number = current_document['number']
        if doc_number == user_doc_number:
            doc_founded = True
            break
    return doc_founded


def get_doc_owner_name(user_doc_number):
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for current_document in documents:
            doc_number = current_document['number']
            if doc_number == user_doc_number:
                return current_document['name']


def get_all_doc_owners_names():
    users_list = []
    for current_document in documents:
        try:
            doc_owner_name = current_document['name']
            users_list.append(doc_owner_name)
        except KeyError:
            pass
    return set(users_list)


def remove_doc_from_shelf(doc_number):
    for directory_number, directory_docs_list in directories.items():
        if doc_number in directory_docs_list:
            directory_docs_list.remove(doc_number)
            break


def add_new_shelf(shelf_number=''):
    # if not shelf_number:
    #     shelf_number = '2'
    if shelf_number not in directories.keys():
        directories[shelf_number] = []
        return shelf_number, True
    return shelf_number, False


def append_doc_to_shelf(doc_number, shelf_number):
    add_new_shelf(shelf_number)
    directories[shelf_number].append(doc_number)


def delete_doc(user_doc_number):
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for current_document in documents:
            doc_number = current_document['number']
            if doc_number == user_doc_number:
                documents.remove(current_document)
                remove_doc_from_shelf(doc_number)
                return doc_number, True


def get_doc_shelf(user_doc_number):
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for directory_number, directory_docs_list in directories.items():
            if user_doc_number in directory_docs_list:
                return directory_number


def move_doc_to_shelf():
    user_doc_number = '2207 876234'
    user_shelf_number = '3'
    remove_doc_from_shelf(user_doc_number)
    append_doc_to_shelf(user_doc_number, user_shelf_number)
    print('Документ номер "{}" был перемещен на полку номер "{}"'.format(user_doc_number, user_shelf_number))


def show_document_info(document):
    doc_type = document['type']
    doc_number = document['number']
    doc_owner_name = document['name']
    print('{} "{}" "{}"'.format(doc_type, doc_number, doc_owner_name))


def show_all_docs_info():
    print('Список всех документов:\n')
    for current_document in documents:
        show_document_info(current_document)


def add_new_doc(new_doc_shelf_number):
    new_doc_number = '123'
    new_doc_type = 'passport'
    new_doc_owner_name = 'Klint EastWood'
    new_doc = {
        "type": new_doc_type,
        "number": new_doc_number,
        "name": new_doc_owner_name
    }
    documents.append(new_doc)
    append_doc_to_shelf(new_doc_number, new_doc_shelf_number)
    return new_doc_shelf_number


def secretary_program_start():
    """
    ap - (all people) - команда, которая выводит список всех владельцев документов
    p – (people) – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
    l – (list) – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
    s – (shelf) – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
    a – (add) – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип,
    имя владельца и номер полки, на котором он будет храниться.
    d – (delete) – команда, которая спросит номер документа и удалит его из каталога и из перечня полок;
    m – (move) – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую;
    as – (add shelf) – команда, которая спросит номер новой полки и добавит ее в перечень;
    q - (quit) - команда, которая завершает выполнение программы
    """
    print(
        'Вас приветствует программа помошник!\n',
        '(Введите help, для просмотра списка поддерживаемых команд)\n'
    )
    while True:
        user_command = input('Введите команду - ')
        if user_command == 'p':
            owner_name = get_doc_owner_name()
            print('Владелец документа - {}'.format(owner_name))
        elif user_command == 'ap':
            uniq_users = get_all_doc_owners_names()
            print('Список владельцев документов - {}'.format(uniq_users))
        elif user_command == 'l':
            show_all_docs_info()
        elif user_command == 's':
            directory_number = get_doc_shelf()
            print('Документ находится на полке номер {}'.format(directory_number))
        elif user_command == 'a':
            print('Добавление нового документа:')
            new_doc_shelf_number = add_new_doc()
            print('\nНа полку "{}" добавлен новый документ:'.format(new_doc_shelf_number))
        elif user_command == 'd':
            doc_number, deleted = delete_doc()
            if deleted:
                print('Документ с номером "{}" был успешно удален'.format(doc_number))
        elif user_command == 'm':
            move_doc_to_shelf()
        elif user_command == 'as':
            shelf_number, added = add_new_shelf()
            if added:
                print('Добавлена полка "{}"'.format(shelf_number))
        elif user_command == 'help':
            print(secretary_program_start.__doc__)
        elif user_command == 'q':
            break

# ЗАДАНИЕ 2


yadisk_token = 'Здесь пишем токен'
headers = {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(yadisk_token)
        }


def get_new_folder(new_folder):
    """Функция создает новую папку на Яндекс.Диск"""
    up_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        'path': new_folder,
        'overwrite': 'true'
    }
    response = requests.put(up_url, headers=headers, params=params)
    print(response.status_code)
    return response.status_code


def get_files_list(folder_name):
    """Функция проверяет наличие папки на Яндекс.Диск"""
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        'path': f'disk:/',
        'limit': '5',
        'fields': '_embedded.items.name'
    }
    response = requests.get(files_url, headers=headers, params=params).json()
    value_list = []
    for lines in response['_embedded']['items']:
        for value in lines.values():
            value_list.append(value)
    if folder_name in value_list:
        return 'Папка есть на Яндекс.Диск'
    else:
        return 'Папки нет на Яндекс.Диск'


# if __name__ == '__main__':
#     # secretary_program_start()
#     get_new_folder('Folder_for_test')
#     get_files_list('Folder_for_test')
