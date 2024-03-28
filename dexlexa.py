import json
import logging
import requests
from pydexcom import Dexcom


def create_json_logger(filename):
    """Creates a JSON formatter logger."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)

    logger = logging.getLogger('dexlexa')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # Log all info and errors

    return logger


def get_reading(username, password):
    """Fetches current glucose reading from Dexcom."""
    try:
        dexcom = Dexcom(username, password)
        return dexcom.get_current_glucose_reading()
    except Exception as e:
        logger.error(f"Error connecting to Dexcom: {e}")
        return None


def alexa_trigger(monkey_endpoint, glucose_value, glucose_trend):
    """Triggers alert on Alexa via voicemonkey.io."""
    try:
        response = requests.get(monkey_endpoint)
        if response.status_code == 200:
            result = f"Alert triggered: bg={glucose_value}, trend={glucose_trend}"
            return result
        else:
            result = f"Error triggering alert. Status code: {response.status_code}"
            return result
    except requests.RequestException as e:
        result = f"Error connecting to voicemonkey.io: {e}"
        return result


def alert_logic(glucose_value, glucose_trend, myalerts):
    #Checks for alerts based on current reading.
    for i in myalerts:
        if (myalerts[i].get("bottom_range") <= glucose_value <= myalerts[i].get("top_range") and
                glucose_trend in myalerts[i].get("glucose_trend")):
            return myalerts[i].get("monkey")
    return None


def main():
    """Retrieves readings and triggers alerts."""
    logger = create_json_logger("dexlexa.log")

    try:
        # Load configuration
        with open("dexlexa.json") as config_file:
            config = json.load(config_file)

        glucose_reading = get_reading(config["dexcom"]["username"], config["dexcom"]["password"])
        if glucose_reading:
            monkey_endpoint = alert_logic(glucose_reading.value, str(glucose_reading.trend), config.get("alerts"))
            if monkey_endpoint:
                result = alexa_trigger(monkey_endpoint, glucose_reading.value, str(glucose_reading.trend))
                if result.startswith("Alert"):
                    logger.info(result)
                else:
                    logger.error(result)
            else:
                logger.info(f"No alerts triggered: bg={glucose_reading.value}, trend={glucose_reading.trend}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
