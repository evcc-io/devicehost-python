"""Behaviour lock for the meter device type. Run with `uv run python test_meter.py`."""

import meter


def test_capabilities_follow_the_configuration():
    assert meter.Meter({"power": "-3000"}).capabilities() == ["api.Meter"]
    assert meter.Meter({"power": "-3000", "energy": "1234.5"}).capabilities() == [
        "api.Meter",
        "api.MeterEnergy",
    ]
    # evcc renders an unset optional property as an empty value
    assert meter.Meter({"power": "-3000", "energy": ""}).capabilities() == ["api.Meter"]


def test_call_returns_the_configured_values():
    m = meter.Meter({"power": "-3000", "energy": "1234.5"})
    assert m.call("api.Meter", "CurrentPower", []) == [-3000.0]
    assert m.call("api.MeterEnergy", "TotalEnergy", []) == [1234.5]


def test_unknown_method_raises():
    m = meter.Meter({"power": "0"})
    try:
        m.call("api.Meter", "Nope", [])
    except KeyError:
        return
    raise AssertionError("expected KeyError")


def test_missing_required_property_raises():
    try:
        meter.Meter({})
    except KeyError:
        return
    raise AssertionError("expected KeyError")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
