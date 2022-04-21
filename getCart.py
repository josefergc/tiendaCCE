from pymongo import MongoClient
import json

#Crea conexion mongo
myclient = MongoClient("mongodb+srv://"+varMongoUser+":"+varMongoPassword+"@cluster0.xbunp.mongodb.net")
mydb = myclient["prueba"]
mycol = mydb["carrito"]

#Valida si no envian ningun parametro y devuelve error
if not event["queryStringParameters"]:
    return {
        'statusCode': 406,
        'body': json.dumps('El campo user_id es necesario para continuar con la accion')
    }   

#Valida si envia el campo usuario y devuelve error
if not 'user_id' in event["queryStringParameters"]:
    return {
            'statusCode': 406,
            'body': json.dumps('El campo user_id es necesario para continuar con la accion')
    } 

#obtiene el usuario del parametro y genera el filtro de busqueda
user = int(event["queryStringParameters"]['user_id'])
myquery = {"user_id":user}

#variable para crear el resultado (listado de productos en el carrito)
dictItems = {}
item = 0

#recorre cada producto y lo deja en el formato de salida
for product in mycol.find(myquery):
    item+=1
    dictItems["item_"+str(item)] = {"producto":product["nombre"],"producto":product["nombre"],"cantidad":product["cantidad"], "precio":product["precio"]}
    
#Devuelve resultado    
return {
    'statusCode': 200,
    'body': json.dumps({'cart':dictItems})
}
