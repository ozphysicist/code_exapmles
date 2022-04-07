import datetime
from typing import Dict

from db_utils import connections
from sqlalchemy import and_, select

from test.system import System
from test.lib.test_object import TestObject
from test.db.test_db import TestDbTable, TestDbTableDetl


def get_object(
        *,
        datadriven: Dict,
        system: System,
) -> Tuple:
    test_object = TestObject(
        dd=replace_dates(datadriven),
        system=system,
    )
    system.start_process(   
        test_object_id=test_object.test_object_id,
    )
    test_object.check_loaded_obj_in_db()
    return test_object


def get_process_id(
        *,
        test_object_id: str,
        action_id: str,
) -> str:
    with connections.db_transaction(DB_CONNECT_TEST_DB) as conn:
        statement = select(
            [TestDbTable.ID],
        ).where(
            and_(
                TestDbTable.OBJECTID == test_object_id,
                TestDbTable.ACTIONID == action_id,
            ),
        )
        result = str(conn.execute(statement).fetchone()[0])
    return result


def get_process_date(test_object: TestObject) -> str:
    with connections.db_transaction(DB_CONNECT_TEST_DB) as conn:
        statement = select(
            [TestDbTableDetl.PROCESSDATE],
        ).where(TestDbTableDetl.OBJECTID == test_object.desc.id)
        result = conn.execute(statement).fetchone()[0]
    return result = str(result.strftime('%d.%m.%Y'))


def generate_param_info(test_object: TestObject) -> str:
    params = []
    for param in get_enable_paramid(test_object_id=test_object.desc.id):
        params.append(f'{param["PARAMID"]} - {get_param_name(param_id=param["PARAMID"])}')
    params_info = ', \r'.join(params)
    return params_info
