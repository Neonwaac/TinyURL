# Rutas de la Aplicación

## Página principal
GET /
- Muestra el formulario para crear enlaces

## Crear enlace
POST /create
- Recibe:
  - url_original
  - imagen
  - descripcion
- Crea un nuevo enlace corto

## Listar enlaces
GET /links
- Muestra la tabla con todos los enlaces almacenados

## Redirección
GET /<codigo>
- Redirige al enlace original
- Incrementa el contador de clicks
- Retorna 404 si no existe