# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import stock_pb2 as stock__pb2

GRPC_GENERATED_VERSION = '1.66.2'
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
        + f' but the generated code in stock_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class StockServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateStock = channel.unary_unary(
                '/com.unla.stockearte.StockService/CreateStock',
                request_serializer=stock__pb2.CreateStockRequest.SerializeToString,
                response_deserializer=stock__pb2.StockResponse.FromString,
                _registered_method=True)
        self.EditStock = channel.unary_unary(
                '/com.unla.stockearte.StockService/EditStock',
                request_serializer=stock__pb2.EditStockRequest.SerializeToString,
                response_deserializer=stock__pb2.StockResponse.FromString,
                _registered_method=True)
        self.GetStocks = channel.unary_unary(
                '/com.unla.stockearte.StockService/GetStocks',
                request_serializer=stock__pb2.GetStocksRequest.SerializeToString,
                response_deserializer=stock__pb2.GetStocksResponse.FromString,
                _registered_method=True)
        self.GetStock = channel.unary_unary(
                '/com.unla.stockearte.StockService/GetStock',
                request_serializer=stock__pb2.GetStockRequest.SerializeToString,
                response_deserializer=stock__pb2.GetStockResponse.FromString,
                _registered_method=True)


class StockServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EditStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStocks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StockServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateStock': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateStock,
                    request_deserializer=stock__pb2.CreateStockRequest.FromString,
                    response_serializer=stock__pb2.StockResponse.SerializeToString,
            ),
            'EditStock': grpc.unary_unary_rpc_method_handler(
                    servicer.EditStock,
                    request_deserializer=stock__pb2.EditStockRequest.FromString,
                    response_serializer=stock__pb2.StockResponse.SerializeToString,
            ),
            'GetStocks': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStocks,
                    request_deserializer=stock__pb2.GetStocksRequest.FromString,
                    response_serializer=stock__pb2.GetStocksResponse.SerializeToString,
            ),
            'GetStock': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStock,
                    request_deserializer=stock__pb2.GetStockRequest.FromString,
                    response_serializer=stock__pb2.GetStockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.unla.stockearte.StockService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('com.unla.stockearte.StockService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class StockService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateStock(request,
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
            '/com.unla.stockearte.StockService/CreateStock',
            stock__pb2.CreateStockRequest.SerializeToString,
            stock__pb2.StockResponse.FromString,
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
    def EditStock(request,
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
            '/com.unla.stockearte.StockService/EditStock',
            stock__pb2.EditStockRequest.SerializeToString,
            stock__pb2.StockResponse.FromString,
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
    def GetStocks(request,
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
            '/com.unla.stockearte.StockService/GetStocks',
            stock__pb2.GetStocksRequest.SerializeToString,
            stock__pb2.GetStocksResponse.FromString,
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
    def GetStock(request,
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
            '/com.unla.stockearte.StockService/GetStock',
            stock__pb2.GetStockRequest.SerializeToString,
            stock__pb2.GetStockResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
