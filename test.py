import allure
from asserts import assert_true

from lib.utils import mapping_test_object_params
from test.lib.test_object import TestObject
from test.system import System


@allure.epic('[TEST-001]: Передача параметров')
@allure.story('Проверка маппинга параметров тестового объекта')
def test_mapping_test_object_parameters(
        system: System,
        f_data_s_test_objects_v_map_params: dict,
) -> None:
    with allure.step('Подготовка тестового объекта'):
        test_object = TestObject(
            dd=f_data_s_test_objects_v_map_params,
            system=system,
        )
    with allure.step('Старт процесса и проверка создания объекта'):
        test_object.start()
        test_object.check_loaded_asts_in_db()
    with allure.step('Проверка наличия параметра у тестового объекта'):
        params = test_object.get_test_obj_data().param_id
        param_id = mapping_test_object_params(test_object)
        assert_true(
            param_id in params,
            f'У тестового объекта {test_object.test_object_id} отсутсвует параметр {param_id}',
        )
        