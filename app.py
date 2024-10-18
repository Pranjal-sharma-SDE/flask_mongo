from flask import Flask,request,jsonify
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

uri = os.getenv('MONGO_URI')

app = Flask(__name__)



# Create a new client and connect to the server
client = MongoClient(uri)

# Select the database and collection
db = client['user_database']  # Replace 'user_database' with your DB name
users_collection = db['users']  # Replace 'users' with your collection name


# Ping the server to check if it's running
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'test'

# dynamic route

# @app.route('/test2', defaults={'username': None})
# @app.route('/test2/', defaults={'username': None})     got error for guest if doing without this . tell the reason.
@app.route('/test2/<username>')
def test2(username:str = None)->str:    # type hinting
    if username is None:
        return 'Hello, Guest!'
    return 'Hello, ' + username


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    username = data['username']
    password = data['password']
    email = data['email']

    if username is None or password is None or email is None:
        return jsonify({'error': 'Username or password or email is missing'}), 400

    users_collection.insert_one({'username': username, 'password': password, 'email': email})

    return jsonify({'message': 'User added successfully'})


@app.route('/get_users')
def get_users():
    users_list = list(users_collection.find({}, {'_id': 0}))  # Exclude the '_id' field
    return jsonify(users_list), 200


# @app.route('/get_users', methods=['GET'])
# def get_users():
#     users = users_collection.find()

#     users_list = []
#     for user in users:
#         print(user)
#         users_list.append(user)
#     # print(users)
#     # users_list = []
#     # for user in users:
#     #     users_list.append(user)
#     return jsonify(users_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


