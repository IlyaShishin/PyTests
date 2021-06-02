import pytest

from main import get_doc_owner_name, add_new_shelf, delete_doc, get_doc_shelf, add_new_doc, get_new_folder, \
    get_files_list


class TestPyTest:

    def setup(self):
        print('method setup')

    def test_get_doc_owner_name(self):
        assert get_doc_owner_name('11-2') == "Геннадий Покемонов"

    def test_add_new_shelf(self):
        assert add_new_shelf('2') == ('2', False)

    def test_delete_doc(self):
        assert delete_doc('11-2') == ('11-2', True)

    def test_get_doc_shelf(self):
        assert get_doc_shelf('10006') == '2'

    def test_add_new_doc(self):
        assert add_new_doc('3') == '3'

    @pytest.mark.parametrize('folder_name, expected_result', [('Folder_for_test', 201), ('Folder_for_test', 409),
                                                              ('Another_folder', 201)])
    def test_get_new_folder(self, folder_name, expected_result):
        assert get_new_folder(folder_name) == expected_result

    @pytest.mark.parametrize('folder_name, expected_result', [('Folder_for_test', 'Папка есть на Яндекс.Диск'),
                                                              ('Folder_for_test', 'Папки нет на Яндекс.Диск'),
                                                              ('Some_folder', 'Папки нет на Яндекс.Диск')])
    def test_get_files_list(self, folder_name, expected_result):
        assert get_files_list(folder_name) == expected_result

    def teardown(self):
        print('method teardown')
