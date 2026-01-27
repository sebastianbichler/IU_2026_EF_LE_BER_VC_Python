class NutStorage:
    def __init__(self, data: dict):
        self.data_arrays = data
        self.data_list = self._to_native_list(data)

    def _to_native_list(self, data):
        return [
            {
                "amount": int(data["amount"][i]),
                "expected_amount": int(data["expected_amount"][i])
            }
            for i in range(len(data["amount"]))
        ]

    def get_data_as_numpy(self):
        return self.data_arrays

    def get_data_as_native_list(self):
        return self.data_list
