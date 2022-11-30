import sys
import datetime as dt
import temporenc # pip install temporenc
from os.path import exists

class Block:
    previous_hash = b""
    timestamp = b""
    case_ID = b""
    evidence_item_ID = b""
    state = b""
    data_length = b""
    data = b""
    def initPrev(self):
       return bytearray(32)

    def getTimeStamp(self):
        now = dt.datetime.now()
        return temporenc.packb(now)

    def initCaseID(self):
        return bytearray(16)

    def initEvidenceItemID(self):
        return bytearray(4)
    
    def initState(self):
        return b'INITIAL\x00\x00\x00\x00\x00'

    def checkedInState(self):
        return b'CHECKEDIN\x00\x00\x00'

    def checkedOutState(self):
        return b'CHECKEDOUT\x00\x00'

    def disposedState(self):
        return b'DISPOSED\x00\x00\x00\x00'

    def destroyedState(self):
        return b'DESTROYED\x00\x00\x00'

    def ReleasedState(self):
        return b'RELEASED\x00\x00\x00\x00'
    
    def initDataLength(self):
        return (b'\x00\x00\x00\x0e')

    def initData(self):
        return(b'Initial block\0')
   
def block_to_bytes(block : Block):
    bs = b''
    bs = bs + block.previous_hash
    bs = bs + block.timestamp
    bs = bs + block.case_ID
    bs = bs + block.evidence_item_ID
    bs = bs + block.state
    bs = bs + block.data_length
    bs = bs + block.data
    return bs
    
def create_init_block():
    temp_block = Block()
    temp_block.previous_hash = temp_block.initPrev()
    temp_block.timestamp = temp_block.getTimeStamp()
    temp_block.case_ID = temp_block.initCaseID()
    temp_block.evidence_item_ID = temp_block.initEvidenceItemID()
    temp_block.state = temp_block.initState()
    temp_block.data_length = temp_block.initDataLength()
    temp_block.data = temp_block.initData()
    return temp_block
    
def readBlockchain():
    blockchain = []
    with open('blockchain', 'rb') as f:  
        blockchain_bytes =  f.read()
        
    chain_size = len(blockchain_bytes)
    print('Length:' + str(chain_size))
    entry_length = 0
    while entry_length < chain_size:
        entry = Block()    
        entry.previous_hash = blockchain_bytes[entry_length + 0:entry_length + 32]
        entry.timestamp = blockchain_bytes[entry_length + 32:entry_length + 40]
        entry.case_ID = blockchain_bytes[entry_length + 40: entry_length + 56]
        entry.evidence_item_ID = blockchain_bytes[entry_length + 56: entry_length + 60]
        entry.state = blockchain_bytes[entry_length + 60: entry_length + 72]
        entry.data_length = blockchain_bytes[entry_length + 72: entry_length + 76]
        print(entry.data_length)
        data_int_val = int.from_bytes(entry.data_length, 'big')
        print(data_int_val)
        entry.data = blockchain_bytes[entry_length + 76 : (76 + entry_length) + data_int_val]
        blockchain.append(entry)
        entry_length =+ 76 + data_int_val
    return blockchain                            

if sys.argv[1] == "init":    
    if exists("blockchain"):
        chain = readBlockchain()
        print("Blockchain file found with INITIAL block")
        for i in chain:
            tempblock : Block = i
            print(tempblock.previous_hash)
            print(tempblock.timestamp)
            print(tempblock.case_ID)
            print(tempblock.evidence_item_ID)
            print(tempblock.state)
            print(tempblock.data_length)
            print(tempblock.data)                        
    else:       
        with open('blockchain', 'wb') as f:
            first = create_init_block()
            init_bytestr = block_to_bytes(first)
            with open('blockchain', 'wb') as f:
                f.write(init_bytestr)              
        print("Blockchain file not found. Created INITIAL block.")
