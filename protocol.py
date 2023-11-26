import json
import time
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_tcp(message, host, port):
    try:
        port = int(port)  # Validate that port is an integer
        socket_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_temp.connect((host, port))
        message = message.encode('utf-8')
        socket_temp.send(message)
        logger.info(f"Message sent to {host}:{port}: {message}")
    except ValueError:
        logger.error("Port must be an integer.")
    except Exception as e:
        message_info = json.loads(message)
        message_parts = message_info['content_name'].split('/')[0].split('-')
        logger.error(f"[{message_parts[2]}] Connection Error: {e}. Message = {message_info}.")
    finally:
        socket_temp.close()

def make_interest_packet(content_name):
    try:
        # Validate content_name format
        if not isinstance(content_name, str) or not content_name:
            raise ValueError("Invalid content_name format.")
        
        packet = {
            "content_name": f'{content_name}/{time.time()}',
            "type": "interest"
        }
        return json.dumps(packet)
    except Exception as e:
        logger.error(f"Error creating interest packet: {str(e)}")
        return None

def make_data_packet(content_name, data):
    try:
        # Validate content_name format
        if not isinstance(content_name, str) or not content_name:
            raise ValueError("Invalid content_name format.")
        
        packet = {
            "content_name": f'{content_name}/{time.time()}',
            'data': data,
            'type': 'data'
        }
        return json.dumps(packet)
    except Exception as e:
        logger.error(f"Error creating data packet: {str(e)}")
        return None
