from pymongo import MongoClient
import json

#Crea conexion mongo
myclient = MongoClient("mongodb+srv://"+varMongoUser+":"+varMongoPassword+"@cluster0.xbunp.mongodb.net")
mydb = myclient["prueba"]
mycol = mydb["carrito"]

#captura el payload    
data = json.loads(event["body"])

#Valida el campo user_id
if not 'user_id' in data:
    return {
    'statusCode': 406,
    'body': json.dumps('El campo user_id es necesario para continuar con la accion')
}
#Valida el campo del producto o si tiene la opción de limpiar el carrito    
if not 'product_id' in data and not 'delete_all' in data:
    return {
    'statusCode': 406,
    'body': json.dumps('Debe especificar que producto desea eliminar')
}

#inicializa la variable para filtar el borrado
myquery = {}

#arma el query si es un solo producto
if 'product_id' in data:
    myquery = {"user_id":data["user_id"], "product_id":data["product_id"]}

#La opción "delete all" tiene prioridad y cambia el filtro
if 'delete_all' in data:
    if data['delete_all']=='true':
        myquery = {"user_id":data["user_id"]}        
    
#ejecuta el borrado    
mycol.delete_many(myquery)

return {
    'statusCode': 200,
    'body': json.dumps('Ejecutado satisfactoriamente')
}
