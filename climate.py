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
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

import requests

def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
        ) -> None:
    aircons = [LGAircon()]
    add_entities(aircons)

# async def async_setup_entry(hass, entry, async_add_entities):
#     """Config entry"""
#     await coordinator.async_config_entry_first_refresh()

#     async_add_entities()

class LGAirconCoordinator(DataUpdateCoordinator):
    """LG Aircon Coordinator"""

    def __init__(self, hass, api):
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API endpont"""

        try:
            api_url = "http://10.0.0.237:8000/state"
            async with async_timeout.timeout(10):
             return await requests.get(api_url).json
        except:
            raise UpdateFailed("Failed to communicate with API")

class LGAircon(LGAirconCoordinator, ClimateEntity):
    _attr_has_entity_name = True

    def __init__(self, coord, idx):
        super().__init__(coordinator)
        self.idx = idx

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

    @callback
    def _handle_coordinator_update(self) -> None: 
        self._current_temp = self.coordinator.data[self.idx]["cur_temp"]
        self.async_write_ha_state()