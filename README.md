# Recording California Reservoir Water Level using MQTT

This project is to demnostrate usage of MQTT to communicate water levels from publisher to subscriber and use the data to populate the dashboard.

## Prerequisites

- Python 3.x
- Redis server
- MQTT broker (e.g., Mosquitto)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sarveshborkar/mqtt-california-reservoir.git
    cd mqtt-california-reservoir
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Start the Redis server:
    ```sh
    redis-server
    ```

4. Start the MQTT broker (e.g., Mosquitto):
    ```sh
    mosquitto
    ```

## Running the Application

1. Start the MQTT subscriber to receive data and cache it:
    ```sh
    python subscriber.py
    ```

2. Publish data to the MQTT broker:
    ```sh
    python publisher.py data/Shasta_WML.csv Shasta/WML
    python publisher.py data/Oroville_WML.csv Oroville/WML
    python publisher.py data/Sonoma_WML.csv Sonoma/WML
    ```

3. Start the Dash web application:
    ```sh
    python app.py
    ```

4. Open your web browser and navigate to `http://127.0.0.1:8050` to view the dashboard.

## Dashboard

The dashboard allows you to select a date from a dropdown menu and view the water levels of the Oroville, Shasta, and Sonoma reservoirs on that date.

## Project Structure

- `app.py`: Main application file for the Dash web application.
- `cache.py`: Contains functions for caching data in Redis.
- `subscriber.py`: MQTT subscriber that receives data and caches it.
- `publisher.py`: Publishes data to the MQTT broker.
- `data/`: Contains CSV files with water level data.
- `assets/`: Contains CSS styles for the dashboard.
- `screenshots/`: Contains screenshots of the application.
- `requirements.txt`: Lists the required Python packages.
