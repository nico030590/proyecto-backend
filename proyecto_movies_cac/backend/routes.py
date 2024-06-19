from flask import jsonify, request, redirect, url_for, flash, render_template, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db  
from models import Usuario 

# Ruta para obtener un usuario por su ID
@app.route('/usuarios/<int:user_id>', methods=['GET'])
def obtener_usuario_por_id(user_id):
    usuario = Usuario.query.get(user_id)
    if usuario:
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'fechaNacimiento': usuario.fechaNacimiento.isoformat(),
            'pais': usuario.pais,
            'fecha_registro': usuario.fecha_registro.isoformat()
        }), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
# Ruta para obtener todos los usuarios (ejemplo API)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    # Serializar solo los campos necesarios
    usuarios_serializados = [
        {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'fechaNacimiento': usuario.fechaNacimiento.strftime('%Y-%m-%d'),
            'pais': usuario.pais,
            'fecha_registro': usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }
        for usuario in usuarios
    ]
    return jsonify(usuarios_serializados), 200

# Ruta para crear un nuevo usuario (ejemplo API)
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(nombre=data['nombre'], apellido=data['apellido'], email=data['email'], contraseña=data['contraseña'], fechaNacimiento=data['fechaNacimiento'], pais=data['pais'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario creado exitosamente"}), 201

# Ruta para actualizar un usuario específico por su ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    data = request.json
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.email = data.get('email', usuario.email)
    usuario.contraseña = data.get('contraseña', usuario.contraseña)
    usuario.fechaNacimiento = data.get('fechaNacimiento', usuario.fechaNacimiento)
    usuario.pais = data.get('pais', usuario.pais)

    db.session.commit()
    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

# Ruta para eliminar un usuario específico por su ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

# Ruta para la página principal
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.nombre)
    else:
        return render_template('index.html')

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Datos del formulario recibidos:", request.form)
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        fechaNacimiento = request.form['fechaNacimiento']
        pais = request.form['pais']
        terminos = request.form.get('terminos')

        # Validación de campos obligatorios y términos y condiciones
        if not (nombre and apellido and email and contraseña and fechaNacimiento and pais and terminos):
            flash('Por favor, completa todos los campos y acepta los términos y condiciones.')
            return redirect(url_for('register'))

        # Guardar el nuevo usuario en la base de datos
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña, fechaNacimiento=fechaNacimiento, pais=pais)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso')
        return redirect(url_for('index'))

    return render_template('registrarse.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validar las credenciales
        usuario = Usuario.verificar_credenciales(email, password)

        if usuario:
            login_user(usuario)  # Iniciar sesión para el usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))  # Redirigir a la página principal
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
            return redirect(url_for('iniciar_sesion'))  # Redirigir de nuevo a la página de inicio de sesión

    # Si el método no es POST, renderizar el formulario de inicio de sesión
    return render_template('iniciosesion.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required  # Requiere que el usuario esté autenticado para acceder
def cerrar_sesion():
    logout_user()  # Cerrar sesión del usuario
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('index'))

# Ruta para servir archivos CSS
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../frontend/css', path)

# Ruta para servir archivos JS
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../frontend/js', path)

# Ruta para servir otros archivos estáticos
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('../frontend/assets', path)

# Ruta para la edición de usuarios
@app.route('/pages/editar_usuario', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def editar_usuario():
    return render_template('editar_usuario.html')

