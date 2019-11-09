'''
@Description: log tool that can take a log of messages with the level INFO, WARNING, ERROR, or CRITICAL
@Version: 1.0.0.20191109
@Author: Jichen Zhao (driver) and Connor Worthington (observer)
@Date: 2019-11-09 06:00:48
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-09 06:44:03
'''

import logging


def Log(level: 'str', message) -> None:
    '''
    This function can add a message with the level INFO, WARNING, ERROR, or CRITICAL to the specified running log.

    :param level: the level of a message (accepted values: 'info', 'warning', 'error', and 'critical')
    :param message: the message decided to show in the related record of the running log
    :raises Exception: a common exception will be raised if the level of a message is invalid
    '''

    logging.basicConfig(
        level = logging.INFO, filename = 'appName.log', filemode = 'a',
        format = '%(asctime)s - %(module)s\%(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s') # TODO: filename

    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
    else:
        raise Exception('Invalid level of a message.')


# test purposes only
if __name__ == '__main__':
    Log('info', True)
    Log('warning', 404)

    try:
        2 / 0
    except Exception as e:
        Log('error', e)
    
    Log('critical', 'No such module.')