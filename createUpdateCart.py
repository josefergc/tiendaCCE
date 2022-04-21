from pymongo import MongoClient
import pymysql
import json

#Crea conexion Mysql    
db = pymysql.connect(host='database-cce.ckrk1ltkekxb.us-east-1.rds.amazonaws.com',user=varUser,password=varPassword,db='tienda')
cursor = db.cursor()

#Crea conexion mongo
myclient = MongoClient("mongodb+srv://"+varMongoUser+":"+varMongoPassword+"@cluster0.xbunp.mongodb.net")
mydb = myclient["prueba"]
mycol = mydb["carrito"]

#Carga la información del payload
data = json.loads(event["body"])

#Valida si el campo user_id o product_id se envian en el llamado    
if not 'user_id' in data or not 'product_id' in data:
    return {
        'statusCode': 406,
        'body': json.dumps('Los campos user_id y product_id son necesarios para continuar con la accion')
    }    

#Obtiene el stock del producto
cursor.execute('''SELECT Stock FROM productos where ID=''' + str(data["product_id"]) )
myresult = cursor.fetchone()

#ejecuta el query para validar si ya esta el producto en el carrito
myquery = {"user_id":data["user_id"], "product_id":data["product_id"]}
product = mycol.find_one(myquery)

#si el producto se crea/actualiza en el carrito debe enviar el campo cantidad
if not 'cantidad' in data:
    return {
    'statusCode': 406,
    'body': json.dumps('El campo cantidad es necesario para continuar con la accion')
}

#Valida que haya el stock del producto para hacer la compra
if myresult[0]<data["cantidad"]:
    return {
    'statusCode': 406,
    'body': json.dumps('No hay Stock suficiente del producto para realizar la compra')
}

#si el producto es nuevo o se actualiza realiza el cargue respectivo
if not product:
    #si el producto es nuevo en el carrito debe enviar todo los campos
    if not 'nombre' in data or  not 'precio' in data:
        return {
        'statusCode': 406,
        'body': json.dumps('Los campos nombre y precio son necesarios para continuar con la accion')
    }  
    
    mylist = [ { "user_id": data["user_id"], "product_id":data["product_id"],"nombre":data["nombre"], "cantidad":data["cantidad"],"precio":data["precio"]}]  
    x = mycol.insert_many(mylist)
else:
    x = mycol.update_one(myquery, {"$set": { "cantidad":data["cantidad"]} }) 

db.close()

return {
    'statusCode': 200,
    'body': json.dumps('Ejecutado satisfactoriamente')
}