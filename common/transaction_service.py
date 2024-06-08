class TransactionService:
    def __init__(self):
        self.transactions = {}  # dictionary to store (key, value) pairs for each transactionID

    def store_value(self, transaction_id, key, value):
        self.transactions[transaction_id] = (key, value)

    def get_value(self, transaction_id):
        return self.transactions[transaction_id]

transaction_service = TransactionService()