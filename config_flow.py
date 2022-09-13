from homeassistant import config_entries

DOMAIN = "lgaircon"

class LGAirconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_dhcp(self, info):
        if info is not None:
            pass