from flask import Flask, jsonify
from FlightRadar24.api import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

@app.route('/flights/<flight_number>', methods=['GET'])
def get_flight_by_number(flight_number):
    try:
        flights = fr_api.get_flights()  # This retrieves a list of current flights
        flight_details = None
        for flight in flights:
            if flight.callsign == flight_number:
                flight_details = fr_api.get_flight_details(flight.id)
                break
        if flight_details:
            return jsonify(flight_details)
        else:
            return jsonify({'error': 'Flight not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)