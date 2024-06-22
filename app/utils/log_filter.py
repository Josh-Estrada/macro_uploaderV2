import logging

class RelevantLogFilter(logging.Filter):
    def filter(self, record):
        # Filter out messages that are not relevant
        if 'Starting new HTTPS connection' in record.getMessage():
            return False
        if 'Unverified HTTPS request' in record.getMessage():
            return False
        if record.name == 'urllib3.connectionpool':
            return False
        return True
