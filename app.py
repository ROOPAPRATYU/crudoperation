from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
#configuration for monodb
app.config['MONGO_URI'] = 'mongodb://localhost:27017/roopa'
#create PyMongo app
mongo = PyMongo(app)
#collection create
collection = mongo.db.userinfo
# Collection to store counters for id
counter_collection = mongo.db.counters  

#Endpoint For Get all user info
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = list(collection.find({}, {'_id': 0}))
        # Convert ObjectId to string for each user
        for user in users:
            user['id'] = str(user['id'])
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint to Get User Info With help of Id
    
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        if user_id.isdigit():
            user = collection.find_one({'id': int(user_id)}, {'_id': 0})
        else:
            user = collection.find_one({'id': user_id}, {'_id': 0})

        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#create new User Endpoint

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        if 'name' in user_data and 'email' in user_data and 'password' in user_data:
            counter = counter_collection.find_one_and_update(
                {'_id': 'user_counter'},
                {'$inc': {'seq': 1}},
                upsert=True
            )
            if counter is None:
                return jsonify({'error': 'Failed to retrieve counter'}), 500

            user = {
                'id': counter['seq'],
                'name': user_data['name'],
                'email': user_data['email'],
                'password': user_data['password']
            }
            result = collection.insert_one(user)
            if result.inserted_id:
                return jsonify({'message': 'User created successfully', 'id': user['id']}), 201
            else:
                return jsonify({'error': 'Failed to create user'}), 500
        else:
            return jsonify({'error': 'Name, email, and password are required'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#delete user with the help of id endpoint
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if user_id.isdigit():
            user_id = int(user_id)

        result = collection.delete_one({'id': user_id})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Update the already existing user with the help of id
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.get_json()
        if 'name' in user_data or 'email' in user_data or 'password' in user_data:
            if user_id.isdigit():
                user_id = int(user_id)

            updated_user = {}

            if 'name' in user_data:
                updated_user['name'] = user_data['name']
            if 'email' in user_data:
                updated_user['email'] = user_data['email']
            if 'password' in user_data:
                updated_user['password'] = user_data['password']

            result = collection.update_one({'id': user_id}, {'$set': updated_user})
            if result.modified_count > 0:
                return jsonify({'message': 'User updated successfully'})
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'At least one field (name, email, or password) is required'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
