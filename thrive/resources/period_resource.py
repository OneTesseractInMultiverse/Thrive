import uuid
from flask import jsonify, request
from thrive import app
from thrive.models.graph import Period
from thrive.models.transactions import spawn_periods_for_year

# --------------------------------------------------------------------------
# POST GROUP
# --------------------------------------------------------------------------
@app.route('/api/v1/period', methods=['POST'])
def post_period():
    
    # First we verify the request is an actual json request. If not, then we
    # responded with a HTTP 400 Bad Request result code.
    if not request.is_json:
        app.logger.warning('Request without JSON payload received on token endpoint')
        return jsonify({"msg": "Only JSON request is supported"}), 400
        
    # If we get here, is because the request contains valid json so we can
    # parse the parameters
    period_data = request.get_json()
    
    if 'year' not in period_data or 'denominator' not in period_data:
        return jsonify({
            "msg": "Year is not present in payload"
        }), 400
    
    year = int(period_data['year'])
    denominator = int(period_data['denominator'])
    if spawn_periods_for_year(year=year, denominator=denominator):
        return jsonify({
            "msg": "Periods spawned successfully for year: " + str(year)
        }), 201
    return jsonify({
        "msg": "Unable to spawn periods for provided year"
    }), 500
    