from multiprocessing.connection import Client
from xmlrpc.client import Fault
import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import product_pb2
import product_pb2_grpc
import stock_pb2
import stock_pb2_grpc
import store_pb2
import store_pb2_grpc
import base64
from google.protobuf.json_format import MessageToDict
import user_pb2
import user_pb2_grpc
import purchase_order_pb2
import purchase_order_pb2_grpc
from zeep import Client
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

## ----------------------------------------------SOAP-------------------------------------------------##
SOAP_URL = 'http://localhost:8080/ws/purchaseOrderSoapService.wsdl'
soap_client = Client(wsdl=SOAP_URL)

SOAP_ENDPOINT = "http://localhost:8080/ws/filters"

## ----------------------------------------------SOAP-------------------------------------------------##
#################################### FILTERS ENDPOINTS #########################################


def send_soap_request(soap_body):
    headers = {'Content-Type': 'text/xml'}
    response = requests.post(SOAP_ENDPOINT, data=soap_body, headers=headers)
    return response.content


def parse_soap_response(response):
    root = ET.fromstring(response)

    namespace = {"tns": "http://stockearte-backend.com/"}

    result = {}
    if root.find('.//tns:createFiltersModelResponse', namespace) is not None:
        result['id'] = root.find('.//tns:id', namespace).text
    elif root.find('.//tns:updateFiltersModelResponse', namespace) is not None:
        result['success'] = root.find('.//tns:success', namespace).text
    elif root.find('.//tns:deleteFiltersModelResponse', namespace) is not None:
        result['success'] = root.find('.//tns:success', namespace).text

    return result


@app.route('/filters/create', methods=['POST'])
def create_filters_model():
    data = request.json
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://stockearte-backend.com/">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:createFiltersModelRequest>
                <tns:productCode>{data['productCode']}</tns:productCode>
                <tns:filtersName>{data['filtersName']}</tns:filtersName>
                <tns:state>{data.get('state', '')}</tns:state>
                <tns:idTienda>{data.get('idTienda', 0)}</tns:idTienda>
                <tns:desde>{data.get('desde', '')}</tns:desde>
                <tns:hasta>{data.get('hasta', '')}</tns:hasta>
            </tns:createFiltersModelRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    response = send_soap_request(soap_body)
    json_response = parse_soap_response(response)
    return jsonify(json_response), 200


@app.route('/filters/update', methods=['PUT'])
def update_filters_model():
    data = request.json
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://stockearte-backend.com/">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:updateFiltersModelRequest>
                <tns:id>{data['id']}</tns:id>
                <tns:productCode>{data.get('productCode', '')}</tns:productCode>
                <tns:filtersName>{data['filtersName']}</tns:filtersName>
                <tns:state>{data.get('state', '')}</tns:state>
                <tns:idTienda>{data.get('idTienda', 0)}</tns:idTienda>
                <tns:desde>{data.get('desde', '')}</tns:desde>
                <tns:hasta>{data.get('hasta', '')}</tns:hasta>
            </tns:updateFiltersModelRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    response = send_soap_request(soap_body)
    json_response = parse_soap_response(response)
    return jsonify(json_response), 200


@app.route('/filters/delete', methods=['DELETE'])
def delete_filters_model():
    data = request.json
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://stockearte-backend.com/">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:deleteFiltersModelRequest>
                <tns:id>{data['id']}</tns:id>
            </tns:deleteFiltersModelRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """
    response = send_soap_request(soap_body)
    json_response = parse_soap_response(response)
    return jsonify(json_response), 200


## ----------------------------------------------SOAP-------------------------------------------------##
#################################### PURCHASE ORDER ENDPOINTS #########################################
@app.route('/api/purchase-orders/findById', methods=['POST'])
def get_purchase_orders():
    order_id = request.json.get('id')
    codigo_producto = request.json.get('codigoProducto')
    fecha_desde = request.json.get('fechaDesde')
    fecha_hasta = request.json.get('fechaHasta')
    estado = request.json.get('estado')
    tienda = request.json.get('tienda')
    try:
        response = soap_client.service.GetPurchaseOrders(
            id=order_id,
            codigoProducto=codigo_producto,
            fechaDesde=fecha_desde,
            fechaHasta=fecha_hasta,
            estado=estado,
            tienda=tienda
        )
        if isinstance(response, list):
            response_list = []
            for order in response:
                order_dict = {
                    'id': order.id,
                    'estado': order.estado,
                    'observaciones': order.observaciones,
                    'orden_despacho': order.orden_despacho,
                    'fechaSolicitud': str(order.fechaSolicitud),
                    'fechaRecepcion': str(order.fechaRecepcion) if order.fechaRecepcion else None,
                    'idTienda': order.idTienda,
                    'orders': [{'codigo': o.codigo, 'color': o.color, 'talle': o.talle, 'cantidad': o.cantidad} for o in order.orders]
                }
                response_list.append(order_dict)
            return jsonify(response_list), 200
        else:
            return jsonify({'error': 'Invalid response format'}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


## ----------------------------------------------GRPC-------------------------------------------------##
#################################### PURCHASE ORDER ENDPOINTS #########################################

@app.route('/purchase/create', methods=['POST'])
def create_purchase():
    data = request.json
    orders = [
        purchase_order_pb2.OrderDetail(
            codigo=order['codigo'],
            color=order['color'],
            talle=order['talle'],
            cantidad=int(order['cantidad'])
        )
        for order in data.get('orders', [])
    ]
    idTienda = int(data['idTienda'])
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = purchase_order_pb2_grpc.PurchaseOrderServiceStub(channel)
        request_data = purchase_order_pb2.PurchaseOrder(
            orders=orders,
            idTienda=idTienda
        )
        response = stub.CreatePurchaseOrder(request_data)
        return jsonify({'success': response.success})


@app.route('/purchase/edit', methods=['POST'])
def edit_purchase():
    data = request.json  # Espera un cuerpo en formato JSON

    id = data['id']
    estado = data['estado']
    observaciones = data['observaciones']
    orden_despacho = data['orden_despacho']
    idTienda = data['idTienda']

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = purchase_order_pb2_grpc.PurchaseOrderServiceStub(channel)

        # Crea la solicitud
        request_data = purchase_order_pb2.PurchaseOrder(
            id=id,
            estado=estado,
            observaciones=observaciones,
            orden_despacho=orden_despacho,
            idTienda=idTienda
        )

        # Llama al método gRPC
        response = stub.EditPurchaseOrder(request_data)

        # Retorna la respuesta del servidor gRPC
        return jsonify({'success': response.success})


@app.route('/purchase/delete', methods=['DELETE'])
def delete_purchase():
    data = request.json  # Espera un cuerpo en formato JSON

    id = data['id']

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = purchase_order_pb2_grpc.PurchaseOrderServiceStub(channel)

        # Crea la solicitud
        request_data = purchase_order_pb2.DeletePurchaseOrderRequest(
            id=id
        )

        # Llama al método gRPC
        response = stub.DeletePurchaseOrder(request_data)

        # Retorna la respuesta del servidor gRPC
        return jsonify({'success': response.success})


@app.route('/purchase/findById', methods=['POST'])
def findById_purchase():
    data = request.json
    id = data['id']
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = purchase_order_pb2_grpc.PurchaseOrderServiceStub(channel)
        request_data = purchase_order_pb2.GetPurchaseOrderByIdRequest(
            id=id
        )
        response = stub.ListPurchaseOrdersById(request_data)
        purchase_orders_list = []
        for order in response.purchaseOrders:
            purchase_orders_list.append({
                'id': order.id,
                'estado': order.estado,
                'observaciones': order.observaciones,
                'orden_despacho': order.orden_despacho,
                'fechaSolicitud': {
                    'seconds': order.fechaSolicitud.seconds,
                    'nanos': order.fechaSolicitud.nanos
                } if order.HasField('fechaSolicitud') else None,
                'fechaRecepcion': {
                    'seconds': order.fechaRecepcion.seconds,
                    'nanos': order.fechaRecepcion.nanos
                } if order.HasField('fechaRecepcion') else None,
                'idTienda': order.idTienda,
                'orders': [{
                    'codigo': o.codigo,
                    'color': o.color,
                    'talle': o.talle,
                    'cantidad': o.cantidad
                } for o in order.orders]
            })
        return jsonify({'purchaseOrders': purchase_orders_list})

#################################### PRODUCT ENDPOINTS #########################################


@app.route('/product/create', methods=['POST'])
def create_product():
    data = request.json  # Espera un cuerpo en formato JSON
    if not data or 'nombre' not in data or 'talle' not in data or 'foto' not in data or 'color' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren nombre, talle, foto y color.'}), 400

    nombre = data['nombre']
    talle = data['talle']
    foto = data['foto']
    color = data['color']
    stock = data.get('stock', 0)  # Stock opcional
    id_tienda = data.get('idTienda', [])  # idTienda opcional (lista)

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)

        # Crea la solicitud
        request_data = product_pb2.Product(
            nombre=nombre,
            talle=talle,
            foto=foto,
            color=color,
            stock=stock,
            idTienda=id_tienda
        )

        # Llama al método gRPC
        response = stub.CreateProduct(request_data)

        # Retorna la respuesta del servidor gRPC
        return jsonify({'success': response.success})


@app.route('/product/edit', methods=['POST'])
def edit_product():
    data = request.json.get('requestBody')
    if not data or 'id' not in data or 'nombre' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren id y nombre.'}), 400
    request_data = product_pb2.Product(
        id=data['id'],
        nombre=data['nombre'],
        talle=data.get('talle', ''),
        foto=data.get('foto', ''),
        color=data.get('color', ''),
        stock=data.get('stock', 0),
        idTienda=list(map(int, data.get('idTienda', [])))
    )
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        response = stub.EditProduct(request_data)
        return jsonify({'success': response.success})


@app.route('/product/delete', methods=['DELETE'])
def delete_product():
    data = request.json
    if not data or 'id' not in data:
        return jsonify({'error': 'Datos inválidos. Se requiere id.'}), 400

    request_data = product_pb2.DeleteProductRequest(id=data['id'])

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)

        # Llama al método gRPC
        response = stub.DeleteProduct(request_data)

        # Retorna la respuesta del servidor gRPC
        return jsonify({'success': response.success})


@app.route('/product/filter', methods=['POST'])
def filter_product():
    data = request.json
    if not data:
        return jsonify({'error': 'Datos inválidos. Se requieren criterios de filtrado.'}), 400

    # Crear la solicitud de filtrado
    request_data = product_pb2.FilterProductRequest(
        nombre=data.get('nombre', ''),
        codigo_unico=data.get('codigo_unico', ''),
        talle=data.get('talle', ''),
        color=data.get('color', '')
    )
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        response = stub.FilterProduct(request_data)

        products = [{
            'id': product.id,
            'nombre': product.nombre,
            'talle': product.talle,
            'foto': product.foto,
            'color': product.color,
            'stock': product.stock,
            'codigo': product.codigo,
        } for product in response.product]
        return jsonify({'products': products})


@app.route('/product/detail', methods=['POST'])
def get_detail_product():
    data = request.json
    if not data or 'id' not in data:  # or 'tipo_usuario' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren id y tipo_usuario.'}), 400
    print(data)
    product_id = int(data['id'])
    request_data = product_pb2.GetDetailProductRequest(
        id=product_id
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        response = stub.GetDetailProduct(request_data)

        if response.product.id == 0:
            return jsonify({'error': 'Producto no encontrado.'}), 404

        product = response.product
        print(product)
        return jsonify({
            'id': product.id,
            'nombre': product.nombre,
            'talle': product.talle,
            'foto': product.foto,
            'color': product.color,
            'stock': product.stock,  # Only keep one 'stock'
            'codigo': product.codigo,
            # Convert RepeatedScalarContainer to a list
            'idTienda': list(product.idTienda)
        })

######################################## STORE ENDPOINTS ##############################################


@app.route('/store/create', methods=['POST'])
def create_store():
    data = request.json
    if not data or 'code' not in data or 'address' not in data or 'city' not in data or 'province' not in data or 'enabled' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren code, address, city, province y enabled.'}), 400

    request_data = store_pb2.CreateStoreRequest(
        code=data['code'],
        address=data['address'],
        city=data['city'],
        province=data['province'],
        enabled=data['enabled']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = store_pb2_grpc.StoreServiceStub(channel)
        response = stub.CreateStore(request_data)
        return jsonify({'success': response.success})


@app.route('/store/edit', methods=['POST'])
def edit_store():
    data = request.json
    if not data or 'storeId' not in data or 'code' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren storeId y code.'}), 400
    request_data = store_pb2.EditStoreRequest(
        storeId=data['storeId'],
        code=data['code'],
        address=data.get('address', ''),
        city=data.get('city', ''),
        province=data.get('province', ''),
        enabled=bool(int(data.get('enabled', '0'))),
        usersId=list(map(int, data.get('usersId', []))),  # Convert to integer
        # Convert to integer
        productsId=list(map(int, data.get('productsId', [])))
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = store_pb2_grpc.StoreServiceStub(channel)
        response = stub.EditStore(request_data)
        return jsonify({'success': response.success})


@app.route('/store/get_stores', methods=['POST'])
def get_stores():
    data = request.json
    request_data = store_pb2.GetStoresRequest(
        code=data.get('code', ''),
        enabled=data.get('enabled', '')
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = store_pb2_grpc.StoreServiceStub(channel)
        response = stub.GetStores(request_data)

        stores = [MessageToDict(store) for store in response.stores]
        return jsonify({'stores': stores})


@app.route('/store/get_store', methods=['POST'])
def get_store():
    data = request.json
    if not data or 'storeId' not in data:
        return jsonify({'error': 'Datos inválidos. Se requiere storeId.'}), 400

    store_id = int(data['storeId'])
    request_data = store_pb2.GetStoreRequest(
        storeId=store_id
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = store_pb2_grpc.StoreServiceStub(channel)
        response = stub.GetStore(request_data)

        store = MessageToDict(response.store)
        print('Datos de la tienda devueltos desde gRPC:', store)
        return jsonify({'store': store})

######################################## STOCK ENDPOINTS ##############################################


@app.route('/stock/create', methods=['POST'])
def create_stock():
    data = request.json
    if not data or 'storeId' not in data or 'productId' not in data or 'quantity' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren storeId, productId y quantity.'}), 400

    request_data = stock_pb2.CreateStockRequest(
        storeId=data['storeId'],
        productId=data['productId'],
        quantity=data['quantity']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.CreateStock(request_data)
        return jsonify({'success': response.success})


@app.route('/stock/edit', methods=['POST'])
def edit_stock():
    data = request.json
    if not data or 'id' not in data or 'storeId' not in data or 'productId' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren id, storeId y productId.'}), 400

    request_data = stock_pb2.EditStockRequest(
        id=data['id'],
        storeId=data['storeId'],
        productId=data['productId'],
        quantity=data['quantity']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.EditStock(request_data)
        return jsonify({'success': response.success})


@app.route('/stock/get_stocks', methods=['POST'])
def get_stocks():
    request_data = stock_pb2.GetStocksRequest()
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.GetStocks(request_data)
        stocks = []
        for stock in response.stocks:
            stock_dict = MessageToDict(stock)
            if 'quantity' not in stock_dict:
                stock_dict['quantity'] = 0
            stocks.append(stock_dict)
        return jsonify({'stocks': stocks})


@app.route('/stock/get_stock', methods=['POST'])
def get_stock():
    data = request.json
    if not data or 'id' not in data:
        return jsonify({'error': 'Datos inválidos. Se requiere id.'}), 400
    request_data = stock_pb2.GetStockRequest(
        id=int(data['id'])
    )
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.GetStock(request_data)
        stock = MessageToDict(response.stock)
        if 'quantity' not in stock:
            stock['quantity'] = 0
        return jsonify({'stock': stock})

######################################## USER ENDPOINTS ##############################################


@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'firstName' not in data or 'lastName' not in data or 'enabled' not in data or 'storeId' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren username, password, firstName, lastName, enabled y storeId.'}), 400

    request_data = user_pb2.CreateUserRequest(
        username=data['username'],
        password=data['password'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        enabled=data['enabled'],
        storeId=data['storeId']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.CreateUser(request_data)
        return jsonify({'success': response.success})


@app.route('/user/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren username y password.'}), 400
    request_data = user_pb2.AuthenticateUserRequest(
        username=data['username'],
        password=data['password']
    )
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.AuthenticateUser(request_data)
        return jsonify({'success': response.success, 'storeId': response.storeId})


@app.route('/user/asignUserToStore', methods=['POST'])
def asign_user_to_store():
    data = request.json
    if not data or 'userId' not in data or 'storeId' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren userId y storeId.'}), 400

    request_data = user_pb2.AsignUserToStoreRequest(
        userId=data['userId'],
        storeId=data['storeId']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.AsignUserToStore(request_data)
        return jsonify({'success': response.success})


@app.route('/user/edit', methods=['POST'])
def edit_user():
    data = request.json
    if not data or 'userId' not in data or 'username' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren userId y username.'}), 400
    print(data)
    request_data = user_pb2.EditUserRequest(
        userId=int(data['userId']),
        username=data['username'],
        password=data.get('password', ''),
        firstName=data.get('firstName', ''),
        lastName=data.get('lastName', ''),
        enabled=bool(int(data.get('enabled', '0'))),
        storeId=int(data.get('storeId', 0))
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.EditUser(request_data)
        return jsonify({'success': response.success})


@app.route('/user/getUsers', methods=['POST'])
def get_users():
    data = request.json
    request_data = user_pb2.GetUsersRequest(
        username=data.get('username', ''),
        storeCode=data.get('storeCode', '')
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUsers(request_data)

        users = [MessageToDict(user) for user in response.users]
        return jsonify({'users': users})


@app.route('/user/getUser', methods=['POST'])
def get_user():
    data = request.json
    if not data or 'userId' not in data:
        return jsonify({'error': 'Datos inválidos. Se requiere userId.'}), 400

    request_data = user_pb2.GetUserRequest(
        userId=data['userId'],
        username=data.get('username', '')
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUser(request_data)

        user = MessageToDict(response.user)
        return jsonify({'user': user})


if __name__ == '__main__':
    app.run(port=5000)
