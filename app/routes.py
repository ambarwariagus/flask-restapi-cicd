from flask_restx import Namespace, Resource, fields

from app.auth import require_api_key
from app.models import create_user, delete_user, get_all_users, get_user_by_id, update_user

ns = Namespace("users", description="User CRUD operations")

user_model = ns.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description="User ID"),
        "username": fields.String(required=True, description="Username", min_length=3, max_length=50),
        "email": fields.String(required=True, description="Email address"),
        "full_name": fields.String(required=True, description="Full name", min_length=1, max_length=100),
        "created_at": fields.String(readonly=True, description="Creation timestamp"),
    },
)

user_input = ns.model(
    "UserInput",
    {
        "username": fields.String(required=True, description="Username", min_length=3, max_length=50),
        "email": fields.String(required=True, description="Email address"),
        "full_name": fields.String(required=True, description="Full name", min_length=1, max_length=100),
    },
)


def validate_email(email):
    return isinstance(email, str) and "@" in email and "." in email.split("@")[-1]


@ns.route("/")
class UserList(Resource):
    @ns.doc("list_users")
    @ns.marshal_list_with(user_model)
    def get(self):
        """List semua users"""
        return get_all_users()

    @ns.doc("create_user", security="apikey")
    @ns.expect(user_input, validate=True)
    @ns.marshal_with(user_model, code=201)
    @ns.response(400, "Validation error")
    @ns.response(401, "Unauthorized")
    @ns.response(409, "User already exists")
    @require_api_key
    def post(self):
        """Buat user baru"""
        data = ns.payload

        if not validate_email(data.get("email", "")):
            ns.abort(400, "Format email tidak valid")

        try:
            user = create_user(data["username"], data["email"], data["full_name"])
        except Exception:
            ns.abort(409, "Username atau email sudah terdaftar")

        return user, 201


@ns.route("/<int:user_id>")
@ns.param("user_id", "User ID")
@ns.response(404, "User not found")
class UserDetail(Resource):
    @ns.doc("get_user")
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get user by ID"""
        user = get_user_by_id(user_id)
        if not user:
            ns.abort(404, "User tidak ditemukan")
        return user

    @ns.doc("update_user", security="apikey")
    @ns.expect(user_input, validate=True)
    @ns.marshal_with(user_model)
    @ns.response(401, "Unauthorized")
    @ns.response(409, "Conflict")
    @require_api_key
    def put(self, user_id):
        """Update user"""
        user = get_user_by_id(user_id)
        if not user:
            ns.abort(404, "User tidak ditemukan")

        data = ns.payload

        if not validate_email(data.get("email", "")):
            ns.abort(400, "Format email tidak valid")

        try:
            updated = update_user(user_id, data["username"], data["email"], data["full_name"])
        except Exception:
            ns.abort(409, "Username atau email sudah dipakai user lain")

        return updated

    @ns.doc("delete_user", security="apikey")
    @ns.response(204, "User deleted")
    @ns.response(401, "Unauthorized")
    @require_api_key
    def delete(self, user_id):
        """Hapus user"""
        user = get_user_by_id(user_id)
        if not user:
            ns.abort(404, "User tidak ditemukan")
        delete_user(user_id)
        return "", 204
