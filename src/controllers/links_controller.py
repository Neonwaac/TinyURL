from flask import Blueprint, request, redirect, render_template, jsonify, url_for
from src.models.LinkModel import LinkModel
from src.models.MetadataModel import MetadataModel
import string
import random

links_controller = Blueprint('links_controller', __name__)

def generate_short_code():
    """Genera un código aleatorio de entre 6 y 8 caracteres."""
    length = random.randint(6, 8)
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@links_controller.route('/', methods=['GET'])
def index():
    """
    Ruta base para la visualización de la interfaz (Formulario de Creación)
    """
    return render_template('index.html')

@links_controller.route('/links', methods=['GET'])
def list_links():
    """
    Ruta para listar los enlaces creados
    """
    links = LinkModel.get_all_links() or []
    
    # Enriquecer los enlaces con la metadata de MongoDB
    display_links = []
    for link in links:
        metadata = MetadataModel.get_metadata(link['codigo'])
        if metadata:
            link['imagen'] = metadata.get('imagen')
            link['descripcion'] = metadata.get('descripcion')
        display_links.append(link)
            
    return render_template('links.html', links=display_links)

@links_controller.route('/create', methods=['POST'])
def create_link():
    """
    Función para crear enlace
    Recibe datos del formulario
    """
    url_original = request.form.get('url_original')
    imagen = request.form.get('imagen')
    descripcion = request.form.get('descripcion')
    
    # 1. Validación de campos obligatorios
    if not url_original or not imagen or not descripcion:
        return render_template('index.html', error="Todos los campos son obligatorios.")

    # 2. Validación de duplicados
    existing_link = LinkModel.get_link_by_url(url_original)
    if existing_link:
        return render_template('index.html', error=f"El enlace ya está registrado. Código existente: {existing_link['codigo']}")

    # Generar código único
    codigo = generate_short_code()
    
    # Guardar en MySQL
    if LinkModel.create_link(codigo, url_original):
        # Guardar en MongoDB
        MetadataModel.create_metadata(codigo, imagen, descripcion)
        # Redirigir al listado de enlaces después de crear exitosamente
        return redirect(url_for('links_controller.list_links'))
    else:
         return render_template('index.html', error="Error al crear el enlace. Intente nuevamente.")


@links_controller.route('/<codigo>', methods=['GET'])
def redirect_to_url(codigo):
    """
    Función para redireccionar a la URL original
    Busca el enlace en MySQL
    Actualiza clicks en MySQL
    Redirecciona
    """
    # Buscar enlace en MySQL
    link = LinkModel.get_link_by_code(codigo)
    
    if link:
        # Incrementar clicks
        LinkModel.increment_clicks(codigo)
        # Redireccionar
        return redirect(link['url_original'])
    
    return "Enlace no encontrado", 404

@links_controller.route('/api/links', methods=['GET'])
def get_links():
    """
    Función para obtener enlaces (API)
    """
    links = LinkModel.get_all_links() or []
    
    updated_links = []
    for link in links:
        metadata = MetadataModel.get_metadata(link['codigo'])
        if metadata:
            link['imagen'] = metadata.get('imagen')
            link['descripcion'] = metadata.get('descripcion')
            if '_id' in metadata:
                del metadata['_id'] # No serializable
            # Convertir fechas a string si es necesario
            if 'createdAt' in metadata:
                link['createdAt'] = str(metadata['createdAt'])
        updated_links.append(link)
        
    return jsonify(updated_links)
