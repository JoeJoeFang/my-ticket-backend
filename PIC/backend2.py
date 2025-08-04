from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import os
import base64
from PIL import Image
import io
from sqlalchemy import JSON
#from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
#db = SQLAlchemy(app)
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '924082621'
DATABASE = '9900_learn'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪修改，提升性能\
app.config['SECRET_KEY'] = 'your_secret_key_here'
current_directory = os.path.dirname(os.path.abspath(__file__))
pic_folder = os.path.join(current_directory, 'PIC')
#app.config['PIC_FLODER'] = pic_folder

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Host(db.Model):
    __tablename__ = "host"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80),nullable=False)
    companyName = db.Column(db.String(20), nullable=False)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    datentime = db.Column(db.String(30), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    suburb = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    #last_update = db.Column(db.DateTime, default=datetime.now)

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(160),nullable=False)
    name = db.Column(db.String(20), nullable=False)
    cvc = db.Column(db.String(20), nullable=False)
    duedate = db.Column(db.String(20), nullable=True)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    datentime = db.Column(db.String(30), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    suburb = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    order = db.Column(JSON, nullable=True)
    #last_update = db.Column(db.DateTime, default=datetime.now)

class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    organizername = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    seats = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    from_time = db.Column(db.String(10), nullable=True)
    to_time = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    URL = db.Column(db.String(100), nullable=True)
    thumbnail = db.Column(db.String(5000), nullable=True)
    #last_update = db.Column(db.DateTime, default=datetime.now)

class Events_order(db.Model):
    __tablename__ = "events_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventtitle = db.Column(db.String(20), nullable=False)
    orderdetails = db.Column(JSON, nullable=True)

class Myevents(db.Model):
    __tablename__ = "myevents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.String(50), nullable=False)
    host = db.Column(db.String(50), nullable=False)

@app.route("/user/list")
def delete():
    want_del_id = request.args.get("delete", default=1, type=int)
    query_id = Host.query.filter_by(id=want_del_id).first()
    if not query_id:
        return "message:User not found"
    db.session.delete(query_id)
    db.session.commit()
    return f"message: The user with id {id} was removed from the database!"

@app.route("/user/add")
def add_user():
    user1 = Host(email="刘畅", password="924082621")
    db.session.add(user1)
    db.session.commit()
    return "用户创建成功！"

def add_users():
    user1 = Host(email="刘畅", password="924082621")
    db.session.add(user1)
    db.session.commit()
    return user1

def image_to_base64(image_path):
    # 使用 Pillow 打开图片
    with Image.open(image_path) as image:
        # 将图片转换为二进制数据
        buffered = io.BytesIO()
        image.save(buffered, format=image.format)
        # 将二进制数据编码为 Base64 字符串
        img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#    password = db.Column(db.String(60), nullable=False)

# def create_default_user():
#     default_user = User.query.filter_by(email='default@example.com').first()
#     if not default_user:
#         hashed_password = bcrypt.generate_password_hash('default_password').decode('utf-8')
#         default_user = User(email='default@example.com', password=hashed_password)
#         db.session.add(default_user)
#         db.session.commit()

@app.route('/events', methods=['GET'])
def get_events():
    # 查询数据库以获取事件列表
    events = Events.query.all()

    # 将查询到的事件列表转换为 JSON 格式
    event_list = []
    for event in events:
        event_data = {
            'id': event.id,
            'title': event.title,
            'address': event.address,
            'price': event.price,
            'thumbnail': event.thumbnail,
            'organizerName': event.organizername,
            'eventType' : event.type,
            'seatingCapacity' :event.seats,
            'duration' : event.duration,
            'startDate': event.from_time,
            'endDate': event.to_time,
            'description': event.description,
            'youtubeUrl':event.URL
        }
        #image_path = event.thumbnail
        #base64_str = image_to_base64(image_path)
        #event_data['thumbnail'] = base64_str
        event_list.append(event_data)
    #print("fanhui", event_list)
    # 使用 jsonify 函数将 JSON 格式的事件列表返回给前端
    return jsonify(event_list)

@app.route('/events/title', methods=['GET'])
def get_events_title():
    # 查询数据库以获取事件列表
    events = Events.query.all()
    # 将查询到的事件列表转换为 JSON 格式
    event_list = []
    for event in events:
        event_data = {
            # 'id': event.id,
            'title': event.title,
            # 'address': event.address,
            # 'price': event.price,
            # 'thumbnail': event.thumbnail,
            # 'organizerName': event.organizername,
            # 'eventType' : event.type,
            # 'seatingCapacity' :event.seats,
            # 'duration' : event.duration,
            # 'startDate': event.from_time,
            # 'endDate': event.to_time,
            # 'description': event.description,
            # 'youtubeUrl':event.URL
        }
        event_list.append(event_data)
    #print("fanhui", event_list)
    return jsonify(event_list)

@app.route('/listings', methods=['PUT'])
def update_events_order():
    # 查询数据库以获取事件列表s
    data = request.get_json()
    cust_e = data['email']
    date_ = data['date']
    seat_number = int(data['seat_number'])-1
    title = data['title']
    cust_id = Customer.query.filter_by(email=cust_e).first()
    event = Events_order.query.filter_by(eventtitle=title).first()
    if not event:
        return jsonify({'message': 'Event not found!'}), 404
    if not cust_id:
        return jsonify({'message': 'Customer not found!'}), 404

    cust_id.order = {event.id: date_}
    db.session.commit()

    event_d = event.orderdetails
    if date_ in event_d:
        event_d[date_][seat_number] = [1, cust_id.id]
        event.orderdetails = event_d
        db.session.commit()

        order_data = {
            'id': event.id,
            'eventtitle': event.eventtitle,
            'orderdetials': event.orderdetails
        }
        return jsonify({'message': 'Create order successfully!', 'event': order_data}), 201
    return jsonify({'message': 'Failed to update event details!'}), 400

@app.route('/events/new', methods=['POST'])
def register_event():
    data = request.get_json()
    print(data)
    #thumbnail_data = base64.b64decode(data['thumbnail'])
    #print(data)
    event_title = data['title']
    existing_event = Events.query.filter_by(title=event_title).first()
    if existing_event:
        return jsonify({'message': 'Event title already exists!'}), 400
    image_str = data['thumbnail']
    image_data = base64.b64decode(image_str.split(",")[1])

    if not os.path.exists(pic_folder):
        os.makedirs(pic_folder)
    filename = str(data['title']) + '.jpg'
    file_path = os.path.join(pic_folder, filename)
    with open(file_path, "wb") as f:
        f.write(image_data)
    seats = data['seatingCapacity']
    start_date_str = data['startDate']
    end_date_str = data['endDate']
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    print(data['startDate'])
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    seats_list = [[0, 0] for _ in range(int(data['seatingCapacity']))]
    seats_c = {}
    for i in date_list:
        seats_c[i] = seats_list

    new_order = Events_order(eventtitle=data['title'], orderdetails=seats_c)
    db.session.add(new_order)
    db.session.commit()

    new_event = Events(title=data['title'], address=data['address'], price=data['price'], thumbnail=file_path,
                       type=data['eventType'], seats=data['seatingCapacity'],
                       from_time=data['startDate'], to_time=data['endDate'], URL=data['youtubeUrl'],
                       organizername=data['organizerName'], description=data['description'])
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event created successfully!'}), 201

@app.route('/user/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    existing_host = Host.query.filter_by(email=email).first()
    if existing_host:
        return jsonify({'message': 'Host email already exists!'}), 400
    existing_cust = Customer.query.filter_by(email=email).first()
    if existing_cust:
        return jsonify({'message': 'Customer email already exists!'}), 400
    print(data)
    if 'companyName' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = Host(companyName=data['companyName'], email=data['email'], password=hashed_password)
    else:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = Customer(name=data['Name'], email=data['email'], password=hashed_password, cvc=data['cardCVC'], duedate=data['cardExpirationDate'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/user/auth/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    email = data.get('email')
    password = data.get('password')
    host = Host.query.filter_by(email=email).first()
    # hosts = Host.query.all()
    # for host in hosts:
    #     print(host)

    if not host:
        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            print('message: User not found')
            return jsonify({'message': 'User not found'}), 401
        if not bcrypt.check_password_hash(customer.password, password):
            print('message: Invalid email or password')
            return jsonify({'message': 'Invalid email or password'}), 401

        token = jwt.encode({'id': customer.id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token})
    if not bcrypt.check_password_hash(host.password, password):
        print('message: Invalid email or password')
        return jsonify({'message': 'Invalid email or password'}), 401
    #print("package token")
    #print(app.config['SECRET_KEY'])
    token = jwt.encode({'id': host.id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({'token': token})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/user/auth/logout', methods=['POST'])
def logout():
    token = request.json.get('token')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    return jsonify({'message': 'Logout successful!'}), 200

@app.route('/view_users')
def view_users():
    users = Host.query.all()
    user_list = [{'id': user.id, 'email': user.email, 'password': user.password} for user in users]
    return jsonify(user_list)

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is a protected endpoint!'})

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
        #create_default_user()
    app.run(host='127.0.0.1', port=5005, debug=True)