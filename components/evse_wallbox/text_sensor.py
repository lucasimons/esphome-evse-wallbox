import esphome.codegen as cg
from esphome.components import text_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ICON, CONF_ID

from . import CONF_EVSE_WALLBOX_ID, EVSE_WALLBOX_COMPONENT_SCHEMA

DEPENDENCIES = ["evse_wallbox"]

CODEOWNERS = ["@syssi"]

CONF_PROTECTION_STATUS = "protection_status"

ICON_PROTECTION_STATUS = "mdi:heart-pulse"

TEXT_SENSORS = [
    CONF_PROTECTION_STATUS,
]

CONFIG_SCHEMA = EVSE_WALLBOX_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(CONF_PROTECTION_STATUS): text_sensor.TEXT_SENSOR_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(text_sensor.TextSensor),
                cv.Optional(CONF_ICON, default=ICON_PROTECTION_STATUS): cv.icon,
            }
        ),
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_EVSE_WALLBOX_ID])
    for key in TEXT_SENSORS:
        if key in config:
            conf = config[key]
            sens = cg.new_Pvariable(conf[CONF_ID])
            await text_sensor.register_text_sensor(sens, conf)
            cg.add(getattr(hub, f"set_{key}_text_sensor")(sens))
