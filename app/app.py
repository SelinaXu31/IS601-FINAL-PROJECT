import simplejson as json
from flask import (
    Flask,
    render_template,
    redirect
)
from flask import current_app as app
from flask import request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from forms import ContactForm, SignupForm

app = Flask(__name__, template_folder="templates")
app.config.from_object('config.DevConfig')
app.config.from_pyfile('config.py')
mysql = MySQL(cursorclass=DictCursor)


app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscarData'
mysql.init_app(app)

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(
        render_template("404.html"),
        404
     )


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        render_template("400.html"),
        400
    )


@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(
        render_template("500.html"),
        500
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """User sign-up page."""
    signup_form = SignupForm(request.form)
    if request.method == 'POST':
        if signup_form.validate():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            website = request.form.get('website')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(
                    name=name,
                    email=email,
                    password=generate_password_hash(
                        password,
                        method='sha256'
                    ),
                    website=website
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main_bp.dashboard'))
            flash('A user exists with that email address.')
            return redirect(url_for('auth_bp.signup_page'))
    # GET: Serve Sign-up page
    return render_template(
        '/forms.html',
        title='Create an Account | Flask-Login Tutorial.',
        form=SignupForm(),
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route('/')
def home():
    nav = [
        {'name': 'Home', 'url': 'https://example.com/1'},
        {'name': 'About', 'url': 'https://example.com/2'},
        {'name': 'Pics', 'url': 'https://example.com/3'}
    ]
    return render_template[
        'home.html',
        nav=nav
        title="Welcome to My Site!",
        description="List of Oscar Reward Movies and Actors."
    ]


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Tianqi'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeFemale')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeFemale WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeFemale WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('year'), request.form.get('age'), request.form.get('name'),
                 request.form.get('movie'), city_id)
    sql_update_query = """UPDATE oscarAgeFemale t SET t.year = %s, t.age = %s, t.name = %s, t.movie = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar AwardForm')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('year'), request.form.get('age'),
                 request.form.get('name'), request.form.get('movie'))
    sql_insert_query = """INSERT INTO oscarAgeFemale (id, year,age,name,movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscarAgeFemale WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeFemale')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeFemale WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['id'], content['year'], content['age'],
                 content['name'], content['movie'])
    sql_insert_query = """INSERT INTO oscarAgeFemale (id,year,age,name,movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['year'], content['age'], content['name'],
                 content['movie'], city_id)
    sql_update_query = """UPDATE oscarAgeFemale t SET t.year = %s, t.age = %s, t.name = %s, t.movie = 
            %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscarAgeFemale WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
