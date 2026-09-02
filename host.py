"""Example evcc device host exposing a meter with a configurable power value."""

import argparse
import json
import logging
from concurrent import futures
from itertools import count

import grpc

import devicehost_pb2 as pb
import devicehost_pb2_grpc as pb_grpc

log = logging.getLogger("devicehost")


def types():
    """The device types this host provides, with their configuration properties."""
    return [
        pb.DeviceType(
            device_class="meter",
            type="power",
            title="Example Power Meter",
            properties=[
                pb.Property(
                    name="power",
                    title="Power",
                    help="Power value reported by this meter. Negative means production.",
                    type=pb.PROPERTY_TYPE_FLOAT,
                    unit="W",
                    example="-3000",
                    required=True,
                ),
                pb.Property(
                    name="energy",
                    title="Total energy",
                    help="Optional meter reading. Adds the api.MeterEnergy capability.",
                    type=pb.PROPERTY_TYPE_FLOAT,
                    unit="kWh",
                    advanced=True,
                ),
            ],
        ),
    ]


class Meter:
    """A meter returning the power value it was configured with."""

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


class DeviceHost(pb_grpc.DeviceHostServicer):
    def __init__(self):
        self.devices = {}
        self.ids = count()

    def Types(self, request, context):
        return pb.TypesReply(types=types())

    def New(self, request, context):
        if request.type != "power":
            context.abort(grpc.StatusCode.NOT_FOUND, f"unknown type: {request.type}")

        try:
            device = Meter(request.properties)
        except (KeyError, ValueError) as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"{request.type}: {e}")

        id = f"{request.type}-{next(self.ids)}"
        self.devices[id] = device
        log.info("new %s: %s %s", id, request.type, dict(request.properties))

        return pb.NewReply(id=id, capabilities=device.capabilities())

    def Call(self, request, context):
        device = self.devices.get(request.id)
        if device is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"unknown device: {request.id}")

        args = [json.loads(a) for a in request.args]

        try:
            ret = device.call(request.capability, request.method, args)
        except KeyError as e:
            context.abort(grpc.StatusCode.UNIMPLEMENTED, f"unknown method: {e}")

        return pb.CallReply(ret=[json.dumps(v).encode() for v in ret])


def serve(address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb_grpc.add_DeviceHostServicer_to_server(DeviceHost(), server)
    server.add_insecure_port(address)
    server.start()

    log.info("listening on %s", address)
    server.wait_for_termination()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listen", default="127.0.0.1:8090", help="listen address")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    try:
        serve(args.listen)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
