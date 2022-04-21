import pymysql
import json

#Crea conexion Mysql    
db = pymysql.connect(host='database-cce.ckrk1ltkekxb.us-east-1.rds.amazonaws.com',user=varUser,password=varPassword,db='tienda')
cursor = db.cursor()

#valores por defecto si no envia la paginación (los 100 primeros productos)
page = "0"
limite = "100"

#Verifica si hay parametros en el API de llamado
if event['queryStringParameters']:
    page = event['queryStringParameters'].get("pagina","0")
    limite = event["queryStringParameters"].get('num_productos',"100")

#Realiza el calculo de los productos a desplegar
if page != '0':
    page = str(int(limite)*int((event["queryStringParameters"]['pagina'])))

#Trae el listado de productos activos con paginación
cursor.execute("SELECT ID,Nombre,Imagen,Precio FROM productos WHERE ACTIVO = 1 LIMIT "+ limite + " OFFSET " + page + ";")
myresult = cursor.fetchall()


dictItems = {}
item = 0
#show each product
for product in myresult:
    item+=1
    dictItems["product_"+str(item)] = {"product_id":int(product[0]),"name":product[1],"image":product[2], "precio":float(product[3])}

db.close()
    
return {
    'statusCode': 200,
    'body': json.dumps({'products':dictItems})
    }