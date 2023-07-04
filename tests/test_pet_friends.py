from api import PetFriends
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet_with_valid_data(name="Larry", animal_type="dog",
                                      age='1', pet_photo="images/dog.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_update_pet_info_successfully(name="Sally", animal_type="dog", age="1"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_delete_pet_successfully():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_new_pet(auth_key, "Kitty", "кот", "7", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# 10 тестов для домашнего задания по модулю 24

def test_create_pet_simple_successfully(name="Кулон", animal_type="кот", age="3"):
    '''1: Проверка метода простого добавления питомца с валидными данными без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet_with_valid_data(pet_photo="images/cat.jpg"):
    '''2: Проверка метода добавления фото к существующему питомцу с валидными данными'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] is not None


def test_get_api_key_for_invalid_user(email="not_real_email@1secmail.net", password="not_real_password"):
    '''3: Получение api-ключа с данными незарегистрированного пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password="sftest"):
    '''4: Получение api-ключа с данными зарегистрированного пользователя с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_invalid_user_valid_password(email="hterocephalus@yandex.ru", password=valid_password):
    '''5: Получение api-ключа с опечаткой в электронной почте и правильным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
     '''6: Получение списка питомцев с несуществующим api-ключом'''
     _, auth_key = pf.get_api_key(valid_email, valid_password)

     # замена ключа на несуществующий
     auth_key = invalid_auth_key

     status, result = pf.get_list_of_pets(auth_key, filter)
     assert status != 200


def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''7: Получение списка "моих питомцев" зарегистрированного пользователя'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_create_pet_simple_wrong_age(name="Горгона", animal_type="медуза", age="много"):
    '''8: Добавление питомца (без фото) с неверно написанным возрастом.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age


def test_post_new_pet_with_invalid_photo(name="Текст", animal_type="текстовый файл",
                                      age='8 мин', pet_photo="images/photo.txt"):
    '''9: Добавление питомца с текстовым файлом вместо фото.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None


def test_create_pet_simple_invalid_data(name="", animal_type="", age=""):
    '''Тест 10: Проверка метода простого добавления питомца (без фото) с пустыми полями.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name





