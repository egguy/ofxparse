from BeautifulSoup import BeautifulStoneSoup

class Ofx(object):
    pass

class Account(object):
    def __init__(self):
        self.number = ''
        self.routing_number = ''
        self.statement = None
    def __str__(self):
        return "Accout: %s, routing number: %s" % (self.number, self.routing_number)

class Statement(object):
    def __init__(self):
        self.start_date = ''
        self.end_date = ''
        self.transactions = []
    def __str__(self):
        return "Statment start: %s stop: %s with %s transations" % (self.start_date, self.end_date, len(self.transactions))

class Transaction(object):
    def __init__(self):
        self.name = ''
        self.type = ''
        self.date = ''
        self.amount = ''
        self.id = ''
        self.memo = ''
    def __repr__(self):
        return "<Transaction %s>" % self.id

class Institution(object):
    pass

class OfxParser(object):
    @classmethod
    def parse(cls_, file_handle):
        if isinstance(file_handle, type('')):
            raise RuntimeError("parse() takes in a file handle, not a string")
        ofx_obj = Ofx()
        ofx = BeautifulStoneSoup(file_handle)
        stmtrs_ofx = ofx.find('stmtrs')
        if stmtrs_ofx:
            ofx_obj.bank_account = cls_.parseStmtrs(stmtrs_ofx)
        return ofx_obj

    @classmethod
    def parseStmtrs(cls_, stmtrs_ofx):
        ''' Parse the <STMTRS> tag and return an Account object. '''
        account = Account()
        acctid_tag = stmtrs_ofx.find('acctid')
        if hasattr(acctid_tag, 'contents'):
            account.number = acctid_tag.contents[0].strip()
        bankid_tag = stmtrs_ofx.find('bankid')
        if hasattr(bankid_tag, 'contents'):
            account.routing_number = bankid_tag.contents[0].strip()

        if stmtrs_ofx:
            account.statement = cls_.parseStatement(stmtrs_ofx)
        return account
    
    @classmethod
    def parseStatement(cls_, stmt_ofx):
        '''
        Parse a statement in ofx-land and return a Statement object.
        '''
        statement = Statement()
        dtstart_tag = stmt_ofx.find('dtstart')
        if hasattr(dtstart_tag, "contents"):
            statement.start_date = dtstart_tag.contents[0].strip()
        dtend_tag = stmt_ofx.find('dtend')
        if hasattr(dtend_tag, "contents"):
            statement.end_date = dtend_tag.contents[0].strip()
        ledger_bal_tag = stmt_ofx.find('ledgerbal')
        if hasattr(ledger_bal_tag, "contents"):
            balamt_tag = ledger_bal_tag.find('balamt')
            if hasattr(balamt_tag, "contents"):
                statement.balance = balamt_tag.contents[0].strip()
        avail_bal_tag = stmt_ofx.find('availbal')
        if hasattr(avail_bal_tag, "contents"):
            balamt_tag = avail_bal_tag.find('balamt')
            if hasattr(balamt_tag, "contents"):
                statement.available_balance = balamt_tag.contents[0].strip()
        for transaction_ofx in stmt_ofx.findAll('stmttrn'):
            statement.transactions.append(cls_.parseTransaction(transaction_ofx))
        return statement

    @classmethod
    def parseTransaction(cls_, txn_ofx):
        '''
        Parse a transaction in ofx-land and return a Transaction object.
        '''
        transaction = Transaction()

        type_tag = txn_ofx.find('trntype')
        if hasattr(type_tag, 'contents'):
            transaction.type = type_tag.contents[0].strip().lower()

        name_tag = txn_ofx.find('name')
        if hasattr(name_tag, "contents"):
            transaction.name = name_tag.contents[0].strip()

        memo_tag = txn_ofx.find('memo')
        if hasattr(memo_tag, "contents"):
            transaction.memo = memo_tag.contents[0].strip()

        amt_tag = txn_ofx.find('trnamt')
        if hasattr(amt_tag, "contents"):
            transaction.amount = amt_tag.contents[0].strip()

        date_tag = txn_ofx.find('dtposted')
        if hasattr(date_tag, "contents"):
            transaction.date = date_tag.contents[0].strip()

        id_tag = txn_ofx.find('fitid')
        if hasattr(id_tag, "contents"):
            transaction.id = id_tag.contents[0].strip()

        return transaction
