import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1

river = Blueprint('rivers', 'river')

# POST ROUTE
@river.route('/', methods=["POST"])
def create_rivers():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    river = models.RiverSystem.create(**payload)
    ## see the object
    print(river.__dict__)
    ## Look at all the methods
    print(dir(river))
    # Change the model to a dict
    print(model_to_dict(river), 'model to dict')
    river_dict = model_to_dict(river)
    return jsonify(data=river_dict, status={"code": 201, "message": "Success"})

# GET Route
@river.route('/', methods=["GET"])
def get_all_rivers():
    ## find the rivers and change each one to a dictionary into a new array
    try:
        rivers = [model_to_dict(river) for river in models.RiverSystem.select()]
        print(rivers)
        return jsonify(data=rivers, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# # create route
# @river.route('/', methods=["POST"])
# # @login_required
# def create_rivers():
#     ## see request payload anagolous to req.body in express
#     payload = request.get_json()
#     print(type(payload), 'payload')
#     payload['user'] = current_user.id
#     river = models.riverSystem.create(**payload) # this could be a session to get the user id -> use current_user
#     ## see the object
#     print(post.__dict__)
#     ## Look at all the methods
#     print(dir(post))
#     # Change the model to a dict
#     print(model_to_dict(post), 'model to dict')
#     post_dict = model_to_dict(post)
#     return jsonify(data=post_dict, status={"code": 201, "message": "Success"})

# ## update route
# @post.route('/<id>', methods=["PUT"])
# # @login_required
# def update_post(id):
#     print('UPDATINGGG')
#     print(id)
#     payload = request.get_json()
#     print(payload)
#     payload['user'] = payload['user']['id']
#     query = models.Post.update(**payload).where(models.Post.id==id)
#     print(query)
#     query.execute()
#     # print(model_to_dict(models.Post.get_by_id(id)))
#     return jsonify(data=model_to_dict(models.Post.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

# @post.route('/<id>', methods=["Delete"])
# # @login_required
# def delete_post(id):
#     query = models.Post.delete().where(models.Post.id==id)
#     print(models.Post.id)
#     query.execute()
#     return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})
