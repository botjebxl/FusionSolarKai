import logging
from functools import partial

from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.device_registry import async_get as async_get_device_registry

from .api.fusion_solar_py.client import FusionSolarClient
from .api.fusion_solar_py.exceptions import AuthenticationException, CaptchaRequiredException
from .const import DOMAIN
from .sensor import DeviceHandlerFactory

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "switch", "binary_sensor"]


def _release_shared_client(hass, client_key):
    """Decrement ref_count for a shared client; remove it if no longer used."""
    clients = hass.data.get(DOMAIN, {}).get("_clients", {})
    client_info = clients.get(client_key)
    if client_info:
        client_info["ref_count"] -= 1
        if client_info["ref_count"] <= 0:
            del clients[client_key]


async def async_setup_entry(hass, entry):
    entry.async_on_unload(entry.add_update_listener(update_listener))

    username = entry.options.get("username", entry.data["username"])
    password = entry.options.get("password", entry.data["password"])
    subdomain = entry.options.get("subdomain", entry.data.get("subdomain", "uni001eu5"))

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if "_clients" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["_clients"] = {}

    client_key = (username, subdomain)
    if client_key in hass.data[DOMAIN]["_clients"]:
        client_info = hass.data[DOMAIN]["_clients"][client_key]
        client = client_info["client"]
        client_info["ref_count"] += 1
        _LOGGER.debug(
            "Reusing existing FusionSolar client for %s (ref_count=%d)",
            subdomain,
            client_info["ref_count"],
        )
    else:
        try:
            client = await hass.async_add_executor_job(
                partial(
                    FusionSolarClient,
                    username,
                    password,
                    captcha_model_path=hass,
                    huawei_subdomain=subdomain,
                )
            )
        except (AuthenticationException, CaptchaRequiredException) as err:
            raise ConfigEntryAuthFailed(
                f"Authentication failed: {err}"
            ) from err
        except Exception as err:
            raise ConfigEntryNotReady(
                f"Failed to connect to FusionSolar: {err}"
            ) from err
        hass.data[DOMAIN]["_clients"][client_key] = {"client": client, "ref_count": 1}

    hass.data[DOMAIN][entry.entry_id] = client
    hass.data[DOMAIN][f"{entry.entry_id}_client_key"] = client_key

    device_id = entry.data.get("device_id")
    device_name = entry.data.get("device_name")
    device_type = entry.data.get("device_type")

    device_info = {
        "identifiers": {(DOMAIN, str(device_id))},
        "name": device_name,
        "manufacturer": "FusionSolar",
        "model": device_type or "Unknown",
        "via_device": None,
    }
    hass.data[DOMAIN][f"{entry.entry_id}_device_info"] = device_info

    try:
        sensor_handler = DeviceHandlerFactory.create_handler(hass, entry, device_info)
        coordinator = await sensor_handler.create_coordinator()

        hass.data[DOMAIN][f"{entry.entry_id}_coordinator"] = coordinator
        hass.data[DOMAIN][f"{entry.entry_id}_sensor_handler"] = sensor_handler
    except ConfigEntryAuthFailed:
        hass.data[DOMAIN].pop(f"{entry.entry_id}_device_info", None)
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _release_shared_client(hass, client_key)
        hass.data[DOMAIN].pop(f"{entry.entry_id}_client_key", None)
        raise
    except Exception as e:
        _LOGGER.error("Failed to create coordinator for device %s: %s", device_name, e)
        hass.data[DOMAIN].pop(f"{entry.entry_id}_device_info", None)
        hass.data[DOMAIN].pop(entry.entry_id, None)
        _release_shared_client(hass, client_key)
        hass.data[DOMAIN].pop(f"{entry.entry_id}_client_key", None)
        raise ConfigEntryNotReady(
            f"Failed to set up device {device_name}: {e}"
        ) from e

    device_registry = async_get_device_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, str(entry.data["device_id"]))},
        manufacturer="FusionSolar",
        name=entry.data["device_name"],
        model=entry.data["device_type"],
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def update_listener(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        client_key = hass.data[DOMAIN].get(f"{entry.entry_id}_client_key")
        if client_key and "_clients" in hass.data[DOMAIN]:
            client_info = hass.data[DOMAIN]["_clients"].get(client_key)
            if client_info:
                client_info["ref_count"] -= 1
                if client_info["ref_count"] <= 0:
                    try:
                        await hass.async_add_executor_job(
                            client_info["client"].log_out
                        )
                    except Exception as err:
                        _LOGGER.warning(
                            "Failed to log out FusionSolar client on unload: %s",
                            err,
                        )
                    del hass.data[DOMAIN]["_clients"][client_key]

        hass.data[DOMAIN].pop(f"{entry.entry_id}_client_key", None)
        hass.data[DOMAIN].pop(f"{entry.entry_id}_coordinator", None)
        hass.data[DOMAIN].pop(f"{entry.entry_id}_sensor_handler", None)
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
