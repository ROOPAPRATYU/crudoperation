from flask import Flask, request, json
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_restful import Api, Resource

app = Flask(__name__)
# Configuration for MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/roopa'
# Create PyMongo app
mongo = PyMongo(app)
# Collection create
collection = mongo.db.userinfo
# Collection to store counters for id
counter_collection = mongo.db.counters
# Create API
api = Api(app)

class UsersResource(Resource):
    def get(self):
        try:
            users = list(collection.find({}, {'_id': 0}))
            # Convert ObjectId to string for each user
            for user in users:
                user['id'] = str(user['id'])
            return json.dumps(users)
        except Exception as e:
            return {'error': str(e)}, 500

    def post(self):
        try:
            user_data = request.get_json()
            if 'name' in user_data and 'email' in user_data and 'password' in user_data:
                counter = counter_collection.find_one_and_update(
                    {'_id': 'user_counter'},
                    {'$inc': {'seq': 1}},
                    upsert=True
                )
                if counter is None:
                    return {'error': 'Failed to retrieve counter'}, 500

                user = {
                    'id': counter['seq'],
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'password': user_data['password']
                }
                result = collection.insert_one(user)
                if result.inserted_id:
                    return {'message': 'User created successfully', 'id': user['id']}, 201
                else:
                    return {'error': 'Failed to create user'}, 500
            else:
                return {'error': 'Name, email, and password are required'}, 400
        except Exception as e:
            return {'error': str(e)}, 500

class UserResource(Resource):
    def get(self, user_id):
        try:
            if user_id.isdigit():
                user = collection.find_one({'id': int(user_id)}, {'_id': 0})
            else:
                user = collection.find_one({'id': user_id}, {'_id': 0})

            if user:
                return user
            else:
                return {'error': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    def put(self, user_id):
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
                    return {'message': 'User updated successfully'}
                else:
                    return {'error': 'User not found'}, 404
            else:
                return {'error': 'At least one field (name, email, or password) is required'}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    def delete(self, user_id):
        try:
            if user_id.isdigit():
                user_id = int(user_id)

            result = collection.delete_one({'id': user_id})
            if result.deleted_count > 0:
                return {'message': 'User deleted successfully'}
            else:
                return {'error': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

# Add resources to the API
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
