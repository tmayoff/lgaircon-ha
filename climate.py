from __future__ import annotations

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
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import requests

def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
        ) -> None:
    aircons = [LGAircon()]
    add_entities(aircons)

class LGAirconCoordinator(DataUpdateCoordinator):
    """LG Aircon Coordinator"""

    def __init__(self, hass, api):
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API endpont"""

        try:
            

class LGAircon(ClimateEntity):
    _attr_has_entity_name = True

    def __init__(self):
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

        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_hvac_mode = HVACMode.OFF

        self._attr_fan_modes = [FAN_ON, FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
        self._attr_fan_mode = FAN_OFF
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL, HVACMode.FAN_ONLY]

        self._attr_supported_features = 0
        self._attr_supported_features |= ClimateEntityFeature.FAN_MODE

    def async_update(self): 
        api_url = "http://10.0.0.237:8000/state"
        res = requests.get(api_url)
        state = res.json()
        self._current_temp = state["cur_temp"]