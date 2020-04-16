from flask import request, g, jsonify

from app.api import bp
from app.api.auth import token_auth
from app.api.decorators import user_role_required
from app.api.errors import bad_request
from app.models.user import UserRoles
from app.projects.aap_diagnosis.aap_diagnosis_model import AAPGynDiagnosisModel
from app.projects.aap_diagnosis.aap_gyn_diagnosis import AAPGynDiagnosis


@bp.route('/aap-gyn-diagnosis/', methods=['POST'])
@token_auth.login_required
def aap_gyn_create_diagnosis():
    """Creates diagnosis from JSON data in the request."""
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json() or {}
    else:
        data = request.form.to_dict() or {}

    model, error = AAPGynDiagnosis.predict(data, g.current_user)
    if model and not error:
        return jsonify(model), 201
    else:
        return bad_request(error)


@bp.route('/aap-gyn-diagnosis/')
@token_auth.login_required
def aap_gyn_get_diagnoses():
    """Retrieves diagnoses of a user."""
    return jsonify(AAPGynDiagnosisModel.objects().filter(
        user_id=g.current_user.id))


@bp.route('/aap-gyn-diagnosis/<doc_id>')
@token_auth.login_required
def aap_gyn_get_diagnosis_from_id(doc_id):
    """Retrieves diagnosis corresponding to the given ID."""
    example_doc = AAPGynDiagnosisModel.objects.get_or_404(
        id=doc_id, user_id=g.current_user.id)
    return jsonify(example_doc)


@bp.route('/aap-gyn-diagnosis/<doc_id>', methods=['DELETE'])
@token_auth.login_required
def aap_gyn_delete_diagnosis_from_id(doc_id):
    """Deletes diagnosis corresponding to the given ID."""
    AAPGynDiagnosisModel.objects.get_or_404(
        id=doc_id, user_id=g.current_user.id).delete()
    return jsonify({"success": True})


@bp.route('/aap-gyn-diagnosis/<doc_id>', methods=['PATCH'])
@token_auth.login_required
@user_role_required(UserRoles.EXPERT)
def aap_gyn_diagnosis_update(doc_id):
    """Updates fields of a diagnosis from the data in the request."""
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json() or {}
    else:
        data = request.form.to_dict() or {}

    model = AAPGynDiagnosisModel.objects.get_or_404(
        id=doc_id, user_id=g.current_user.id)
    model.save(data)

    return jsonify(model)
