"""Example evcc device host.

Add a device type by writing a module with a TYPE descriptor and a device
class, then registering it in DEVICES.
"""

import argparse
import json
import logging
from concurrent import futures
from itertools import count

import grpc

import meter
from pb import devicehost_pb2 as pb2
from pb import devicehost_pb2_grpc as pb2_grpc

log = logging.getLogger("devicehost")

DEVICES = {
    meter.TYPE.type: (meter.TYPE, meter.Meter),
}


class DeviceHost(pb2_grpc.DeviceHostServicer):
    def __init__(self):
        self.devices = {}
        self.ids = count()

    def Types(self, request, context):
        return pb2.TypesReply(types=[type for type, _ in DEVICES.values()])

    def New(self, request, context):
        entry = DEVICES.get(request.type)
        if entry is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"unknown type: {request.type}")

        try:
            device = entry[1](request.properties)
        except (KeyError, ValueError) as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"{request.type}: {e}")

        id = f"{request.type}-{next(self.ids)}"
        self.devices[id] = device
        log.info("new %s: %s %s", id, request.type, dict(request.properties))

        return pb2.NewReply(id=id, capabilities=device.capabilities())

    def Call(self, request, context):
        device = self.devices.get(request.id)
        if device is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"unknown device: {request.id}")

        args = [json.loads(a) for a in request.args]

        try:
            ret = device.call(request.capability, request.method, args)
        except KeyError as e:
            context.abort(grpc.StatusCode.UNIMPLEMENTED, f"unknown method: {e}")

        return pb2.CallReply(ret=[json.dumps(v).encode() for v in ret])


def serve(address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb2_grpc.add_DeviceHostServicer_to_server(DeviceHost(), server)
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
