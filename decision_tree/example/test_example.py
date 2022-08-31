import pytest

from decision_tree.example.container import ValidationTreeContainer
from decision_tree.example.entities import SessionDto


@pytest.fixture
def tree_container():
    yield ValidationTreeContainer()


@pytest.mark.parametrize(
    "dto, result",
    [
        pytest.param(
            SessionDto(
                device_session_id="any",
                user_name="name",
                pass_hash="hash",
                auth_required=True,
            ),
            True,
            id="all fields are valid",
        ),
        pytest.param(
            SessionDto(
                device_session_id="any",
                user_name=None,
                pass_hash=None,
                auth_required=False,
            ),
            True,
            id="no auth required, but session is valid",
        ),
        pytest.param(
            SessionDto(
                device_session_id="any",
                user_name=None,
                pass_hash=None,
                auth_required=True,
            ),
            False,
            id="name is missing",
        ),
        pytest.param(
            SessionDto(
                device_session_id="any",
                user_name="any",
                pass_hash=None,
                auth_required=True,
            ),
            False,
            id="pass hash is missing",
        ),
        pytest.param(
            SessionDto(
                device_session_id="",
                user_name=None,
                pass_hash=None,
                auth_required=False,
            ),
            False,
            id="no auth required, empty session id",
        ),
        pytest.param(
            SessionDto(
                device_session_id="",
                user_name="any",
                pass_hash="any",
                auth_required=True,
            ),
            False,
            id="no auth required, empty session id",
        ),
        pytest.param(
            SessionDto(
                device_session_id="any",
                user_name="any",
                pass_hash="any",
                auth_required=True,
                _user_exists_in_db=False,
            ),
            False,
            id="user does not exist in db",
        ),
    ],
)
def test_tree_container(tree_container, dto, result):
    assert tree_container.calculate(dto).valid is result
