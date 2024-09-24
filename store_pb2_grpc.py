# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import store_pb2 as store__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in store_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class StoreServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateStore = channel.unary_unary(
                '/com.unla.stockearte.StoreService/CreateStore',
                request_serializer=store__pb2.CreateStoreRequest.SerializeToString,
                response_deserializer=store__pb2.StoreResponse.FromString,
                _registered_method=True)
        self.EditStore = channel.unary_unary(
                '/com.unla.stockearte.StoreService/EditStore',
                request_serializer=store__pb2.EditStoreRequest.SerializeToString,
                response_deserializer=store__pb2.StoreResponse.FromString,
                _registered_method=True)
        self.GetStores = channel.unary_unary(
                '/com.unla.stockearte.StoreService/GetStores',
                request_serializer=store__pb2.GetStoresRequest.SerializeToString,
                response_deserializer=store__pb2.GetStoresResponse.FromString,
                _registered_method=True)
        self.GetStore = channel.unary_unary(
                '/com.unla.stockearte.StoreService/GetStore',
                request_serializer=store__pb2.GetStoreRequest.SerializeToString,
                response_deserializer=store__pb2.GetStoreResponse.FromString,
                _registered_method=True)


class StoreServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EditStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStores(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StoreServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateStore': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateStore,
                    request_deserializer=store__pb2.CreateStoreRequest.FromString,
                    response_serializer=store__pb2.StoreResponse.SerializeToString,
            ),
            'EditStore': grpc.unary_unary_rpc_method_handler(
                    servicer.EditStore,
                    request_deserializer=store__pb2.EditStoreRequest.FromString,
                    response_serializer=store__pb2.StoreResponse.SerializeToString,
            ),
            'GetStores': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStores,
                    request_deserializer=store__pb2.GetStoresRequest.FromString,
                    response_serializer=store__pb2.GetStoresResponse.SerializeToString,
            ),
            'GetStore': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStore,
                    request_deserializer=store__pb2.GetStoreRequest.FromString,
                    response_serializer=store__pb2.GetStoreResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.unla.stockearte.StoreService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('com.unla.stockearte.StoreService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class StoreService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.unla.stockearte.StoreService/CreateStore',
            store__pb2.CreateStoreRequest.SerializeToString,
            store__pb2.StoreResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EditStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.unla.stockearte.StoreService/EditStore',
            store__pb2.EditStoreRequest.SerializeToString,
            store__pb2.StoreResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetStores(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.unla.stockearte.StoreService/GetStores',
            store__pb2.GetStoresRequest.SerializeToString,
            store__pb2.GetStoresResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/com.unla.stockearte.StoreService/GetStore',
            store__pb2.GetStoreRequest.SerializeToString,
            store__pb2.GetStoreResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
