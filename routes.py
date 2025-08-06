import string
from functools import wraps
import random
import json
from flask import Blueprint, jsonify, request
from flask_mail import Mail, Message
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from models import Host, Customer, Events, Email, Events_order, Comments, db
import jwt
from sqlalchemy.orm.attributes import flag_modified
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from flask import current_app

bp = Blueprint('routes', __name__)
mail = Mail()
# bcrypt = Bcrypt()

# Decorator to ensure that a valid token is provided in the request
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if token is provided in the request
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        # Try to decode the token with the secret key
        try:
            data = jwt.decode(token, bp.config['SECRET_KEY'])
        # If the token is invalid, return an error response
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)

    return decorated


def cust_generate_reset_token():
    # Generate a random sample of 4 characters from the ascii_letters and digits string
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return token


def cust_send_reset_email(cust, token):
    # Create a message object with the subject and recipient
    msg = Message('Reset your password', recipients=[cust.email])
    
    # Set the message body with the verification code
    msg.body = f"Your account is trying to reset the password, the verification code is:\n{token}"
    
    # Send the message using the mail object
    mail.send(msg)


def verify_reset_token(email, role, token):
    res = Email.query.filter(
        Email.email == email,
        Email.role == role,
        Email.token == token,
        Email.expires > datetime.now()
    ).first()
    return res


# @bp.route is a decorator used to define a route for the given blueprint
# the route "/user/list" is associated with the delete() function

@bp.route("/user/list")
def delete():
    want_del_id = request.args.get("delete", default=1, type=int)
    query_id = Host.query.filter_by(id=want_del_id).first()
    if not query_id:
        return "message:User not found"
    # if query_id is found, delete the record from the database
    db.session.delete(query_id)
    db.session.commit()
    return f"message: The user with id {id} was removed from the database!"


@bp.route("/user/add")
def add_user():
    # Create a new user object with the given email and password
    user1 = Host(email="刘畅", password="924082621")
    # Add the user to the database session
    db.session.add(user1)
    # Commit the changes to the database
    db.session.commit()
    # Return a success message
    return "successfull！"


@bp.route('/events', methods=['GET'])
def get_events():
    # Get all events from the database
    events = Events.query.all()
    # Get the current date
    current_date = datetime.now().date()

    event_list = []
    # Iterate through all events
    for event in events:
        # Convert the event start time and end time to dates
        event_date = datetime.strptime(event.from_time, "%Y-%m-%d").date()
        end_date = datetime.strptime(event.to_time, "%Y-%m-%d").date()
        # Calculate the difference between the current date and the event start date
        gap = event_date - current_date
        gap2 = end_date - current_date

        # Check if the event start date is within 30 days of the current date, and the event end date is after the current date
        if gap.days <= 30 and gap2.days >= 0:
            # Create a dictionary to store the event information
            event_data = {
                'id': event.id,
                'title': event.title,
                'address': event.address,
                'price': event.price,
                'thumbnail': event.thumbnail,
                'organizerName': event.organizername,
                'eventType': event.type,
                'seatingCapacity': event.seats,
                'duration': event.duration,
                'startDate': event.from_time,
                'endDate': event.to_time,
                'description': event.description,
                'youtubeUrl': event.URL
            }
            event_list.append(event_data)
    return jsonify(event_list), 201


# @bp.route('/events/search', methods=['GET'])
# def search_events():
#     # Get the event description from the request
#     event_description = request.args.get('description', '')
#     # Get the keyword from the request
#     keyword = request.args.get('keyWord', '')
#     # Get the event type from the request
#     event_type = request.args.get('eventType', '')
#     # Create a query object for the Events class
#     query = Events.query

#     events = Events.query.all()
#     # Search for events based on the description, keyword, and event type
#     if event_description:
#         query = query.filter(Events.description.ilike(f'%{event_description}%'))
#     if keyword:
#         query = query.filter(Events.keyword.ilike(f'%{keyword}%'))
#     if event_type:
#         query = query.filter(Events.event_type.ilike(f'%{event_type}%'))

#     events = query.all()
#     event_list = []

#     # Search for events based on the description, keyword, and event type
#     for event in events:
#         flag_print = 0
#         if event_type == 'all types':
#             if keyword.lower() == '':
#                 if event_description.lower() in event.description.lower():
#                     flag_print = 1
#             elif event_description.lower() == '':
#                 if keyword.lower() in event.title.lower():
#                     flag_print = 1
#             elif keyword.lower() == '' and event_description.lower() == '':
#                 flag_print = 1
#             else:
#                 if keyword.lower() in event.title.lower() and event_description.lower() in event.description.lower():
#                     flag_print = 1
#         else:
#             if event_description.lower() == '' and event_type.lower() == '' and keyword.lower() == '':
#                 return jsonify([]), 200
#             elif keyword.lower() == '':
#                 if event_description.lower() in event.description.lower() and event_type.lower() in event.type.lower():
#                     flag_print = 1
#             elif event_description.lower() == '':
#                 if keyword.lower() in event.title.lower() and event_type.lower() in event.type.lower():
#                     flag_print = 1
#             elif event_type.lower() == '':
#                 if keyword.lower() in event.title.lower() and event_description.lower() in event.description.lower():
#                     flag_print = 1
#             elif keyword.lower() == '' and event_description.lower() == '':
#                 if event_type.lower() in event.type.lower():
#                     flag_print = 1
#             elif keyword.lower() == '' and event_type.lower() == '':
#                 if event_description.lower() in event.description.lower():
#                     flag_print = 1
#             elif event_description.lower() == '' and event_type.lower() == '':
#                 if keyword.lower() in event.title.lower():
#                     flag_print = 1
#             else:
#                 if keyword.lower() in event.title.lower() and event_description.lower() in event.description.lower() and event_type.lower() in event.type.lower():
#                     flag_print = 1
                    
#         if flag_print == 1:
#             # Create a dictionary called event_data containing the event information
#             event_data = {
#                 'id': event.id,
#                 'title': event.title,
#                 'address': event.address,
#                 'price': event.price,
#                 'thumbnail': event.thumbnail,
#                 'organizerName': event.organizername,
#                 'eventType': event.type,
#                 'seatingCapacity': event.seats,
#                 'duration': event.duration,
#                 'startDate': event.from_time,
#                 'endDate': event.to_time,
#                 'description': event.description,
#                 'youtubeUrl': event.URL
#             }
#             event_list.append(event_data)
#     return jsonify(event_list), 200

@bp.route('/events/search', methods=['GET'])
def search_events():
    # Get search parameters from the query string
    event_description = request.args.get('description', '').strip().lower()
    keyword = request.args.get('keyWord', '').strip().lower()
    event_type = request.args.get('eventType', '').strip().lower()

    # Start a query
    query = Events.query

    # Filter by event type (unless it’s 'all types' or empty)
    if event_type and event_type != 'all types':
        query = query.filter(Events.type.ilike(f'%{event_type}%'))

    # Filter by keyword in title
    if keyword:
        query = query.filter(Events.title.ilike(f'%{keyword}%'))

    # Filter by description
    if event_description:
        query = query.filter(Events.description.ilike(f'%{event_description}%'))

    try:
        events = query.all()
        results = []
        for event in events:
            event_data = {
                'id': event.id,
                'title': event.title,
                'address': event.address,
                'price': event.price,
                'thumbnail': event.thumbnail,
                'organizerName': event.organizername,
                'eventType': event.type,  # 👈 使用 event.type 因为你的字段叫 type
                'seatingCapacity': event.seats,
                'duration': event.duration,
                'startDate': event.from_time,
                'endDate': event.to_time,
                'description': event.description,
                'youtubeUrl': event.URL
            }
            results.append(event_data)

        return jsonify(results), 200

    except Exception as e:
        print("Error during event search:", e)
        return jsonify({"message": "Internal server error"}), 500

# return events titles
@bp.route('/events/title', methods=['GET'])
def get_events_title():
    events = Events.query.all()
    event_list = []
    for event in events:
        event_data = {
            'title': event.title,
        }
        event_list.append(event_data)
    return jsonify(event_list)

# return hosted events
@bp.route('/events/host/<int:userId>', methods=['GET'])
def get_host_events(userId):
    events = Events.query.filter_by(hostId=userId)
    event_list = []
    for event in events:
        event_data = {
            'id': event.id,
            'hostId': event.hostId,
            'title': event.title,
            'address': event.address,
            'price': event.price,
            'organizerName': event.organizername,
            'eventType': event.type,
            'seatingCapacity': event.seats,
            'duration': event.duration,
            'startDate': event.from_time,
            'endDate': event.to_time,
            'description': event.description,
            'youtubeUrl': event.URL,
            'thumbnail': event.thumbnail
        }
        event_list.append(event_data)
    return jsonify(event_list)

# return specifical event
@bp.route('/events/<int:eventId>', methods=['GET'])
def get_events_details(eventId):
    event = Events.query.filter_by(id=eventId).first()
    event_order = Events_order.query.filter_by(id=eventId).first()
    if not event_order or not event:
        return jsonify({'message': 'Event not found!!!!!'}), 404
    event_data = {
        'id': event.id,
        'title': event.title,
        'address': event.address,
        'price': event.price,
        'thumbnail': event.thumbnail,
        'organizerName': event.organizername,
        'eventType': event.type,
        'seatingCapacity': event.seats,
        'duration': event.duration,
        'startDate': event.from_time,
        'endDate': event.to_time,
        'description': event.description,
        'youtubeUrl': event.URL,
        'orderdetails': event_order.orderdetails
    }
    return jsonify(event_data)

# customer booking function
@bp.route('/bookings', methods=['PUT'])
def update_events_bookings():
    data = request.get_json()
    cust_id = data['userId']
    date_ = data['Date']
    seat_number = data['seat']
    eventid = data['eventId']
    cust = Customer.query.filter_by(id=cust_id).first()
    event = Events_order.query.filter_by(id=eventid).first()
    events = Events.query.filter_by(id=eventid).first()
    # if exist event
    if not event:
        return jsonify({'message': 'Event not found!'}), 404
    # if exist customer
    if not cust:
        return jsonify({'message': 'Customer not found!'}), 405
    # initialization customer feature
    if cust.order is None:
        cust.order = {}
    price = events.price * len(seat_number)
    # if enough money
    if cust.wallet < price:
        return jsonify({'message': 'You do not have enough money!'}), 401
    flag = 0
    s = 0
    # check if seat is available
    for i in seat_number:
        if event.orderdetails[date_][int(i)][0] == 1:
            flag = 1
            s = int(i) + 1
            break
    if flag == 1:
        return jsonify({'message': f'Seats {s} are not available!'}), 402
    # update customer wallet
    if str(event.id) in cust.order:
        if date_ in cust.order[str(event.id)]:
            pass
        else:
            cust.order[str(event.id)].append(date_)
    else:
        cust.order[event.id] = [date_]
    flag_modified(cust, "order")
    db.session.commit()
    # update event details
    event_d = event.orderdetails
    if date_ in event_d:
        for i in seat_number:
            event_d[date_][i] = [1, cust_id]
            cust.wallet -= events.price
            event.orderdetails = event_d
        flag_modified(event, "orderdetails")
        db.session.commit()
        order_data = {
            'id': event.id,
            'eventtitle': event.eventtitle,
            'orderdetails': event.orderdetails
        }
        
        # send email to customer
        for i in range(len(seat_number)):
            seat_number[i] += 1

        events_json = {
            'title': events.title,
            'type': events.type,
            'address': events.address,
            'price': events.price,
            'seats': seat_number,
            'organizerName': events.organizername,
            'date': data['Date'],
            'description': events.description
        }
        events_html = render_template('mail_booking.html', events_json=events_json)
        message = Message(subject="Booking Successfully!", recipients=[cust.email])
        message.html = events_html

        mail.send(message)
        return jsonify({'message': 'Create order successfully!', 'event': order_data}), 201
    return jsonify({'message': 'Failed to update event details!'}), 400

# recommendation system
@bp.route('/bookings/<int:userId>/recommendation', methods=['GET'])
def get_recommendation(userId):
    current_app.logger.info(f"Fetching recommendations for user: {userId}")
    cust = Customer.query.filter_by(id=int(userId)).first()
    user_events_ids = list(cust.order.keys())
    event_type_frequency = defaultdict(int)

    # If the user has booked events, calculate the frequency of event types
    if user_events_ids:
        for event_id in user_events_ids:
            event = Events.query.get(event_id)
            if event:
                event_type_frequency[event.type] += 1
        favorite_event_type = max(event_type_frequency, key=event_type_frequency.get)

        recommended_events = Events.query.filter(
            Events.type == favorite_event_type,
            Events.id.notin_(user_events_ids),
            Events.from_time > datetime.now()
        ).order_by(Events.from_time).limit(6).all()

        # If no recommended events are found, return all upcoming events
        if not recommended_events:
            current_app.logger.info(f"No recommended events found for favorite type '{favorite_event_type}' for user: {userId}")
            return jsonify([])
    else:
        recommended_events = Events.query.filter(
            Events.id.notin_(user_events_ids),
            Events.from_time > datetime.now()
        ).order_by(Events.from_time).limit(3).all()
        if not recommended_events:
            current_app.logger.info(f"No upcoming events to recommend for new or inactive user: {userId}")
            return jsonify([])

    events_json = [{
        'id': event.id,
        'title': event.title,
        'type': event.type,
        'description': event.description,
        'address': event.address,
        'price': event.price,
        'thumbnail': event.thumbnail,
        'organizerName': event.organizername,
        'eventType': event.type,
        'seatingCapacity': event.seats,
        'duration': event.duration,
        'startDate': event.from_time,
        'endDate': event.to_time,
        'youtubeUrl': event.URL
    } for event in recommended_events]
    return jsonify(events_json)


# show my booking page
@bp.route('/bookings/<int:userId>', methods=['GET'])
def get_bookings(userId):
    cust = Customer.query.filter_by(id=userId).first()
    events_list = []

    # if user has no bookings
    if cust.order is None or len(cust.order) == 0:
        return jsonify({'message': 'No events found!'}), 404
    # if user has bookings, return all tickets
    for k, v in cust.order.items():
        event_order = Events_order.query.filter_by(id=int(k)).first()
        events = Events.query.filter_by(id=int(k)).first()
        for i in v:
            orderdetails = event_order.orderdetails[i]
            seat_list = []
            for j in range(len(orderdetails)):
                seat_number = j+1
                if orderdetails[j][1] == str(userId):
                    seat_list.append(j)
                    event1 = {
                        'eventId': event_order.id,
                        'userId': cust.id,
                        'eventtitle': event_order.eventtitle,
                        'thumbnail': events.thumbnail,
                        'description': events.description,
                        'date': i,
                        'seat': seat_number
                    }
                    events_list.append(event1)
    return jsonify(events_list), 200


# cancel booking
@bp.route('/bookings/cancel/<int:userId>', methods=['PUT'])
def cancel_bookings(userId):
    data = request.get_json()
    seat = data['seat'] - 1
    cust = Customer.query.filter_by(id=int(userId)).first()
    events = Events.query.filter_by(id=int(data['eventId'])).first()
    event_id = str(data['eventId'])
    # if event is found in customer's order
    if event_id in cust.order:
        price = events.price
        event_order = Events_order.query.filter_by(id=int(data['eventId'])).first()
        # print(int(event_order.orderdetails[data['Date']][seat][1]), int(data['userId']))

        # if seat is booked by the customer
        if int(event_order.orderdetails[data['Date']][seat][1]) == int(data['userId']):

            event_order.orderdetails[data['Date']][seat] = [0, 0]
            flag_modified(event_order, "orderdetails")
        flag = 0
        
        # check if the customer has booked the event before
        for i in range(len(event_order.orderdetails[data['Date']])):
            if int(event_order.orderdetails[data['Date']][i][1]) == int(data['userId']):
                flag = 1
        if flag == 0:
            # delete the event from the customer's order
            if len(cust.order[event_id]) == 1:
                del cust.order[event_id]
                flag_modified(cust, "order")
            else:
                cust.order[event_id].remove(data['Date'])
                flag_modified(cust, "order")
        # refund
        cust.wallet += price
        flag_modified(cust, "wallet")
        seat_number = seat + 1
        events_json = {
            'title': events.title,
            'type': events.type,
            'address': events.address,
            'price': events.price,
            'seats': seat_number,
            'organizerName': events.organizername,
            'date': data['Date'],
            'description': events.description
        }

        # send email to the customer
        events_html = render_template('mail_cancel_booking.html', events_json=events_json)
        message = Message(subject="Your Booking has been canceled successfully!", recipients=[cust.email])
        message.html = events_html
        mail.send(message)
        db.session.commit()
        return jsonify({'message': 'Refund successfully!'}), 201
    else:
        return jsonify({'message': 'Event not Found!!!'}), 400


# host cancel event
@bp.route('/bookings/cancel_event/<int:userId>', methods=['PUT'])
def cancel_events(userId):
    data = request.get_json()
    event_order = Events_order.query.filter_by(id=data['eventId']).first()
    event = Events.query.filter_by(id=data['eventId']).first()
    comment = Comments.query.filter_by(eventId=data['eventId']).first()
    user_list = defaultdict(int)
    events = Events.query.filter_by(id=int(data['eventId'])).first()
    price = events.price

    seat_list = {}
    # get all the seats that have been booked
    for k, v in event_order.orderdetails.items():
        for i in range(len(v)):
            if v[i][0] == 1:
                user_list[v[i][1]] += 1
                if v[i][1] in seat_list:
                    seat_list[v[i][1]].append(i)
                else:
                    seat_list[v[i][1]] = [i]
 
    # refund
    for i, j in user_list.items():
        user = Customer.query.filter_by(id=int(i)).first()
        user.wallet += price * (int(j))
        del user.order[str(data['eventId'])]
        flag_modified(user, "order")
        flag_modified(user, "wallet")
        db.session.commit()
        events_json = {
            'title': event.title,
            'type': event.type,
            'address': event.address,
            'price': event.price,
            'organizerName': event.organizername,
            'startDate': event.from_time,
            'endDate': event.to_time,
            'description': event.description
        }

        # send email to the customer
        events_html = render_template('mail_cancel_event.html', events_json=events_json)
        message = Message(subject="Host has Canceled Your Booking!", recipients=[user.email])
        message.html = events_html
        mail.send(message)
    db.session.delete(event)
    db.session.delete(event_order)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Event has been canceled!'}), 201

# customer comments(authentication)
@bp.route('/comments/customer', methods=['POST'])
def if_order():
    data = request.get_json()
    cust = Customer.query.filter_by(id=data['customerId']).first()

    # if customer has not ordered this event
    if str(data['eventId']) not in cust.order:
        return jsonify({'message': 'You did not order this event!'}), 404
    else:
        comment = Comments.query.filter_by(eventId=data['eventId']).first()
        if str(data['customerId']) in comment.comment:
            return jsonify({'message': 'You already commented this event!'}), 401
        else:
            return jsonify({'message': 'You can fill your review now!'}), 201


# customer comments
@bp.route('/comments/customer', methods=['PUT'])
def cust_comments():
    data = request.get_json()
    cust = Customer.query.filter_by(id=data['userId']).first()
    c = [data['Date'], data['review'], cust.name, 'None', 'None', 'None', 'None']
    comment = Comments.query.filter_by(eventId=int(data['eventId'])).first_or_404()
    comment.comment[data['userId']] = c
    flag_modified(comment, "comment")
    db.session.commit()
    return jsonify({'message': 'Add comment successfully!'}), 201

# show comments
@bp.route('/comments/<int:eventId>', methods=['GET'])
def get_comments(eventId):
    comments = Comments.query.filter_by(eventId=eventId).first_or_404()
    return jsonify(comments.comment), 201

# host comments(authentication)
@bp.route('/comments/host', methods=['POST'])
def if_host():
    data = request.get_json()
    event = Events.query.filter_by(id=int(data['eventId'])).first_or_404()
    comment = Comments.query.filter_by(eventId=int(data['eventId'])).first_or_404()
    if event.hostId == int(data['hostId']):
        if comment.comment[data['userId']][5] == data['hostId']:
            return jsonify({'message': 'You have already replied this comment!'}), 401
        else:
            return jsonify({'message': 'Reply your review!'}), 201
    else:
        return jsonify({'message': 'You did not host this event!'}), 400

# host comments
@bp.route('/comments/host', methods=['PUT'])
def host_comments():
    data = request.get_json()
    host = Host.query.filter_by(id=int(data['hostId'])).first_or_404()
    comment = Comments.query.filter_by(eventId=int(data['eventId'])).first_or_404()
    comment.comment[data['userId']][3] = data['Date']
    comment.comment[data['userId']][4] = data['review']
    comment.comment[data['userId']][5] = data['hostId']
    comment.comment[data['userId']][6] = host.companyName
    flag_modified(comment, "comment")
    db.session.commit()
    return jsonify({'message': 'Add comment successfully!'}), 201

# create new event
@bp.route('/events/new', methods=['POST'])
def register_event():
    data = request.get_json()
    event_title = data['title']
    existing_event = Events.query.filter_by(title=event_title).first()
    # check if event title already exists
    if existing_event:
        return jsonify({'message': 'Event title already exists!'}), 400
    image_str = data['thumbnail']
    seats = data['seatingCapacity']
    start_date_str = data['startDate']
    end_date_str = data['endDate']
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    date_list = []
    current_date = start_date
    # generate a list of dates between start_date and end_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    seats_list = [[0, 0] for _ in range(int(data['seatingCapacity']))]
    seats_c = {}
    # assign seats to each date
    for i in date_list:
        seats_c[i] = seats_list

    new_order = Events_order(eventtitle=data['title'], orderdetails=seats_c)
    db.session.add(new_order)
    db.session.commit()
    new_comment = Comments(eventId=new_order.id, comment={})
    db.session.add(new_comment)
    db.session.commit()

    # create a new event
    new_event = Events(hostId=data['hostId'], title=data['title'], address=data['address'], price=data['price'],
                       thumbnail=image_str,
                       type=data['eventType'], seats=data['seatingCapacity'],
                       from_time=data['startDate'], to_time=data['endDate'], URL=data['youtubeUrl'],
                       organizername=data['organizerName'], description=data['description'])
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event created successfully!'}), 201

# host register
@bp.route('/user/auth/host_register', methods=['POST'])
def host_register():
    data = request.get_json()
    email = data['email']
    existing_host = Host.query.filter_by(email=email).first()
    # check if email already exists
    if existing_host:
        return jsonify({'message': 'Host email already exists!'}), 400
    existing_cust = Customer.query.filter_by(email=email).first()
    if existing_cust:
        return jsonify({'message': 'Customer email already exists!'}), 401
    # hash the password
    hashed_password = generate_password_hash(data['password'])
    new_user = Host(companyName=data['companyName'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

# customer register
@bp.route('/user/auth/customer_register', methods=['POST'])
def cust_register():
    data = request.get_json()
    email = data['email']
    existing_cust = Customer.query.filter_by(email=email).first()
    # check if email already exists
    if existing_cust:
        return jsonify({'message': 'Customer email already exists!'}), 400
    existing_host = Host.query.filter_by(email=email).first()
    if existing_host:
        return jsonify({'message': 'Host email already exists!'}), 401
    # hash the password
    hashed_password = generate_password_hash(data['password'])
    new_user = Customer(name=data['Name'], email=data['email'], password=hashed_password, cvc=data['cardCVC'],
                        duedate=data['cardExpirationDate'], wallet=0, cardNumber=data['cardNumber'], order={})
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201


@bp.route('/user/auth/customer', methods=['GET'])
def get_customer():
    user_id = request.args.get('userId')
    user_id = int(user_id) if user_id is not None else None
    cust = Customer.query.filter_by(id=user_id).first()
    
    # if no customer found for the given user_id, return a 404 error
    if cust is None:
        print('No customer found for UserID:', user_id)
        return jsonify({'error': 'Customer not found'}), 404

    cust_detail = {
        'id': cust.id,
        'email': cust.email,
        'name': cust.name,
        'duedate': cust.duedate,
        'wallet': cust.wallet,
        'cardNumber': cust.cardNumber
    }
    return jsonify(cust_detail)

# customer recharge
@bp.route('/user/auth/customer/recharge', methods=['PUT'])
def top_up():
    data = request.get_json()
    user_id = data['userId']
    amount = data['amount']
    cust = Customer.query.filter_by(id=user_id).first()
    # rechange wallet
    cust.wallet += int(amount)
    flag_modified(cust, "wallet")
    db.session.commit()
    amount = cust.wallet
    return jsonify(amount), 201

# login function
@bp.route('/user/auth/login', methods=['POST'])
def login():
    data = request.json
    identity = data['identity']
    email = data.get('email')
    password = data.get('password')
    # check if host
    if identity == 'host':
        # host login
        host = Host.query.filter_by(email=email).first()
        if not host:
            customer = Customer.query.filter_by(email=email).first()
            if not customer:
                return jsonify({'message': 'User not found'}), 401
            else:
                return jsonify({'message': 'Please login customer!'}), 402
        else:
            # check if password is correct
            if not check_password_hash(host.password, password):
                return jsonify({'message': 'Invalid email or password'}), 403
            token = jwt.encode({'id': host.id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)},
                               current_app.config['SECRET_KEY'])
            return jsonify({'token': token, 'id': host.id})
    else:
        # customer login
        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            host = Host.query.filter_by(email=email).first()
            if not host:
                return jsonify({'message': 'User not found'}), 404
            else:
                return jsonify({'message': 'Please login host!'}), 405
        else:
            # check if password is correct
            if not check_password_hash(customer.password, password):
                return jsonify({'message': 'Invalid email or password'}), 406
            token = jwt.encode({'id': customer.id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)},
                               current_app.config['SECRET_KEY'])
            return jsonify({'token': token, 'id': customer.id})

# logout function
@bp.route('/user/auth/logout', methods=['POST'])
def logout():
    token = request.json.get('token')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    return jsonify({'message': 'Logout successful!'}), 200



# def view_users() is the function that will be executed when this route is accessed

@bp.route('/view_users')
def view_users():
    users = Host.query.all()
    # List comprehensions are used to create a list of dictionaries containing user information
    user_list = [{'id': user.id, 'email': user.email, 'password': user.password} for user in users]
    return jsonify(user_list)


# @token_required is a decorator used to ensure that the user is authenticated and authorized to access this protected endpoint
# def protected() returns a json object with a message indicating that this is a protected endpoint and returns the status code 200

@bp.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is a protected endpoint!'})


@bp.route('/user/auth/send_email', methods=['GET', 'POST'])
def send_email():
    # Get the role and email from the request
    role = request.json.get('role')
    email = request.json.get('email')
    
    # Check if the role is valid
    if role == 'Host':
        user = Host.query.filter_by(email=email).first()
    elif role == 'Customer':
        user = Customer.query.filter_by(email=email).first()
    else:
        return jsonify({'message': 'Invalid role. Role must be either "Host" or "Customer".'}), 400
    
    # If no user is found, return a 404 error
    if user is None:
        return jsonify({'message': f'No {role} found with the provided email address.'}), 404

    # If the user is found, generate a reset token and send the reset email
    if user:
        token = cust_generate_reset_token()
        cust_send_reset_email(user, token)

        # Set the expire time for the token
        expire_time = datetime.now() + timedelta(minutes=2)
        new_email = Email(email=email, role=role, token=token, expires=expire_time)
        db.session.add(new_email)
        db.session.commit()

        response = {'message': 'Reset email sent, please check your email.'}
        return jsonify(response), 200
    else:
        response = {'message': 'Invalid email.'}
        return jsonify(response), 404


@bp.route('/user/auth/check_token', methods=['GET', 'POST'])
def check_token():
    email = request.json.get('email')
    role = request.json.get('role')
    token = request.json.get('token')

    current_app.logger.info("Validating token: %s", token)

    email_code = verify_reset_token(email, role, token)

    # if the email_code is None, return an error message and a 404 status code
    if not email_code:
        return jsonify({'message': 'Invalid email or verify code expired.'}), 404

    current_app.logger.info("Token info: %s", email_code.token)

    # if the token does not match the email_code, return an error message and a 404 status code
    if email_code.token != token:
        response = {'message': 'Invalid or expired verify code'}
        return jsonify(response), 404

    # if the token is valid, return a success message and a 200 status code
    response = {'message': 'Verification successfully'}
    return jsonify(response), 200


@bp.route('/user/auth/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.json.get('email')
    role = request.json.get('role')
    token = request.json.get('token')
    current_app.logger.info("Validating token: %s", token)
    email_code = verify_reset_token(email, role, token)

    # if the email_code is None, return an error message and a 404 status code
    if not email_code:
        return jsonify({'message': 'Your verify code is expired.'}), 404
    
    # if the token does not match the email_code, return an error message and a 404 status code
    if email_code.token != token:
        response = {'message': 'Invalid or expired verify code'}
        return jsonify(response), 404

    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')

    # if the password and confirm_password are not matched, return an error message and a 404 status code
    if password != confirm_password:
        response = {'message': 'Password and confirm password are not matched'}
        return jsonify(response), 404

    # if the user is not found, return an error message and a 404 status code
    if role == 'Customer':
        user = Customer.query.filter_by(email=email).first()
    elif role == 'Host':
        user = Host.query.filter_by(email=email).first()
    else:
        return jsonify({'message': 'Invalid role.'}), 404
    
    user.password = generate_password_hash(password)
    db.session.commit()
    response = {'message': 'User password set successfully'}
    return jsonify(response), 200
