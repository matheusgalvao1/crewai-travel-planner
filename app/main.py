from flask import Flask, render_template, request, jsonify
from travel_planner.travel_planner_crew import TravelPlannerCrew

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan_trip():
    try:
        # Get form data
        city = request.form.get('city')
        days = int(request.form.get('days'))
        num_attractions = int(request.form.get('num_attractions'))

        # Create the crew and run it
        try:
            travel_crew = TravelPlannerCrew()
            result = travel_crew.travel_crew().kickoff(inputs={
                "city": city,
                "days": days,
                "num_attractions": num_attractions
            })
        except Exception as e:
            return jsonify({"error": f"Error generating travel plan: {str(e)}"}), 500

        # Return the pydantic output in JSON format
        if result.pydantic:
            return jsonify(result.pydantic.model_dump())
        return jsonify({"error": "No travel itinerary generated"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)