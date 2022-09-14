from __future__ import annotations

from datetime import timedelta
import async_timeout
import logging
import requests

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    TEMP_CELSIUS
)

from homeassistant.components.climate.const import (
        HVACMode,
        FAN_ON, FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH,
        SWING_OFF
)
from homeassistant.core import (HomeAssistant, callback)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=10)

async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        async_add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
        ) -> None:

    aircons = [LGAircon(hass)]
    async_add_entities(aircons)

class LGAircon(ClimateEntity):
    _attr_has_entity_name = True

    def __init__(self, hass):
        self._hass = hass

        self._attr_name = "LG Aircon"
        self._attr_min_temp = 18
        self._attr_max_temp = 30

        self._current_temp = None
        self._current_humidity = None

        self._current_fan_mode = FAN_LOW
        self._current_operation = HVACMode.OFF
        self._current_swing_mode = SWING_OFF
        self._target_temp = 20
        self._attr_target_temperature_high = None
        self._attr_target_temperature_low = None
        self._attr_target_temperature_step = 1

        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_hvac_mode = HVACMode.OFF

        self._attr_fan_modes = [FAN_ON, FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
        self._attr_fan_mode = FAN_OFF
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL, HVACMode.DRY, HVACMode.FAN_ONLY]

        self._attr_supported_features = 0
        self._attr_supported_features |= ClimateEntityFeature.FAN_MODE
        self._attr_supported_features |= ClimateEntityFeature.TARGET_TEMPERATURE

    def fetch_state(self):
        api_url = "http://10.0.0.84:8000/state"
        res = requests.get(api_url)
        state = res.json()
        _LOGGER.info(state)
        self._target_temp = state["target_temp"]

        mode = state["mode"]
        if mode == "Off":
            self._current_operation = HVACMode.OFF
        elif mode == "Cool":
            self._current_operation = HVACMode.COOL
        elif mode == "Heat":
            self._current_operation = HVACMode.HEAT
        elif mode == "Dehum":
            self._current_operation = HVACMode.DRY
        elif mode == "Fan":
            self._current_operation = HVACMode.FAN_ONLY

    def fetch_temperature(self):
        api_url = "http://10.0.0.84:8000/current_temp"
        res = requests.get(api_url)
        temp = res.json()
        self._current_temp = temp

    async def send_update_state(self):
        api_url = "http://10.0.0.84:8000/state"
        state = {
            'mode': self._current_operation,
            'target_temp': self._target_temp
            }
        res = requests.post(api_url, json=state)

    async def async_update(self):
        await self._hass.async_add_executor_job(self.fetch_state)
        await self._hass.async_add_executor_job(self.fetch_temperature)

    @property
    def current_temperature(self):
        return self._current_temp

    @property
    def target_temperature_step(self):
        return 1

    @property
    def target_temperature(self):
        return self._target_temp

    @property
    def hvac_mode(self):
        return self._current_operation

    async def async_set_hvac_mode(self, hvac_mode):
        self._current_operation = hvac_mode
        await self.send_update_state()

    async def async_set_fan_mode(self, fan_mode):
        self._current_fan_mode = fan_mode
        await self._hass.async_add_executor_job(self.send_update_state)

    async def async_set_temperature(self, **kwargs):
        print(kwargs)
        _LOGGER.info(kwargs)
        await self._hass.async_add_executor_job(self.send_update_state)