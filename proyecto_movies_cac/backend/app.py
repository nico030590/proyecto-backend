from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, Usuario

# Crear la función de fábrica de la aplicación Flask
def create_app():
    app = Flask(__name__, static_folder='../frontend', template_folder='../frontend/pages')
    CORS(app)

    # Configurar la aplicación con la clase Config definida en config.py
    app.config.from_object(Config)

    # Configuración de la base de datos con SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'iniciar_sesion'  # Especificar la vista para el inicio de sesión

    # Función para cargar un usuario desde la base de datos
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Rutas de la aplicación
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return render_template('index.html', username=current_user.nombre)
        else:
            return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            contraseña = request.form['contraseña']
            fecha_nacimiento = request.form['fechaNacimiento']
            pais = request.form['pais']

            # Crea un nuevo usuario
            nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email, contraseña=contraseña,
                                    fechaNacimiento=fecha_nacimiento, pais=pais)

            try:
                # Guarda el nuevo usuario en la base de datos
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash('Registro exitoso')
                return redirect(url_for('index'))  # Redirige a la página principal después del registro exitoso
            except Exception as e:
                flash('Error al registrar usuario: ' + str(e))  # Manejo de errores
                db.session.rollback()  # Revierte la sesión en caso de error

        return render_template('registrarse.html')

    @app.route('/login', methods=['GET', 'POST'])
    def iniciar_sesion():
        if request.method == 'POST':
            # Lógica para iniciar sesión (por completar)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        return render_template('iniciosesion.html')

    @app.route('/logout')
    @login_required  # Requiere que el usuario esté autenticado para acceder
    def cerrar_sesion():
        logout_user()  # Cerrar sesión del usuario
        flash('Sesión cerrada exitosamente')
        return redirect(url_for('index'))

    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('../frontend/css', path)

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('../frontend/js', path)

    # Ruta para la página de edición de usuario y listado de usuarios
    @app.route('/editar_usuario', methods=['GET'])
    # @login_required
    def editar_usuario():
         usuarios = Usuario.query.all()
         return render_template('editar_usuario.html', usuarios=usuarios, usuario_editar=None)

    @app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
    # @login_required
    def editar_usuario_id(id):
        usuario_editar = Usuario.query.get_or_404(id)

        if request.method == 'POST':
            usuario_editar.nombre = request.form['nombre']
            usuario_editar.email = request.form['email']
            usuario_editar.edad = request.form['edad']

            try:
                db.session.commit()
                flash('Usuario actualizado exitosamente', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar usuario: {str(e)}', 'error')

            return redirect(url_for('editar_usuario'))

        usuarios = Usuario.query.all()
        return render_template('editar_usuario.html', usuarios=usuarios, usuario_editar=usuario_editar)

    @app.route('/eliminar_usuario/<int:id>', methods=['POST'])
    # @login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
    def eliminar_usuario(id):
        usuario = Usuario.query.get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
            flash('Usuario eliminado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar usuario: {str(e)}', 'error')

        return redirect(url_for('editar_usuario'))

    @app.route('/assets/<path:path>')
    def send_assets(path):
        return send_from_directory('../frontend/assets', path)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
