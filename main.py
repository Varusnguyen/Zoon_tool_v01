from utilities import create_tracking_file, configure_logging
from zoon_play import ZoonPlay


if __name__ == "__main__":
    create_tracking_file('tracking.csv')
    configure_logging('logs', 'tracking.csv')
    zoon = ZoonPlay()