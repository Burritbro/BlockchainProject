
class Hashmap:
    def __init__(self):
        self._n_buckets = 64
        self._len = 64
        self._mapping = self.create_buckets()

    def create_buckets(self):
        return [dict() for i in range(self._n_buckets)]

    def set_value(self, key, value):

        hashed_key = hash(key) % self._len

        bucket = self._mapping[hashed_key]

        # found_key = False

        for index, record in enumerate(bucket):

            if index == key:
                # found_key = True
                break

        # if found_key:

        bucket[key] = value
        # else:
        #     bucket[key] = value


    def get_value(self, key):
        hashed_key = hash(key) % self._len

        bucket = self._mapping[hashed_key]

        return bucket[key]


    def delete_val(self, key):
        """functionality for delete"""
        hashed_key = hash(key) % self._len

        bucket = self._mapping[hashed_key]

        del bucket[key]

    def _deposit(self, key, amount):
        """Deposit funds functionality"""
        hashed_key = hash(key) % self._len
        if key in self._mapping[hashed_key]:
            self._mapping[hashed_key][key] += amount
        else:
            self._mapping[hashed_key][key] = amount

    def _withdraw(self, key, amount):
        """functionality for withdrawal"""
        hashed_key = hash(key) % self._len
        bucket = self._mapping[hashed_key]
        if key in bucket:
            bucket[key] -= amount
            return f"Balance after transaction: {bucket[key]}"
        else:
            return f"Key {key} not found in the hash map."




    def __str__(self):
        return "".join(str(item) for item in self._mapping)








