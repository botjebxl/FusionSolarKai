import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    device_name = entry.data.get("device_name")
    coordinator = hass.data[DOMAIN].get(f"{entry.entry_id}_coordinator")

    if not coordinator:
        _LOGGER.debug(
            "Coordinator not found for device %s. Skipping binary_sensor setup.",
            device_name,
        )
        return

    device_id = entry.data.get("device_id")
    device_info = hass.data[DOMAIN].get(f"{entry.entry_id}_device_info")

    entities = [
        FusionSolarAlarmSensor(coordinator, device_id, device_name, device_info)
    ]
    _LOGGER.info(
        "Adding %d binary_sensor entities for device %s", len(entities), device_name
    )
    async_add_entities(entities)


class FusionSolarAlarmSensor(CoordinatorEntity, BinarySensorEntity):

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, device_id, device_name, device_info):
        super().__init__(coordinator)
        self._attr_unique_id = f"{device_id}_alarm"
        self._attr_name = f"{device_name} Alarm"
        self._attr_device_info = device_info

    def _get_alarm_list(self):
        if not self.coordinator.data:
            return []
        alarm_data = self.coordinator.data.get("alarms", {})
        if isinstance(alarm_data, dict):
            return alarm_data.get("data", {}).get("list", []) or []
        if isinstance(alarm_data, list):
            return alarm_data
        return []

    @property
    def is_on(self):
        return len(self._get_alarm_list()) > 0

    @property
    def extra_state_attributes(self):
        alarms = self._get_alarm_list()
        return {"alarm_count": len(alarms), "alarms": alarms}
