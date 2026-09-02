"""A meter type whose power value comes from the device configuration."""

from pb import devicehost_pb2 as pb2

TYPE = pb2.DeviceType(
    device_class="meter",
    type="power",
    title="Example Power Meter",
    properties=[
        pb2.Property(
            name="power",
            title="Power",
            help="Power value reported by this meter. Negative means production.",
            type=pb2.PROPERTY_TYPE_FLOAT,
            unit="W",
            example="-3000",
            required=True,
        ),
        pb2.Property(
            name="energy",
            title="Total energy",
            help="Optional meter reading. Adds the api.MeterEnergy capability.",
            type=pb2.PROPERTY_TYPE_FLOAT,
            unit="kWh",
            advanced=True,
        ),
    ],
)


class Meter:
    def __init__(self, properties):
        self.power = float(properties["power"])
        self.energy = float(properties["energy"]) if properties.get("energy") else None

    def capabilities(self):
        caps = ["api.Meter"]
        if self.energy is not None:
            caps.append("api.MeterEnergy")
        return caps

    def call(self, capability, method, args):
        match capability, method:
            case "api.Meter", "CurrentPower":
                return [self.power]
            case "api.MeterEnergy", "TotalEnergy":
                return [self.energy]
        raise KeyError(f"{capability}.{method}")
