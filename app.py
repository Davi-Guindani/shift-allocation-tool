from flask import Flask, request, jsonify
from models.schedule_request import WorkerScheduleRequest
from services.schedule_service import generate_schedule

app = Flask(__name__)

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.json
    try:
        request_data = WorkerScheduleRequest.from_dict(data)
        solutions = generate_schedule(request_data)
        return jsonify({"solutions": solutions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)