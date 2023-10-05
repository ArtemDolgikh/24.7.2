import os
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

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


def test_add_new_pet_with_valid_data(name='Vusha', animal_type='rat',
                                     age='3', pet_photo='images/Funny-rat.jpg'):
    """Добавление питомца с валидными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем ответ с результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Gosha", "rat", "2", "images/Funny-rat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Yan', animal_type='RAT', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_successful_add_pet_photo(pet_photo="images/Badger.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key_invalid(email, password)
    assert status == 403


def test_unsuccessful_add_pet_photo(pet_photo="images/Tiger.pdf"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

        assert status == 500


def test_add_new_pet_with_invalid_data(name='', animal_type='',
                                     age='', pet_photo='images/Badger.jpg'):
    """Добавление питомца с невалидными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403


def test_add_new_pet_with_invalid_data(name='WL{G22f4MLUT70P?3LrpuFBhTaFWzy[PV5F,4np&waY0_Kn-X.N8aV{!,vmSawS/:[%Re6:VFh$U$DGLpyp)#w??W0,F=5,[t*5:-73rQ)+wQc5Qzm0#B_Z])3$k$LA?yhWc24f7/MErWtR/KgMxY;-2$K?7w*9?)m_S.Cc0&/cpjEQ:Qe3dm1({rgf([2%mmu;Y-Q,-wgtWD+,i={vSC@yG$d3#7}$B8*-KqVW*_kYdUNL!ar?yVU%+dB]',
                                       animal_type='_JF{LaB8!r:,r[!Z;+ZCti64$S1;C1M}agX}[[1zmuMW3#kv4_naxWw_PvVC207:_8CA3ic}Ciq,AH_88pbm/{Jp/AvX&]L3hjj.{vppMTVK&Ri=?S-,@daR6}LE8TzGn(KGJ+7.J9N!wF-CU%/3eM0jNN8Naq3?uSwx{rXn18}_)t2v+d$yxWm##d{YDd$7b!e,W$8;HyU[Bf4kwDK-(+8tmRT!{({P_qv)rU=a9x.&P.!Z.SP;bA1Y(=G',
                                     age='!Wg4L#4]/J/q_2$aGdxN/71/6E{KL533f=ani!yW-d2{;zda*=P5z;Bw7:N$pdHY*({hc%A{mefrGhu?gFN42UR;QctE)1EL6Q4b@tm{wT8u?V!W%jJKJA{$EHNEyB#JfV0&fPR6@HNmE0;J7zY(:1JNJg{ab5DC1v+%k3$.T$&5L]?c/W=6i4=x,GQ/zw4EF%HDHmi5]XEB4yAV,.vS-47,/ax/4HBa-K_+6d-/DHx&pZa@YC_qFAM;zvg',
                                       pet_photo='images/Funny-rat.jpg'):
    """Добавление питомца с невалидными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403