from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

libros = [
    {"id": 1, "titulo": "El Quijote", "disponible": True},
    {"id": 2, "titulo": "Cien Años de Soledad", "disponible": False}
]
prestamos = [
    {"usuario": "Ana", "id_libro": 2}
]

@app.route('/libros', methods=['GET'])
def obtener_libros():
    return jsonify(libros), 200

@app.route('/prestamos', methods=['GET'])
def obtener_prestamos():
    prestamos_detallados = []
    for p in prestamos:
        libro = next((l for l in libros if l['id'] == p['id_libro']), None)
        if libro:
            prestamos_detallados.append({
                "usuario": p['usuario'],
                "id_libro": p['id_libro'],
                "titulo": libro['titulo']
            })
    return jsonify(prestamos_detallados), 200

@app.route('/libros', methods=['POST'])
def agregar_libro():
    datos = request.json
    titulo = datos.get('titulo', '').strip()
    
    if not titulo:
        return jsonify({"error": "El título del libro es obligatorio"}), 400
    

    for libro in libros:
        if libro['titulo'].lower() == titulo.lower():
            return jsonify({"error": "Ya existe un libro con ese título"}), 409
    

    nuevo_id = max([libro['id'] for libro in libros]) + 1 if libros else 1
    
    nuevo_libro = {
        "id": nuevo_id,
        "titulo": titulo,
        "disponible": True
    }
    
    libros.append(nuevo_libro)
    return jsonify({"mensaje": f"Libro '{titulo}' agregado exitosamente", "libro": nuevo_libro}), 201
@app.route('/prestar', methods=['POST'])
def solicitar_prestamo():
    datos = request.json
    id_libro = datos.get('id_libro')
    usuario = datos.get('usuario', '').strip()
    if not id_libro or not usuario:
        return jsonify({"error": "Faltan datos"}), 400
    if type(id_libro) is not int or id_libro <= 0:
        return jsonify({"error": "El ID del libro debe ser un número positivo mayor a 0"}), 400
    for libro in libros:
        if libro['id'] == id_libro:
            if libro['disponible']:
                libro['disponible'] = False
                prestamos.append({"usuario": usuario, "id_libro": id_libro})
                return jsonify({"mensaje": f"Préstamo exitoso de '{libro['titulo']}' para {usuario}"}), 200
            else:
                return jsonify({"error": "El libro ya está prestado"}), 409
                
    return jsonify({"error": "Libro no encontrado"}), 404


@app.route('/devolver', methods=['POST'])
def devolver_libro():
    datos = request.json
    id_libro = datos.get('id_libro')
    usuario = datos.get('usuario', '').strip()
    if not id_libro or not usuario:
        return jsonify({"error": "Faltan datos"}), 400
    if type(id_libro) is not int or id_libro <= 0:
        return jsonify({"error": "El ID del libro debe ser un número positivo mayor a 0"}), 400
    prestamo_actual = None
    for p in prestamos:
        if p['id_libro'] == id_libro:
            prestamo_actual = p
            break
            
    if not prestamo_actual:
        return jsonify({"error": "No hay un préstamo activo para este libro"}), 404
        
    if prestamo_actual['usuario'] != usuario:
        return jsonify({"error": f"Error: El libro fue prestado a {prestamo_actual['usuario']}, no puedes devolverlo tú."}), 403
    prestamos.remove(prestamo_actual)
    for libro in libros:
        if libro['id'] == id_libro:
            libro['disponible'] = True
            return jsonify({"mensaje": f"Libro '{libro['titulo']}' devuelto con éxito por {usuario}. ¡Ya está disponible!"}), 200
    return jsonify({"error": "Error interno del servidor"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)