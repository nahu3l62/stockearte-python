import grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
import product_pb2
import product_pb2_grpc
import store_pb2
import store_pb2_grpc
import base64
from google.protobuf.json_format import MessageToDict
import user_pb2
import user_pb2_grpc

app = Flask(__name__)
CORS(app)


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
    data = request.json
    if not data or 'id' not in data or 'nombre' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren id y nombre.'}), 400

    # Crea la solicitud
    request_data = product_pb2.Product(
        id=data['id'],
        nombre=data['nombre'],
        talle=data.get('talle', ''),
        foto=data.get('foto', ''),
        color=data.get('color', ''),
        stock=data.get('stock', 0),
        idTienda=data.get('idTienda', [])
    )

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)

        # Llama al método gRPC
        response = stub.EditProduct(request_data)

        # Retorna la respuesta del servidor gRPC
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
        color=data.get('color', ''),
        habilitado=data.get('habilitado','')
    )

    # Establece la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)

        # Llama al método gRPC
        response = stub.FilterProduct(request_data)

        # Retorna la respuesta del servidor gRPC
        products = [{
            'id': product.id,
            'nombre': product.nombre,
            'talle': product.talle,
            'foto': product.foto,
            'color': product.color,
            'stock': product.stock
        } for product in response.product]

        return jsonify({'products': products})


@app.route('/product/detail', methods=['POST'])
def get_detail_product():
    data = request.json
    if not data or 'id' not in data or 'tipo_usuario' not in data:
        return jsonify({'error': 'Datos inválidos. Se requieren id y tipo_usuario.'}), 400

    request_data = product_pb2.GetDetailProductRequest(
        id=data['id'],
        tipo_usuario=data['tipo_usuario'],
        stock=data.get('stock', 0),
        nombre=data.get('nombre', ''),
        talle=data.get('talle', ''),
        foto=data.get('foto', ''),
        color=data.get('color', '')
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        response = stub.GetDetailProduct(request_data)

        if response.product.id == 0:
            return jsonify({'error': 'Producto no encontrado.'}), 404

        product = response.product
        return jsonify({
            'id': product.id,
            'nombre': product.nombre,
            'talle': product.talle,
            'foto': product.foto,
            'color': product.color,
            'stock': product.stock
        })


####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


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
        enabled=data.get('enabled', ''),
        usersId=data.get('usersId', []),
        productsId=data.get('productsId', [])
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

    request_data = store_pb2.GetStoreRequest(
        storeId=data['storeId']
    )

    with grpc.insecure_channel('localhost:6565') as channel:
        stub = store_pb2_grpc.StoreServiceStub(channel)
        response = stub.GetStore(request_data)

        store = MessageToDict(response.store)
        return jsonify({'store': store})

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


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
        return jsonify({'success': response.success})


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

    request_data = user_pb2.EditUserRequest(
        userId=data['userId'],
        username=data['username'],
        password=data.get('password', ''),
        firstName=data.get('firstName', ''),
        lastName=data.get('lastName', ''),
        enabled=data.get('enabled', ''),
        storeId=data.get('storeId', 0)
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
