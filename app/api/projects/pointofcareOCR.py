from flask import request, g, jsonify

from app.api import bp
from app.api.auth import token_auth
from app.projects.pointofcare_ocr.pointofcare_model import POC_OCR_Model


@bp.route('/pocresult', methods=['POST'])
@token_auth.login_required
def pocResult():
    """Creates record of Blood pressure results from JSON data in the request."""
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json() or {}
    else:
        data = request.form.to_dict() or {}

    time = data.get('time')
    systolic = data.get('systolic')
    diastolic = data.get('diastolic')
    heartRate = data.get('heartRate')

    model = POC_OCR_Model(user_id=g.current_user.id, time=time, systolic=systolic, diastolic=diastolic,
                          heartRate=heartRate)
    model.save()

    return jsonify(model), 201


@bp.route('/pocresult')
@token_auth.login_required
def getPocRecords():
    """Retrieves records of a user."""
    return jsonify(POC_OCR_Model.objects().filter(
        user_id=g.current_user.id))


@bp.route('/pocresult/<doc_id>', methods=['DELETE'])
@token_auth.login_required
def poc_delete_from_id(doc_id):
    """Deletes records corresponding to the given ID."""
    POC_OCR_Model.objects.get_or_404(
        id=doc_id, user_id=g.current_user.id).delete()
    return jsonify({"success": True})
