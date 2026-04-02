# Alarm Binary Sensors + Configurable Polling Interval

## Feature 1: Alarm Binary Sensors

### What
One binary sensor per device config entry that indicates whether the device has active alarms/faults.

### Architecture

**New files:**
- `custom_components/fusionsolarkai/binary_sensor.py` — platform setup + `FusionSolarAlarmSensor` entity class

**Modified files:**
- `custom_components/fusionsolarkai/__init__.py` — add `"binary_sensor"` to platform forwards
- `custom_components/fusionsolarkai/device_handler.py` — add `get_alarm_data()` call in `_get_client_and_retry` wrapper, store under `"alarms"` key in coordinator data. Each device handler's `_async_get_data()` is modified to include alarm data.

### Entity Design

- **Entity class**: `FusionSolarAlarmSensor(CoordinatorEntity, BinarySensorEntity)`
- **device_class**: `BinarySensorDeviceClass.PROBLEM`
- **is_on**: `True` when `alarm_count > 0`
- **Attributes**:
  - `alarm_count` (int)
  - `alarms` (list of dicts, each with available fields from the API response)
- **unique_id**: `{device_id}_alarm`
- **name**: `{device_name} Alarm`
- **entity_category**: `EntityCategory.DIAGNOSTIC`

### Data Flow

1. Each device handler's `_async_get_data()` adds a `get_alarm_data(self.device_id)` call
2. Result stored as `coordinator.data["alarms"]`
3. `binary_sensor.py` platform setup retrieves coordinator + device info, creates one `FusionSolarAlarmSensor`
4. Entity reads from `coordinator.data["alarms"]`

### Error Handling

- If `get_alarm_data()` fails, store empty dict — alarm sensor shows as "clear" rather than failing the entire coordinator update
- Log at WARNING level on alarm fetch failure

## Feature 2: Configurable Polling Interval

### What
Let users set the polling interval via the integration's options flow instead of the hardcoded 15 seconds.

### Architecture

**Modified files:**
- `custom_components/fusionsolarkai/const.py` — add `CONF_POLLING_INTERVAL`, `DEFAULT_POLLING_INTERVAL = 60`, `MIN_POLLING_INTERVAL = 15`, `MAX_POLLING_INTERVAL = 300`
- `custom_components/fusionsolarkai/config_flow.py` — add polling interval field to `OptionsFlowHandler`
- `custom_components/fusionsolarkai/device_handler.py` — read polling interval from `entry.options.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)` instead of hardcoded 15
- `custom_components/fusionsolarkai/translations/en.json` — add label for polling interval option

### Options Flow

- Added to the existing `OptionsFlowHandler.async_step_init()`
- Field: integer input, default 60, range 15-300
- Label: "Polling interval (seconds)"

### Reload Behavior

- When options change, HA reloads the config entry, which recreates the coordinator with the new interval — no special handling needed.
