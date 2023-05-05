from hashmap import Hashmap


class Transaction():
    def __init__(self, from_user, to_user, amount):
        self._from = from_user
        self._to = to_user
        self._amount = amount

    def __hash__(self):
        # Concatenate the string representation of the attributes
        str_repr = f"{self._from}{self._to}{self._amount}"
        # Compute the hash value of the concatenated string
        return hash(str_repr)


class Block():
    def __init__(self, transactions=None, prev_hash=None):
        self.prev_hash = prev_hash
        self.transactions = transactions

    def add_transaction(self, _to, _from, _amount):
        """adds transactions to the block transaction attribute"""
        self.transactions.append(Transaction(_to, _from, _amount))

    def __eq__(self, other):
        """eq method to check if the prev_hash is equal to hash of previous"""
        if isinstance(other, Block):
            return self.prev_hash == other.__hash__()
        return False

    def __hash__(self):
        """to hash self"""
        return hash(str(self))

    def __str__(self):
        """Output formatting function"""
        return f"previous hash: {self.prev_hash}, transactions: {self.transactions}, hash: {str(id(self))}"


class Ledger():
    def __init__(self):
        self.balances_hashmap = Hashmap()

    # def has_funds(self, user, amount):

    def has_funds(self, user, amount):
        """Checking if the user has enough funds for transaction"""
        #     if user not in self._hashmap:

        if not self.balances_hashmap.get_value(user):
            return False

        balance = self.balances_hashmap.get_value(user)
        if self.balances_hashmap.get_value(user) is not None and self.balances_hashmap.get_value(user) >= amount:
            return True
        else:
            return False



    def deposit(self, user, amount):
        """deposit funds """
        self.balances_hashmap._deposit(user, amount)

    def withdraw(self, user_from, amount):
        """Withdrawing funds functionality"""
        self.balances_hashmap._withdraw(user_from, amount)


class Blockchain():
    '''Contains the chain of blocks.'''

    #########################
     
    _ROOT_BC_USER = "ROOT"  # Name of root user account.
    _BLOCK_REWARD = 1000  # Amount of HuskyCoin given as a reward for mining a block
    _TOTAL_AVAILABLE_TOKENS = 999999  # Total balance of HuskyCoin that the ROOT user receives in block0

    #########################

    def __init__(self):
        self._blockchain = list()  
        self._bc_ledger = Ledger()  # The ledger of HuskyCoin balances
        # Create the initial block0 
        self._create_genesis_block()

    
    def _create_genesis_block(self):
        '''Creates the initial block in the chain.
        This is NOT how a blockchain usually works, but it is a simple way to give the
        Root user HuskyCoin that can be subsequently given to other users'''
        trans0 = Transaction(self._ROOT_BC_USER, self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)
        block0 = Block([trans0])
        self._blockchain.append(block0)
        self._bc_ledger.deposit(self._ROOT_BC_USER, self._TOTAL_AVAILABLE_TOKENS)

  
    def distribute_mining_reward(self, user):
        '''
        You need to give HuskyCoin to some of your users before you can transfer HuskyCoing
        between users. Use this method to give your users an initial balance of HuskyCoin.
        (In the Bitcoin network, users compete to solve a meaningless mathmatical puzzle.
        Solving the puzzle takes a tremendious amount of copmputing power and consuming a lot
        of energy. The first node to solve the puzzle is given a certain amount of Bitcoin.)
        In this assigment, you do not need to understand "mining." Just use this method to 
        provide initial balances to one or more users.'''
        trans = Transaction(self._ROOT_BC_USER, user, self._BLOCK_REWARD)
        block = Block([trans])
        self.add_block(block)

    def add_block(self, block):
        """adds block to the blockchain paramater--
        transction: type list of Transactions"""
        # Check if there is a transaction

        if not block.transactions:
            return False

        if block.transactions is not None:
            prev_hash = self._blockchain[-1].__hash__() if self._blockchain else None
            block.prev_hash = prev_hash
            self._blockchain.append(block)

        for transaction in block.transactions:
            sender = transaction._from
            receiver = transaction._to
            amount = transaction._amount

            if not self._bc_ledger.has_funds(sender, amount):
                return False

            self._bc_ledger.withdraw(sender, amount)

            self._bc_ledger.deposit(receiver, amount)

        return True
        # self._bc_ledger.balances_hashmap.set_value()

    def validate_chain(self):
        """Validates that the blocks and hashes are correctly hashed and transactions are possible"""

        validated = True  # validate flag
        list_tampered = []  # list for blocks tampered with
        for i in range(1, len(self._blockchain)):
            if self._blockchain[i].prev_hash != self._blockchain[i - 1].__hash__():  # checking if the hash had changed
                list_tampered.append(self._blockchain[i])
                validated = False


        if len(list_tampered) > 0:
            return list_tampered, validated
        else:
            return validated

    def __str__(self):
        """outsputs block in readable form"""
        block_descriptions = []
        for block in self._blockchain:
            block_descriptions.append(f"--previous hash: {block.prev_hash}, transactions: {block.transactions}, hash: {block.__hash__()}")
        return "".join(block_descriptions)



chain = Blockchain()

block = Block()

chain.add_block(block)

print(chain)
