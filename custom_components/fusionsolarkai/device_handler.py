import asyncio
import logging
from datetime import timedelta
from functools import partial
from typing import Dict, Any

import requests.exceptions

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL
from .api.fusion_solar_py.client import FusionSolarClient
from .api.fusion_solar_py.exceptions import (
    AuthenticationException,
    CaptchaRequiredException,
    FusionSolarException,
    FusionSolarRateLimit,
)

_LOGGER = logging.getLogger(__name__)


class BaseDeviceHandler:
    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device_info: Dict[str, Any]
    ):
        self.hass = hass
        self.entry = entry
        self.device_info = device_info
        self.device_id = entry.data.get("device_id")
        self.device_name = entry.data.get("device_name")
        self.device_type = entry.data.get("device_type")
        self._consecutive_failures = 0

    async def create_coordinator(self) -> DataUpdateCoordinator:
        """Create and return a data update coordinator"""
        coordinator = DataUpdateCoordinator(
            self.hass,
            _LOGGER,
            name=f"{self.device_name} FusionSolar Data",
            update_method=self._async_update_data,
            update_interval=timedelta(
                seconds=self.entry.options.get(
                    CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL
                )
            ),
        )
        await coordinator.async_config_entry_first_refresh()
        return coordinator

    async def _async_update_data(self) -> Dict[str, Any]:
        """Wrap _async_get_data with consecutive failure tracking."""
        try:
            data = await self._async_get_data()
            self._consecutive_failures = 0
            return data
        except (AuthenticationException, CaptchaRequiredException) as err:
            self._consecutive_failures += 1
            raise ConfigEntryAuthFailed(
                f"Authentication failed: {err}"
            ) from err
        except Exception:
            self._consecutive_failures += 1
            if self._consecutive_failures >= 3:
                _LOGGER.warning(
                    "%s: %d consecutive update failures — check credentials, "
                    "network connectivity, or FusionSolar service status",
                    self.device_name,
                    self._consecutive_failures,
                )
            raise

    async def _get_client_and_retry(self, operation_func):
        client = self.hass.data[DOMAIN][self.entry.entry_id]

        username = self.entry.options.get("username", self.entry.data["username"])
        password = self.entry.options.get("password", self.entry.data["password"])
        subdomain = self.entry.options.get(
            "subdomain", self.entry.data.get("subdomain", "uni001eu5")
        )

        async def ensure_logged_in(client_instance):
            try:
                is_active = await self.hass.async_add_executor_job(
                    client_instance.is_session_active
                )
                if not is_active:
                    await self.hass.async_add_executor_job(client_instance._login)
                    is_active = await self.hass.async_add_executor_job(
                        client_instance.is_session_active
                    )
                    if not is_active:
                        raise Exception("Login completed but session still not active")
                return True
            except (AuthenticationException, CaptchaRequiredException):
                raise
            except Exception as err:
                _LOGGER.warning("Failed to ensure logged in: %s", err)
                return False

        async def create_new_client():
            new_client = await self.hass.async_add_executor_job(
                partial(
                    FusionSolarClient,
                    username,
                    password,
                    captcha_model_path=self.hass,
                    huawei_subdomain=subdomain,
                )
            )
            if await self.hass.async_add_executor_job(new_client.is_session_active):
                self.hass.data[DOMAIN][self.entry.entry_id] = new_client
                return new_client
            return None

        if not await ensure_logged_in(client):
            client = await create_new_client()
            if client is None:
                raise Exception(
                    "Failed to create a new FusionSolar client — "
                    "check credentials and network connectivity"
                )

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = await operation_func(client)
                if response is None:
                    raise Exception("API returned None response")
                return response
            except (AuthenticationException, CaptchaRequiredException) as err:
                _LOGGER.warning(
                    "Non-retryable credential/captcha error: %s", err
                )
                raise
            except requests.exceptions.SSLError as err:
                _LOGGER.warning(
                    "SSL error (possible MITM), not retrying: %s", err
                )
                raise
            except Exception as err:
                _LOGGER.warning(
                    "Attempt %d/%d failed: %s", attempt + 1, max_retries + 1, err
                )
                if attempt < max_retries:
                    recovery_success = False
                    try:
                        await self.hass.async_add_executor_job(client._login)
                        if await self.hass.async_add_executor_job(
                            client.is_session_active
                        ):
                            recovery_success = True
                    except (AuthenticationException, CaptchaRequiredException) as login_err:
                        _LOGGER.warning(
                            "Credential/captcha error during recovery login: %s",
                            login_err,
                        )
                    except Exception as login_err:
                        _LOGGER.warning(
                            "Recovery login failed: %s", login_err
                        )

                    if not recovery_success:
                        try:
                            client = await create_new_client()
                            if client is not None:
                                recovery_success = True
                            else:
                                _LOGGER.warning(
                                    "Recovery client creation returned None"
                                )
                        except Exception as create_err:
                            _LOGGER.warning(
                                "Recovery client creation failed: %s", create_err
                            )

                    if recovery_success:
                        await asyncio.sleep(2)
                    else:
                        await asyncio.sleep(1)
                else:
                    raise Exception(
                        f"Error fetching data after {max_retries + 1} attempts: {err}"
                    )

        raise Exception("Unexpected end of retry loop")

    async def _async_get_data(self) -> Dict[str, Any]:
        """Get data from the device."""
        raise NotImplementedError()

    def create_entities(self, coordinator: DataUpdateCoordinator) -> list:
        """Create entities for the device."""
        raise NotImplementedError()
