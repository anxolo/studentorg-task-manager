from flask import Blueprint, render_template, request, url_for, redirect, session, flash, current_app
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

def get_engine():
    """Get the SQLAlchemy engine from the app config"""
    return current_app.config['SQLALCHEMY_ENGINE']

def fetch_query(query, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row._mapping) for row in result]
    except Exception as e:
        print(f"Error DB fetch: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return []

def execute_query(query, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text(query), params or {})
            conn.commit()
            return True
    except Exception as e:
        print(f"Error DB execute: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return False

@main.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    
    open_tasks = fetch_query("SELECT * FROM tarefas WHERE estado != 'Feito' ORDER BY data_entrega IS NULL, data_entrega ASC")
    done_tasks = fetch_query("SELECT * FROM tarefas WHERE estado = 'Feito' ORDER BY data_entrega ASC")
    return render_template('index.html', usuario=session.get('usuario'), open_tasks=open_tasks, done_tasks=done_tasks)

@main.route('/login', methods=['POST', 'GET'])
def login():
    if 'usuario' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            result = fetch_query("SELECT * FROM usuarios WHERE usuario = :username", {'username': username})
            
            if result and check_password_hash(result[0]['contrasinal'], password):
                session.permanent = True
                session['usuario'] = result[0]['usuario']
                session['usuario_id'] = result[0]['id']
                return redirect(url_for('main.index'))
            else:
                flash('Usuario ou contrasinal incorrectos', 'error')
        except Exception as e:
            print(f"Error no login: {e}")
            flash('Erro ao iniciar sesión', 'error')
    
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'usuario' not in session: 
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        print("DEBUG: Formulario recibido")
        print(f"DEBUG: Form data: {request.form}")
        
        descricion = request.form.get('descricion', '').strip()
        responsable = request.form.get('responsable', '').strip()
        comision = request.form.get('comision', '').strip()
        data_entrega = request.form.get('data_entrega', '').strip() or None
        estado = request.form.get('estado', 'Pendente')
        
        print(f"DEBUG: Datos procesados - descricion={descricion}, responsable={responsable}, comision={comision}, data_entrega={data_entrega}, estado={estado}")
        
        if not descricion or not responsable:
            flash('A descrición e o responsable son obrigatorios', 'error')
            return render_template('add_task.html', usuario=session.get('usuario'))
        
        try:
            success = execute_query(
                "INSERT INTO tarefas (descricion, responsable, comision, data_entrega, estado) VALUES (:desc, :resp, :com, :fecha, :est)",
                {
                    'desc': descricion,
                    'resp': responsable,
                    'com': comision if comision else None,
                    'fecha': data_entrega,
                    'est': estado
                }
            )
            
            if success:
                print("DEBUG: Tarefa gardada correctamente")
                flash('Tarefa engadida correctamente', 'success')
                return redirect(url_for('main.index'))
            else:
                print("DEBUG: Erro ao gardar tarefa")
                flash('Erro ao engadir a tarefa. Revisa os logs do servidor.', 'error')
        except Exception as e:
            print(f"DEBUG: Excepción ao gardar: {e}")
            flash(f'Erro inesperado: {str(e)}', 'error')
        
        return render_template('add_task.html', usuario=session.get('usuario'))
    
    # Obtener las 3 comisiones y responsables más repetidos
    top_comisiones = fetch_query(
        "SELECT comision, COUNT(*) as count FROM tarefas WHERE comision IS NOT NULL AND comision != '' GROUP BY comision ORDER BY count DESC LIMIT 3"
    )
    top_responsables = fetch_query(
        "SELECT responsable, COUNT(*) as count FROM tarefas WHERE responsable IS NOT NULL AND responsable != '' GROUP BY responsable ORDER BY count DESC LIMIT 3"
    )
    
    return render_template('add_task.html', 
                         usuario=session.get('usuario'),
                         top_comisiones=top_comisiones,
                         top_responsables=top_responsables)

@main.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    if 'usuario' not in session: 
        return redirect(url_for('main.login'))
    execute_query("UPDATE tarefas SET estado=:estado WHERE id=:task_id", 
                  {'estado': request.form.get('estado'), 'task_id': task_id})
    return redirect(url_for('main.index'))

@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'usuario' not in session: 
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        descricion = request.form.get('descricion', '').strip()
        responsable = request.form.get('responsable', '').strip()
        comision = request.form.get('comision', '').strip()
        data_entrega = request.form.get('data_entrega', '').strip() or None
        estado = request.form.get('estado', 'Pendente')
        
        if not descricion or not responsable:
            flash('A descrición e o responsable son obrigatorios', 'error')
        else:
            success = execute_query(
                "UPDATE tarefas SET descricion=:desc, responsable=:resp, comision=:com, data_entrega=:fecha, estado=:est WHERE id=:task_id",
                {
                    'desc': descricion,
                    'resp': responsable,
                    'com': comision if comision else None,
                    'fecha': data_entrega,
                    'est': estado,
                    'task_id': task_id
                }
            )
            if success:
                flash('Tarefa actualizada correctamente', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Erro ao actualizar a tarefa', 'error')
    
    task = fetch_query("SELECT * FROM tarefas WHERE id=:task_id", {'task_id': task_id})
    if not task: 
        return "Not found", 404
    return render_template('edit_task.html', task=task[0], task_id=task_id, usuario=session.get('usuario'))

@main.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    execute_query("DELETE FROM tarefas WHERE id=:task_id", {'task_id': task_id})
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if 'usuario' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not username or not password or not password_confirm:
            flash('Todos os campos son obrigatorios', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('O usuario debe ter polo menos 3 caracteres', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('A contrasinal debe ter polo menos 6 caracteres', 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('As contrasinais non coinciden', 'error')
            return render_template('register.html')
        
        try:
            existe = fetch_query("SELECT id FROM usuarios WHERE usuario = :username", {'username': username})
            
            if existe:
                flash('Este usuario xa está rexistrado', 'error')
                return render_template('register.html')
            
            hash_password = generate_password_hash(password)
            execute_query(
                "INSERT INTO usuarios (usuario, contrasinal) VALUES (:username, :password)",
                {'username': username, 'password': hash_password}
            )
            
            flash('Usuario creado correctamente! Agora podes iniciar sesión', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            print(f"Error no rexistro: {e}")
            flash('Erro ao crear o usuario', 'error')
    
    return render_template('register.html')