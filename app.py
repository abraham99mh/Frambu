from flask import Flask, render_template, request, Response, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta, date

app = Flask(__name__,
            static_url_path='',
            static_folder='frambu/static',
            template_folder='frambu/templates')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frambu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sadgdkhjaslfb32r92bjdsf426543h35bwe'
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    id_cliente = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime())

    def __init__(self, amount, id_cliente, status, date):
        self.amount = amount
        self.id_cliente = id_cliente
        self.status = status
        self.date = date

    def __repr__(self):
        return '<Order %s>' % self.id


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Order %s>' % self.name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Admin %s>' % self.username


@app.route('/')
def home():
    if 'admin' in session:
        clients = Client.query.all()
        cantidadClientes = len(clients)
        p = Order.query.filter(Order.status == False).all()
        pendientes = len(p)
        l = Order.query.filter(Order.status == True).all()
        listas = len(l)

        dates = [0, 0, 0, 0, 0, 0, 0]
        orders_by_date = [[], [], [], [], [], [], []]
        cant = [0, 0, 0, 0, 0, 0, 0]

        for i in range(7):
            dates[i] = date.today() - timedelta(days=i)
            orders_by_date[i] = Order.query.filter(
                func.date(Order.date) == dates[i]).all()
            for order in orders_by_date[i]:
                if order.status == True:
                    cant[i] = cant[i] + 1

        return render_template('index.html', cantidadClientes=cantidadClientes, pendientes=pendientes, listas=listas, ordPendientes=p, dates=dates, cant=cant)

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'admin' in session:
            return redirect(url_for("clients"))
        return render_template('login.html')
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']

        admin = Admin.query.get(1)
        if admin.username == un and admin.password == pw:
            session['admin'] = un
            return redirect(url_for('home'))
        flash("Credenciales inválidas", 'danger')
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    if 'admin' in session:
        session.pop('admin', None)
    return redirect(url_for("login"))


@app.route('/clientes', methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        clients = Client.query.all()
        return render_template('clients.html', clients=clients)
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        client = Client(name)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("clients"))


@ app.route('/crear-orden', methods=['GET', 'POST'])
def create_order():
    if request.method == 'GET':
        orders = Order.query.all()
        clients = Client.query.all()
        return render_template('create_order.html', clients=clients, orders=orders)
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        amount = request.form['amount']
        order = Order(amount, id_cliente, False, datetime.now())
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("create_order"))


@ app.route('/edit-amount', methods=['POST'])
def edit_amount():
    if request.method == 'POST':
        order_id = request.form['id']
        new_amount = request.form['new_amount']
        order = Order.query.get_or_404(order_id)
        order.amount = new_amount
        db.session.commit()
        return Response(status=200)


@ app.route('/update-order', methods=['POST'])
def update_order():
    if request.method == 'POST':
        order_id = request.form['id']
        order = Order.query.get_or_404(order_id)
        if order.status:
            order.status = False
        else:
            order.status = True
        db.session.commit()
        return Response(status=200)


@ app.route('/edit-success')
def edit_success():
    return redirect(url_for("create_order"))


@ app.route('/delete-order', methods=['POST'])
def delete_order():
    if request.method == 'POST':
        order_id = request.form['id']
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return Response(status=200)


@ app.route('/delete-success')
def delete_success():
    return redirect(url_for("create_order"))


if __name__ == '__main__':
    app.run(debug=True)
