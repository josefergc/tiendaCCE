from createUpdateCart import *
from getCart import * 
from deleteCart import * 
from getProducts import *
import unittest

class TestAPI(unittest.TestCase):
    def listado_productos(self):
       self.assertAlmostEqual(getProducts({"queryStringParameters" : { 'pagina':3, 'num_productos':3 }}), {'statusCode': 200, 'body': '{"products": {"product_1": {"product_id": 100, "name": "Producto 10", "image": "https://image.com/product10.png", "precio": 2000.0}, "product_2": {"product_id": 110, "name": "Producto 11", "image": "https://image.com/product11.png", "precio": 2000.0}}}'} )
   
    
    
    def test_create_update(self):
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 111, "product_id": 10, "nombre": "Producto 1", "cantidad": 10, "precio":1500 }'}), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 111, "product_id": 10, "cantidad": 20}' }), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 111, "product_id": 20, "nombre": "Producto 2", "cantidad": 5000, "precio":1550}' }), {'statusCode': 406,'body': json.dumps('No hay Stock suficiente del producto para realizar la compra')})
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 111, "product_id": 20, "nombre": "Producto 2", "cantidad": 30, "precio":1550}' }), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{  "cantidad": 30, "precio":1550}' }), {'statusCode': 406,'body': json.dumps('Los campos user_id y product_id son necesarios para continuar con la accion') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 111, "product_id": 30, "nombre": "Producto 3", "cantidad": 100, "precio":450.98}' }), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 222, "product_id": 10, "nombre": "Producto 1", "cantidad": 10, "precio":1500 }'}), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(createUpdateCart({"body" : '{ "user_id": 222, "product_id": 20, "nombre": "Producto 2", "cantidad": 20, "precio":1550 }'}), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
    
    def test_getCart(self):
       self.assertAlmostEqual(getCart({"queryStringParameters" : { "user_id": 111 }}), {'statusCode': 200, 'body': '{"cart": {"item_1": {"producto": "Producto 1", "cantidad": 20, "precio": 1500}, "item_2": {"producto": "Producto 2", "cantidad": 30, "precio": 1550}, "item_3": {"producto": "Producto 3", "cantidad": 100, "precio": 450.98}}}'} )
        
    def test_deleteCart(self):
        self.assertAlmostEqual(deleteCart({"body" : '{ "user_id": 111, "product_id": 20 }'}), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(deleteCart({"body" : '{ "user_id": 111, "delete_all": 20 }'}), {'statusCode': 200,'body': json.dumps('Ejecutado satisfactoriamente') })
        self.assertAlmostEqual(getCart({"queryStringParameters" : { "user_id": 111 }}), {'statusCode': 200, 'body': '{"cart": {}}'} )
                                                                            
        
        
      