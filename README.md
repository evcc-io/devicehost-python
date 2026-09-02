# devicehost-python

An example [evcc](https://github.com/evcc-io/evcc) device host in Python. It
exposes a single meter type whose power value comes from the device
configuration.

A device host is an external process that tells evcc which device types it
provides and which configuration properties each type takes. evcc turns that
description into a template, renders the configuration UI from it and
instantiates devices through the host.

## Run

```bash
uv run python host.py --listen 127.0.0.1:8090
```

Then point evcc at it. The host name namespaces its types, so `py` offering a
`power` type registers the template `py-power`:

```bash
evcc --device-host py=127.0.0.1:8090
```

With `example.evcc.yaml`:

```yaml
meters:
  - name: pv1
    type: template
    template: py-power
    power: -3000
    energy: 1234.5
```

```console
$ evcc --config example.evcc.yaml --device-host py=127.0.0.1:8090 meter
Power:       -3000W     1ms
Energy:      1234.5kWh  1ms
```

Leaving `energy` unset drops the `Energy` line: capabilities are reported per
instance, so the meter only claims `api.MeterEnergy` when it has a reading to
serve.

## What the host implements

Three RPCs from `proto/devicehost.proto`:

| RPC | Returns |
|-----|---------|
| `Types` | the meter type and its `power` / `energy` properties |
| `New` | a device id plus the capabilities this instance supports |
| `Call` | the value for `api.Meter.CurrentPower`, `api.MeterEnergy.TotalEnergy` |

Properties are structured data, not template YAML. `power` is `FLOAT`,
required, with unit `W`; evcc builds the configuration form, the defaults and
the validation from that.

Call arguments and results are json encoded. Their Go types follow from the
capability's interface in evcc's `api/api.go`, so `CurrentPower` returns one
json number. Errors are gRPC errors, not part of the reply.

## Adding a device type

1. Add a `DeviceType` in `types()` with its properties.
2. Add a class with `capabilities()` and `call()`.
3. Dispatch to it in `DeviceHost.New`.

The capability names are the interface names from evcc's `api` package
(`api.Meter`, `api.MeterEnergy`, `api.PhaseCurrents`, `api.Charger`, …).
Capabilities evcc does not know are ignored, so a host may be newer than the
evcc it talks to.

## Regenerating the stubs

`devicehost_pb2*.py` are checked in so the host runs without protoc. After
changing the proto:

```bash
./generate.sh
```

Keep `proto/devicehost.proto` in sync with `devicehost/proto/devicehost.proto`
in the evcc repository.

## Notes

The transport is insecure and unauthenticated, matching the evcc side. Do not
expose the host outside a trusted network.
