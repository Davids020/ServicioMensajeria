from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import random
from datetime import datetime


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='SERVICIO DE MENSAJERIA',
    description='API rest para servicio de mensajeria',
)

cs = api.namespace('customers', description='INFORMACION DE USUARIOS')
ts = api.namespace('trajectorys', description='INFORMACION DE TRAYECTORIAS')
ps = api.namespace('packages', description='OPERACIONES DE PAQUETES')
bs = api.namespace('bills', description='OPERACIONES DE FACTURAS')

customers = api.model('Customers', {    
    'id': fields.Integer(required=True, description='identificador del cliente'),
    'name': fields.String(required=True, description='nombre del cliente'),
    'lastname': fields.String(required=True, description='Apellido del cliente'),
    'postalC': fields.Integer(required=True, description='Codigo postal del cliente'),
    'address': fields.String(required=True, description='address del cliente'),

})

trajectorys = api.model('Trajectorys', {    
    'id': fields.Integer(required=True, description='Identificador unico de trayectoria'),
    'origin': fields.String(required=True, description='Origen'),
    'destiny': fields.String(required=True, description='Destino'),
    'cost': fields.Float(required=True, description='Costo de envio'),
})

packages = api.model('Packages', {    
    'id': fields.Integer(required=True, description='Identificador unico de trayectoria'),
    'name': fields.String(required=True, description='Nombre del paquete'),
    'price': fields.Float(required=True, description='Precio del paquete'),
})

bills = api.model('Bills' ,{    
    'id': fields.Integer(readonly=True,required=True, description='Identificador unico de trayectoria'),
    'total': fields.Float(required=True, description='Total de la factura'),
    'customer': fields.Nested(customers),
    'package': fields.Nested(packages),
    'trajectory':fields.Nested(trajectorys),
    'date': fields.Date(required=True, description='Precio del paquete',dt_format='rfc822'),

})
# bills  = api.schema_model('Bills', {
#     'required': ['date','customer','package','trajectory'],
#     'properties': {
#         'id': {
#             'type': 'integer'
#         },
#         'total': {
#             'type': 'number',
#             'format': 'float'
            
#         },
#         'date': {
#             'type': 'string',
#             'format': 'date-time'
#         },
#         'customer': {
#             '$ref': '#/definitions/Customers',
#         },
#         'package': {
#         '$ref': '#/definitions/Packages',
#         },
#         'trajectory': {
#         '$ref': '#/definitions/Trajectorys',
#         }
#     },
#     'type': 'object'
# })

#CustomerService
class customerDAO(object):
    def __init__(self):
        self.counter = 0
        self.customers = [
    {
        'id':1,
        'name': 'David',
        'address':'Cartagena' ,
        'lastname': 'Sotelo',
        'postalC': 123456,
        
        
    }
] 

    def get(self, id):
        for customer in self.customers:
            if customer['id'] == id:
                return customer
        api.abort(404, "Customer {} doesn't exist".format(id))

    def create(self, data):
        customer = data
    
        new_customer = {
            'id': random.randint(0,100),
            'name': customer['name'],
            'lastname': customer['lastname'],
            'address': customer['address'],
            'postalC': customer['postalC'],
            
            
            }
        self.customers.append(new_customer)
        return customer

    def delete(self, id):
        customer = self.get(id)
        self.customers.remove(customer)   

    def update(self, id, data):
        customer = self.get(id)
        customer.update(data)
        return customer

DAOCST = customerDAO()

@cs.route('/')
class CustomersService(Resource):
    '''Shows a list of all customers'''
    @cs.doc('list customers info')
    @cs.marshal_list_with(customers)
    def get(self):
        '''Lista de informacion de clientes'''
        return DAOCST.customers

    @cs.doc('create_customer')
    @cs.expect(customers)
    @cs.marshal_with(customers, code=201)
    def post(self):
        '''Crear informacion de clientes'''
        return DAOCST.create(api.payload), 201

@cs.route('/<int:id>')
@cs.response(404, 'Customer not found')
@cs.param('id', 'The Customer identifier')
class CustomerServiceID(Resource):
    '''Show a single customer '''
    @cs.doc('get_customer')
    @cs.marshal_with(customers)
    def get(self, id):
        '''Clientes por ID'''
        return DAOCST.get(id)


    @cs.doc('delete_Customer')
    @cs.response(204, 'Customer deleted')
    def delete(self, id):
        '''Delete a Customer given its identifier'''
        DAOCST.delete(id)
        return '', 204

    @cs.expect(customers)
    @cs.marshal_with(customers)
    def put(self, id):
        '''Actualizar un paquete por su ID'''
        return DAOCST.update(id, api.payload)

#TrajectoryService
class TrajectoryDAO(object):
    def __init__(self):
        self.counter = 0
        self.trajectorys = [

        {
        'id':1,
        'origin': 'Local',
        'destiny': 'Local',
        'cost': 3.500,
        
        
    },
       {
        'id':2,
        'origin': 'Local',
        'destiny':"Centro America",
        'cost': 5.000,
        
        
    },
    {
        'id':3,
        'origin': 'Local',
        'destiny': "Norte America",
        'cost': 7.500,
        
        
    } ,
    {
        'id':4,
        'origin': 'Local',
        'destiny': "Sur America",
        'cost': 7.200,
        
        
    } ,
    {
        'id':5,
        'origin': 'Local',
        'destiny': "Europa",
        'cost': 12.000,
        
        
    } ,
    {
        'id':6,
        'origin': 'Local',
        'destiny': "Asia",
        'cost': 13.500,
        
        
    } ,
    {
        'id':7,
        'origin': 'Local',
        'destiny': 'Africa',
        'cost': 11.350,
        
        
    }

]

    def get(self, id):
        for trajectory in self.trajectorys:
            if trajectory['id'] == id:
                return trajectory
        api.abort(404, "trajectory {} doesn't exist".format(id))

DAO = TrajectoryDAO()

@ts.route('/')
class TrajectoryService(Resource):
    '''Shows a list of all trajectorys'''
    @ts.doc('list trajectorys info')
    @ts.marshal_list_with(trajectorys)
    def get(self):
        '''Lista de informacion de trayectorias'''
        return DAO.trajectorys



#PackageService
class PackageDAO(object):
    def __init__(self):
        self.counter = 0
        self.packages = [
    {
        'id': 1,
        'name': 'zapato nike',
        'price': 50.000,
        
        
    }
]

    def get(self, id):
        for package in self.packages:
            if package['id'] == id:
                return package
        api.abort(404, "Package {} doesn't exist".format(id))

    def create(self, data):
        package = data
    
        new_package = {
            'id': random.randint(0,100),
            'name': package['name'],
            'price': package['price'],
            }

        self.packages.append(new_package)
        return package

    
    def update(self, id, data):
        package = self.get(id)
        package.update(data)
        return package

    def delete(self, id):
        package = self.get(id)
        self.packages.remove(package)

DAOPK = PackageDAO()

@ps.route('/')
class PackagesService(Resource):
    '''Shows a list of all packages'''
    @ps.doc('list packages info')
    @ps.marshal_list_with(packages)
    def get(self):
        '''Lista de informacion de paquetes'''
        return DAOPK.packages

    @ps.doc('create_package')
    @ps.expect(packages)
    @ps.marshal_with(packages, code=201)
    def post(self):
        '''Crear paquete'''
        return DAOPK.create(api.payload), 201



@ps.route('/<int:id>')
@ps.response(404, 'Package not found')
@ps.param('id', 'The package identifier')
class PackagesServiceID(Resource):
    @ps.doc('delete_package')
    @ps.response(204, 'Package deleted')
    def delete(self, id):
        '''Borrar paquete por ID'''
        DAOPK.delete(id)
        return '', 204

    @ps.expect(packages)
    @ps.marshal_with(packages)
    @ps.response(204, 'Package updated')
    def put(self, id):
        '''Actualizar paquete por id'''
        return DAOPK.update(id, api.payload)




#BillService
class BillDAO(object):
    def __init__(self):
        self.counter = 0

        self.bills = []

    @cs.marshal_with(customers)
    def getCustomer(self, id):
        return DAOCST.get(id)
        
    def get(self, id):
        for bill in self.bills:
            if bill['id'] == id:
                return bill
        api.abort(404, "Bill {} doesn't exist".format(id))

    def create(self, data):
        bill = data
        # print(data)
        # total=bill['package']['price']*bill['trajectory']['cost'],

        id_customer=(DAOCST.get( bill['customer']['id']))
        id_package=(DAOPK.get( bill['package']['id']))
        id_trajectory=(DAO.get( bill['trajectory']['id']))
        
        total=id_package['price']*id_trajectory['cost']
        new_bill = {
            'id': random.randint(0,100),
            'customer': {
                'id': id_customer['id'],
                'name': id_customer['name'],
                'lastname':id_customer['lastname'],
                'address': id_customer['address'],
                'postalC': id_customer['postalC'],
                },
            'package': {
                'id':id_package['id'],
                'name': id_package['name'],
                'price': id_package['price'],
            },
            'trajectory': {
                'id': id_trajectory['id'],
                'origin': id_trajectory['origin'],
                'destiny': id_trajectory['destiny'],
                'cost': id_trajectory['cost'],
            },
            'total':total,
            'date':bill['date'],

            }

        self.bills.append(new_bill)
        return bill

    

    def delete(self, id):
        bill = self.get(id)
        self.bills.remove(bill)

DAOBI = BillDAO()

@bs.route('/')
class BillService(Resource):
    '''Shows a list of all packages'''
    @bs.doc('list packages info')
    @bs.marshal_list_with(bills)
    def get(self):
        '''Lista de informacion de paquete'''
        return DAOBI.bills

    @bs.doc('create_package')
    @bs.expect(bills)
    @bs.marshal_with(bills, code=201)
    def post(self):
        '''Crear informacion de paquete'''
        return DAOBI.create(api.payload), 201



@bs.route('/<int:id>')
@bs.response(404, 'Bill not found')
@bs.param('id', 'The bill identifier')
class PackagesServiceID(Resource):
    @bs.doc('delete_bill')
    @bs.response(204, 'Bill deleted')
    def delete(self, id):
        '''Borrar paquete por ID'''
        DAOBI.delete(id)
        return '', 204





















if __name__ == '__main__':
    app.run(debug=True)
