from flask import Blueprint, flash, render_template, request, redirect, url_for, g
from todor.auth import login_required
from .models import Todo, User
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        assigned_to_id = request.form['assigned_to']

        try:
            assigned_to_id = int(assigned_to_id)
        except ValueError:
            #flash('Error: El ID del usuario asignado no es válido.', 'error')
            return redirect(url_for('todo.create'))

        todo = Todo(created_by=g.user.id, title=title, desc=desc, assigned_to_id=assigned_to_id)

        db.session.add(todo)
        db.session.commit()
        

        # flash('Se creó una nueva tarea para el usuario.', 'success')  # Agrega un mensaje de éxito

        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Obtener los valores del formulario
            title = request.form['title']
            desc = request.form['desc']
            
            # Obtener el valor de assigned_to solo si está presente en la solicitud POST
            assigned_to_id = request.form.get('assigned_to', None)
            
            # Verificar si el checkbox está marcado
            state = 'state' in request.form  

            # Actualizar los atributos de la tarea
            todo.title = title
            todo.desc = desc
            if assigned_to_id is not None:
                todo.assigned_to_id = assigned_to_id
            todo.state = state

            # Guardar la tarea actualizada en la base de datos
            db.session.commit()

            # flash('Tarea actualizada correctamente.', 'success')
            return redirect(url_for('todo.index'))

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")

    return render_template('todo/update.html', todo=todo)




@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))