from urllib import parse

from model.scheme import Merchant, Order
from app.setting import robokassa_payment_url, bad_response, success_payment, is_test
from app.utils import calculate_signature, parse_response, check_signature_result


class Robokassa():

	def __init__(self, merchant: Merchant):
		self.merchant = merchant

	def generate_payment_link(self, order: Order) -> str:
		"""URL for redirection of the customer to the service.
		"""
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
			'IsTest': is_test
		}
		return f'{robokassa_payment_url}?{parse.urlencode(data)}'

	def result_payment(self, request: str) -> str:
		"""Verification of notification (ResultURL).
		:param request: HTTP parameters.
		"""
		param_request = parse_response(request)
		cost = param_request['OutSum']
		number = param_request['InvId']
		signature = param_request['SignatureValue']

		signature = calculate_signature(cost, number, signature)

		if check_signature_result(number, cost, signature, self.merchant.password[1]):
			return f'OK{number}'
		return bad_response

	def check_success_payment(self, request: str) -> str:
		"""Verification of operation parameters ("cashier check") in SuccessURL script.
		:param request: HTTP parameters
		"""
		param_request = parse_response(request)
		cost = param_request['OutSum']
		number = param_request['InvId']
		signature = param_request['SignatureValue']

		signature = calculate_signature(cost, number, signature)

		if check_signature_result(number, cost, signature, self.merchant.password[0]):
			return success_payment
		return bad_response
