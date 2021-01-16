from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
    return "Hello, world!"

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username and user['job'] == search_job:
               subdict['users_list'].append(user)
         return subdict
      if search_username:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      if search_job:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['job'] == search_job:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      if "id" not in userToAdd:
         new_id = generate_id(userToAdd)
         userToAdd['id'] = new_id
      users['users_list'].append(userToAdd)
      resp = jsonify(success=True, user=userToAdd)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      id_to_delete = request.args.get('id')
      for i in range(len(users['users_list'])):
          user = users['users_list'][i]
          if user['id'] == id_to_delete:
              users['users_list'].pop(i)
              resp = jsonify(success=True)
              resp.status_code = 200
              return resp
              
      #resp.status_code = 200 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return jsonify(success=False)

@app.route('/users/<id>')
def get_user(id):
   if id :
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users


# Generates an id based on the 1st 4 letters of the name
# and the number of items in the userlist
def generate_id(entry):
   num = len(users['users_list'])
   max_index = min(len(entry['name']), 4)
   return entry['name'][:max_index] + str(num)