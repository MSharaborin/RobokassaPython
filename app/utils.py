import decimal
import hashlib

from loguru import logger


def calculate_signature(*args) -> str:
	"""Create signature MD5.
	"""
	return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
	"""
	:param request: Link.
	:return: Dictionary.
	"""
	from urllib.parse import urlparse
	params = {}

	for item in urlparse(request).query.split('&'):
		key, value = item.split('=')
		params[key] = value
	return params


def check_signature_result(
	order_number: int,
	received_sum: decimal,
	received_signature: hex,
	password: str
) -> bool:
	signature = calculate_signature(received_sum, order_number, password)
	if signature.lower() == received_signature.lower():
		return True
	logger.error(f'{signature.lower()} != {received_signature.lower()}')
	return False
