'''
@Description: log tool that can take a log of messages with the level INFO, WARNING, ERROR, or CRITICAL
@Version: 1.2.2.20191118
@Author: Jichen Zhao (driver) and Niran Prajapati (observer)
@Date: 2019-11-09 06:00:48
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-20 15:40:39
'''

import inspect
import logging


def Log(level: 'str', message: 'str') -> None:
    '''
    Add a message with the level INFO, WARNING, or ERROR to the specified running log.

    :param level: the level of a message (accepted values: 'info', 'warning', and 'error')
    :param message: the message decided to show in the related record of the running log
    :raises Exception: a common exception will be raised if the level of a message is invalid
    '''

    message = inspect.stack()[1][3] + ': ' + message # add the name of the function calling this function to the message

    logging.basicConfig(
        level = logging.INFO,
        filename = 'running.log',
        filemode = 'a',
        datefmt="%Y-%m-%d %H:%M:%S",
        format = '%(asctime)s - %(levelname)s - %(message)s')

    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    else:
        raise Exception('Invalid level of a message.')


# test purposes only
if __name__ == '__main__':
    Log('info', 'Hello World!')
    Log('warning', 'Nothing in the list.')

    try:
        2 / 0
    except Exception as e:
        Log('error', repr(e))