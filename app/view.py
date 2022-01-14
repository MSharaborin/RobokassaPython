from urllib import parse

from model.scheme import Merchant, Order
from app.setting import default_url_robokassa_payment, bad_response, success_payment, is_test
from app.utils import calculate_signature, parse_response, check_signature_result


class Robokassa():

	def __init__(self, merchant: Merchant):
		self.merchant = merchant

	def formation_payment_link(self, order: Order) -> str:
		"""URL for redirection of the customer to the service.
		"""

		# build CRC value
		signature = calculate_signature(
			self.merchant.login,
			order.cost,
			order.number,
			self.merchant.password[0]
		)

		data = {
			'MerchantLogin': self.merchant.login,
			'OutSum': order.cost,
			'InvId': order.number,
			'Description': order.description,
			'SignatureValue': str(signature),
		}

		if is_test:
			data.update({'IsTest': '1'})
		return ''.join((default_url_robokassa_payment, parse.urlencode(data)))

	def get_result_order(self, request: str) -> str:
		"""Verification of notification (ResultURL).
		:param request: HTTP parameters.
		"""
		param_request = parse_response(request)

		# build own CRC
		signature = calculate_signature(
			param_request.get('OutSum'),
			param_request.get('InvId'),
			param_request.get('SignatureValue')
		)
		if check_signature_result(
				param_request.get('InvId'),
				param_request.get('OutSum'),
				signature,
				self.merchant.password[1]
		):
			return ' '.join(('OK', param_request.get('InvId')))
		return bad_response

	def check_success_payment(self, request: str) -> str:
		"""Verification of operation parameters ("cashier check") in SuccessURL script.
		:param request: HTTP parameters
		"""
		param_request = parse_response(request)

		# build own CRC
		signature = calculate_signature(
			param_request.get('OutSum'),
			param_request.get('InvId'),
			param_request.get('SignatureValue')
		)
		if check_signature_result(
				param_request.get('InvId'),
				param_request.get('OutSum'),
				signature,
				self.merchant.password[0]
		):
			return success_payment
		return bad_response
