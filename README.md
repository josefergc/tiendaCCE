# API - Tienda
El API esta configurado en API Gateway de AWS, el cual permite grandes volúmenes de llamadas a sus servicios y al ser tecnología ServerLess, permite un escalamiento rápido.
El API Gateway accede a lambda function donde están implementados en lenguaje Python.
Hay 2 bases de datos, una base relacional en MySQL con la información maestro de los productos y una base de datos NoSQL en Mongo para guardar la información del carrito.

Los llamados disponibles son:

### Listar los productos
Devuelve los productos disponibles con paginación. Si no se envia paginación envia los primeros 100 productos.

**codigo:**  getProducts.py        **url:** https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/catalog

**Metodo:** GET   **Header:**   x-api-key => yWA656mi4c4LxVy5XUdbs3LHA9aaGBf53dxEAP9s


**QueryStringParameters**:

pagina (Página que desea desplegar - la primera pagina es 0)

num_productos (cuantos productos se despliegan por página)

**Ejemplo**

https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/catalog?pagina=3&num_productos=3


------------


### Crear o modificar artículos en el carrito
La función crea un producto o lo edita en caso de ya haber sido adicionado al carrito con anterioridad. Antes de adicionar el producto al carrito se verifica que haya stock del producto. 

**codigo:** createUpdateCart.py      **url:** https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/cart

**Metodo:** POST     **Header:** x-api-key => yWA656mi4c4LxVy5XUdbs3LHA9aaGBf53dxEAP9s

**Payload:**
{
   "user_id": 300,
   "product_id": 20,
   "nombre": "Producto 2",
   "cantidad": 10.5,
   "precio”: 2500
}

------------

### Traer Productos del carrito
La función recibe el usuario y devuelve los artículos que el usuario dispone en su carrito.

**codigo:** getCart.py   **url:** https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/cart

**Metodo:** GET       **Header:** x-api-key => yWA656mi4c4LxVy5XUdbs3LHA9aaGBf53dxEAP9s

**QueryStringParameters**: 

user_id (identificador del usuario)

**Ejemplo**

https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/cart?user_id=399

------------

### Eliminar artículos en el carrito
La función elimina un producto del carrito o permite eliminar todos los productos del carrito con la opción“delete_all" con el valor "true".

**codigo:**deleteCart.py  **url:** https://p4sp89boud.execute-api.us-east-1.amazonaws.com/alpha/cart
**Metodo:** DELETE   **Header:** x-api-key=> yWA656mi4c4LxVy5XUdbs3LHA9aaGBf53dxEAP9s
**Payload:**
{
   "user_id": 300,
   "product_id": 20,
   "delete_all": “true”
}


## Diseño
Todas las llamadas son recibidas por el API Gateway, que permite recibir un gran volumen de llamadas simultaneas, ademas permite manejar autenticación y autorización a los recursos.
Para que la solución se creo un API Key pero se recomienda que el API solo sea accesible a traves de los roles internos de AWS.
Los lambda function manejan API Secret de este modo los usuarios y sus respectivos passwords de la base de datos relacional y de la BD NoSQL no estan quemados en el codifgo.
![](https://jota-chat.s3.amazonaws.com/modeloCCE.png)

### Base de datos
En el diagrama se detalla el modelo de datos, para la BD de datos se detalla el script de creación de la tabla y los datos de prueba:


```
CREATE TABLE productos (
    ID int,
    Nombre varchar(255),
    Descripción text,
    Imagen varchar(255),
    Precio float(20),
    Uom varchar(50),
    Activo Tinyint, 
    Stock int,
    PRIMARY KEY (ID)
);

INSERT INTO productos VALUES (10, "Producto 1", "Descripcion producto 1", "https://image.com/product1.png",1500,"Unidad",1,1000);
INSERT INTO productos VALUES (20, "Producto 2", "Descripcion producto 2", "https://image.com/product2.png",1550,"Unidad",1,1000);
INSERT INTO productos VALUES (30, "Producto 3", "Descripcion producto 3", "https://image.com/product3.png",450.98,"Unidad",1,1000);
INSERT INTO productos VALUES (40, "Producto 4", "Descripcion producto 4", "https://image.com/product4.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (50, "Producto 5", "Descripcion producto 5", "https://image.com/product5.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (70, "Producto 7", "Descripcion producto 7", "https://image.com/product7.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (80, "Producto 8", "Descripcion producto 8", "https://image.com/product8.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (90, "Producto 9", "Descripcion producto 9", "https://image.com/product9.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (100, "Producto 10", "Descripcion producto 10", "https://image.com/product10.png",2000,"Unidad",1,1000);
INSERT INTO productos VALUES (110, "Producto 11", "Descripcion producto 11", "https://image.com/product11.png",2000,"Unidad",1,5);
INSERT INTO productos VALUES (120, "Producto 12", "Descripcion producto 12", "https://image.com/product12.png",2000,"Unidad",0,0);
INSERT INTO productos VALUES (130, "Producto 13", "Descripcion producto 13", "https://image.com/product13.png",2000,"Unidad",0,0);

```


### Pruebas Unitarias

Se ejecutan las pruebas unitarias en el archivo testpruebas.py con resultado satisfactorio.

![](https://jota-chat.s3.amazonaws.com/unitTestResult.png)
