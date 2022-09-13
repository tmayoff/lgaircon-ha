from homeassistant import config_entries

DOMAIN = "lgaircon"

class LGAirconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    # async def async_step_dhcp(self, info):
    #     await self.async_set_unique_id(device_unique_id)
    #     self._abort_if_unique_id_configured()
    return self.async_show_form(
        step_id="dhcp"
    )