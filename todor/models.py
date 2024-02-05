from todor import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    rol = db.Column(db.String(20), nullable = False)
    password = db.Column(db.Text, nullable = False)

    def __init__(self, username, rol, password):
        self.username = username
        self.rol = rol
        self.password = password


    def __repr__(self):
        return f'<User: {self.username} >'
    
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)

    def __init__(self, created_by, title, desc, assigned_to_id):
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.assigned_to_id = assigned_to_id

    def __repr__(self):
        return f'<Todo: {self.title} >'
