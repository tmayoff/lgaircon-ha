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

async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        async_add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
        ) -> None:

    # coordinator = LGAirconCoordinator(hass)

    aircons = [LGAircon()]
    async_add_entities(aircons)

class LGAirconCoordinator(DataUpdateCoordinator):
    """LG Aircon Coordinator"""

    def __init__(self, hass):
        super().__init__(
            hass, 
            _LOGGER,
            name="LG Aircon",
            update_interval=timedelta(seconds=10))
        self._hass = hass

    def update(self):
        api_url = "http://10.0.0.237:8000/state"
        return requests.get(api_url).json

    async def _async_update_data(self):
        """Fetch data from API endpont"""
        try:
            async with async_timeout.timeout(10):
                return await self._hass.async_add_executor_job(self.update)
        except Exception as err:
            raise UpdateFailed(f"Failed to communicate with API {err}")

class LGAircon(ClimateEntity):
    _attr_has_entity_name = True

    def __init__(self):
        # super().__init__(coordinator)

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

    def fetch(self):
        api_url = "http://10.0.0.237:8000/state"
        return requests.get(api_url).json
    
    def async_update(self):        
        res = await self._hass.async_add_executor_job(self.fetch)
        self._current_temp = res["cur_temp"]

    # @callback
    # def _handle_coordinator_update(self) -> None:
    #     if self.coordinator.data:
    #         self._current_temp = self.coordinator.data["cur_temp"]
    #         self.async_write_ha_state()