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

@app.route('/prestar', methods=['POST'])
def solicitar_prestamo():
    datos = request.json
    id_libro = datos.get('id_libro')
    usuario = datos.get('usuario')

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
    usuario = datos.get('usuario')

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