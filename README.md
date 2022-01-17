## Python Robokassa
***

    python -m pip install -r requirements.txt

### Module App:

#### utils:

`def calculate_signature(*args)`: Methods for creating MD5 signatures. 

`def parse_response(request: str)`: Takes a link as a string and creates a dictionary from the data. 

`def check_signature_result(request: str)`: Accepts the parsed data and signature, 
then compares and returns a Boolean value.

#### view:
Сontains the Robokassa class with methods:

`def generate_payment_link()`: URL for redirection of the customer to the service.

`def result_payment()`: Verification of notification (ResultURL).

`def check_success_payment()`: Verification of operation parameters ("cashier check") in SuccessURL script.


### Module model
#### scheme:

    @dataclass
    class Merchant:
        login: str (the Shop Identifier from Technical settings)
        password: Literal['PASSWORD', 'PASSWORD2']


    @dataclass
    class Order:
        number: int (invoice number)
        description: str (description of the purchase)
        cost: decimal (cost of goods, RU)


### Example

    merchant = Merchant('LoginMerch', ['password_1', 'password_2'])
	robokassa_payment = Robokassa(merchant)
	order = Order(12, 'Desc', 500.0)
	link = robokassa_payment.formation_payment_link(order)
	robokassa_payment.get_result_order(link)
	robokassa_payment.check_success_payment(link)