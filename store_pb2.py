# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: store.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'store.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstore.proto\x12\x13\x63om.unla.stockearte\"d\n\x12\x43reateStoreRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x0c\n\x04\x63ity\x18\x03 \x01(\t\x12\x10\n\x08province\x18\x04 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x05 \x01(\x08\"\x98\x01\n\x10\x45\x64itStoreRequest\x12\x0f\n\x07storeId\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\x12\x0c\n\x04\x63ity\x18\x04 \x01(\t\x12\x10\n\x08province\x18\x05 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x06 \x01(\t\x12\x0f\n\x07usersId\x18\x07 \x03(\x05\x12\x12\n\nproductsId\x18\x08 \x03(\x05\"1\n\x10GetStoresRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\t\"o\n\x0cStoreSummary\x12\x0f\n\x07storeId\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\x12\x0c\n\x04\x63ity\x18\x04 \x01(\t\x12\x10\n\x08province\x18\x05 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x06 \x01(\x08\"F\n\x11GetStoresResponse\x12\x31\n\x06stores\x18\x01 \x03(\x0b\x32!.com.unla.stockearte.StoreSummary\" \n\rStoreResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\"\n\x0fGetStoreRequest\x12\x0f\n\x07storeId\x18\x01 \x01(\x05\"D\n\x10GetStoreResponse\x12\x30\n\x05store\x18\x01 \x01(\x0b\x32!.com.unla.stockearte.StoreSummary2\xf7\x02\n\x0cStoreService\x12Z\n\x0b\x43reateStore\x12\'.com.unla.stockearte.CreateStoreRequest\x1a\".com.unla.stockearte.StoreResponse\x12V\n\tEditStore\x12%.com.unla.stockearte.EditStoreRequest\x1a\".com.unla.stockearte.StoreResponse\x12Z\n\tGetStores\x12%.com.unla.stockearte.GetStoresRequest\x1a&.com.unla.stockearte.GetStoresResponse\x12W\n\x08GetStore\x12$.com.unla.stockearte.GetStoreRequest\x1a%.com.unla.stockearte.GetStoreResponseB*\n\x13\x63om.unla.stockearteB\x11StoreServiceProtoP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'store_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\023com.unla.stockearteB\021StoreServiceProtoP\001'
  _globals['_CREATESTOREREQUEST']._serialized_start=36
  _globals['_CREATESTOREREQUEST']._serialized_end=136
  _globals['_EDITSTOREREQUEST']._serialized_start=139
  _globals['_EDITSTOREREQUEST']._serialized_end=291
  _globals['_GETSTORESREQUEST']._serialized_start=293
  _globals['_GETSTORESREQUEST']._serialized_end=342
  _globals['_STORESUMMARY']._serialized_start=344
  _globals['_STORESUMMARY']._serialized_end=455
  _globals['_GETSTORESRESPONSE']._serialized_start=457
  _globals['_GETSTORESRESPONSE']._serialized_end=527
  _globals['_STORERESPONSE']._serialized_start=529
  _globals['_STORERESPONSE']._serialized_end=561
  _globals['_GETSTOREREQUEST']._serialized_start=563
  _globals['_GETSTOREREQUEST']._serialized_end=597
  _globals['_GETSTORERESPONSE']._serialized_start=599
  _globals['_GETSTORERESPONSE']._serialized_end=667
  _globals['_STORESERVICE']._serialized_start=670
  _globals['_STORESERVICE']._serialized_end=1045
# @@protoc_insertion_point(module_scope)
