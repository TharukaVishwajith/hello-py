from flask import Blueprint, request, jsonify, make_response
from app.models import Post

from app import sqla

bp = Blueprint("post", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    posts = Post.query.all()
    response = make_response(
        jsonify(
            {"data": posts,
             "status": "SUCCESS"}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@bp.route("/create", methods=["POST"])
# @login_required
def create():
    try:
        request_data = request.get_json()
        post = Post(
            title=request_data["title"], body=request_data["body"])
    except ValueError as e:
        # failed validation, so flash the message to the user
        return "Failed"

    # Post was validated, so save to DB and return to index
    sqla.session.add(post)
    sqla.session.commit()
    return "Success"
