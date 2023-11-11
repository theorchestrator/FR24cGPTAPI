from flask import Flask, jsonify
import time
from FlightRadar24.api import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

@app.route('/flights/<flight_number>', methods=['GET'])
def get_flight_by_number(flight_number):
    try:
        flights = fr_api.get_flights()  # This retrieves a list of current flights
        for flight in flights:
            if flight.callsign == flight_number:
                flight_details = fr_api.get_flight_details(flight.id)
                if flight_details:
                    # Extract destination and origin using the correct structure from the JSON analysis
                    destination_info = flight_details.get("airport", {}).get("destination", {})
                    origin_info = flight_details.get("airport", {}).get("origin", {})

                    destination = destination_info.get("name", "Unknown") if destination_info else "Unknown"
                    origin = origin_info.get("name", "Unknown") if origin_info else "Unknown"
                    is_live = flight_details.get("status", {}).get("live", False)

                    # Calculate the estimated time to destination
                    estimated_arrival = flight_details.get("time", {}).get("estimated", {}).get("arrival")
                    if estimated_arrival:
                        current_time = int(time.time())
                        time_remaining_seconds = estimated_arrival - current_time
                        hours = time_remaining_seconds // 3600
                        minutes = (time_remaining_seconds % 3600) // 60
                        time_to_destination = f"{hours} hours, {minutes} minutes"
                    else:
                        time_to_destination = "Unknown"

                    return jsonify({
                        "live": is_live,
                        "origin": origin,
                        "destination": destination,
                        "time_to_destination": time_to_destination
                    })
                else:
                    return jsonify({'error': 'Flight details not found'}), 404
        return jsonify({'error': 'Flight not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
