
import logging
from actions.login import login
from actions.web_driver import close_driver, get_page
from utils.error import messageError


def controller_sample(data):

    try:
        username = data['username']
        password = data['password']

    except KeyError as e:
        raise messageError(f"The field '{e.args[0]}' has not been sent")
    try:
        message = "ok"

        logging.info("|| Get initial page")
        driver = get_page()

        logging.info("|| Init Login")
        # driver = login(driver, username, password)

        # Add actions

        close_driver(driver)

        return message

    except Exception as e:
        raise messageError("Error sample controoller: " + str(e))
