import pytest

from typing import Optional

from lanyard import LanyardConfig
from lanyard.constant import API_BASE_URL, API_DEFAULT_VERSION
from lanyard.exception import UnknownAPIVersionError


class TestLanyardConfig:
    def test_init(self) -> None:
        config: LanyardConfig = LanyardConfig()

        assert config.base_url == API_BASE_URL
        assert config.api_version == API_DEFAULT_VERSION
        assert config.url == "https://api.lanyard.rest/v1/"
        assert config.headers == {"Content-Type": "application/json"}
        assert config.token is None
        assert config.timeout is None
        assert config.raise_for_status is True

    def test_custom_init(self) -> None:
        base_url: str = "https://custom.example.com/"
        api_version: int = 2
        token: str = "test_token_123"
        timeout: float = 30.0
        raise_for_status: bool = True

        config: LanyardConfig = LanyardConfig(
            base_url=base_url,
            api_version=api_version,
            token=token,
            timeout=timeout,
            raise_for_status=raise_for_status,
        )

        assert config.base_url == base_url
        assert config.api_version == api_version
        assert config.url == "https://custom.example.com/v2/"
        assert config.headers == {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        assert config.token == token
        assert config.timeout == timeout
        assert config.raise_for_status is raise_for_status

    @pytest.mark.parametrize("token", [None, "xxxxxe47b4dedc260f13a0ec57d78745", ""])
    def test_headers_param(self, token: Optional[str]) -> None:
        config: LanyardConfig = LanyardConfig(token=token)

        if token is None:
            assert config.headers == {"Content-Type": "application/json"}
        else:
            assert config.headers == {
                "Content-Type": "application/json",
                "Authorization": token,
            }

    @pytest.mark.parametrize(
        "api_version, should_raise",
        [
            (1, False),
            (2, False),
            (0, True),
            (-1, True),
        ],
    )
    def test_api_version_param(self, api_version: int, should_raise: bool) -> None:
        if should_raise:
            with pytest.raises(UnknownAPIVersionError):
                LanyardConfig(api_version=api_version)
        else:
            config: LanyardConfig = LanyardConfig(api_version=api_version)
            assert config.api_version == api_version
