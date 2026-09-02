from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROPERTY_TYPE_STRING: _ClassVar[PropertyType]
    PROPERTY_TYPE_BOOL: _ClassVar[PropertyType]
    PROPERTY_TYPE_INT: _ClassVar[PropertyType]
    PROPERTY_TYPE_FLOAT: _ClassVar[PropertyType]
    PROPERTY_TYPE_DURATION: _ClassVar[PropertyType]
    PROPERTY_TYPE_CHOICE: _ClassVar[PropertyType]
PROPERTY_TYPE_STRING: PropertyType
PROPERTY_TYPE_BOOL: PropertyType
PROPERTY_TYPE_INT: PropertyType
PROPERTY_TYPE_FLOAT: PropertyType
PROPERTY_TYPE_DURATION: PropertyType
PROPERTY_TYPE_CHOICE: PropertyType

class TypesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TypesReply(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedCompositeFieldContainer[DeviceType]
    def __init__(self, types: _Optional[_Iterable[_Union[DeviceType, _Mapping]]] = ...) -> None: ...

class DeviceType(_message.Message):
    __slots__ = ("type", "title", "properties")
    CLASS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    type: str
    title: str
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    def __init__(self, type: _Optional[str] = ..., title: _Optional[str] = ..., properties: _Optional[_Iterable[_Union[Property, _Mapping]]] = ..., **kwargs) -> None: ...

class Property(_message.Message):
    __slots__ = ("name", "type", "title", "help", "required", "mask", "advanced", "default_value", "example", "unit", "choice")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    HELP_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    ADVANCED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: PropertyType
    title: str
    help: str
    required: bool
    mask: bool
    advanced: bool
    default_value: str
    example: str
    unit: str
    choice: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[PropertyType, str]] = ..., title: _Optional[str] = ..., help: _Optional[str] = ..., required: _Optional[bool] = ..., mask: _Optional[bool] = ..., advanced: _Optional[bool] = ..., default_value: _Optional[str] = ..., example: _Optional[str] = ..., unit: _Optional[str] = ..., choice: _Optional[_Iterable[str]] = ...) -> None: ...

class NewRequest(_message.Message):
    __slots__ = ("type", "properties")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLASS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    type: str
    properties: _containers.ScalarMap[str, str]
    def __init__(self, type: _Optional[str] = ..., properties: _Optional[_Mapping[str, str]] = ..., **kwargs) -> None: ...

class NewReply(_message.Message):
    __slots__ = ("id", "capabilities")
    ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., capabilities: _Optional[_Iterable[str]] = ...) -> None: ...

class CallRequest(_message.Message):
    __slots__ = ("id", "capability", "method", "args")
    ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    capability: str
    method: str
    args: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, id: _Optional[str] = ..., capability: _Optional[str] = ..., method: _Optional[str] = ..., args: _Optional[_Iterable[bytes]] = ...) -> None: ...

class CallReply(_message.Message):
    __slots__ = ("ret",)
    RET_FIELD_NUMBER: _ClassVar[int]
    ret: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, ret: _Optional[_Iterable[bytes]] = ...) -> None: ...
