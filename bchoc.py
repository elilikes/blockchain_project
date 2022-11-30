#!/usr/bin/env python3
import os
import sys
import datetime as dt
import temporenc # pip install temporenc
from os.path import exists
import hashlib
import uuid

file_path = os.getenv('BCHOC_FILE_PATH') #

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
    entry_length = 0
    while entry_length < chain_size:
        entry = Block()    
        entry.previous_hash = blockchain_bytes[entry_length + 0:entry_length + 32]
        entry.timestamp = blockchain_bytes[entry_length + 32:entry_length + 40]
        entry.case_ID = blockchain_bytes[entry_length + 40: entry_length + 56]
        entry.evidence_item_ID = blockchain_bytes[entry_length + 56: entry_length + 60]
        entry.state = blockchain_bytes[entry_length + 60: entry_length + 72]
        entry.data_length = blockchain_bytes[entry_length + 72: entry_length + 76]
        data_int_val = int.from_bytes(entry.data_length, 'big')
        entry.data = blockchain_bytes[entry_length + 76 : (76 + entry_length) + data_int_val]
        blockchain.append(entry)
        entry_length =+ 76 + data_int_val
    return blockchain                            

def is_valid_uuid(id : str):
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False

if sys.argv[1] == "init":
    if exists("blockchain"):
        print("Blockchain file found with INITIAL block")                       
    else:       
        with open('blockchain', 'wb') as f:
            first = create_init_block()
            init_bytestr = block_to_bytes(first)
            with open('blockchain', 'wb') as f:
                f.write(init_bytestr)              
        print("Blockchain file not found. Created INITIAL block.")


if sys.argv[1] == 'add':
    if sys.argv[2] != '-c':
        exit(29)
    h1 = hashlib.sha256()
    case_id = sys.argv[3].replace("-","")
    if is_valid_uuid(case_id) == False:
        exit(29)
    arg_length = len(sys.argv)
    i = 4
    while i < arg_length:
        new_block = Block()
        chain = readBlockchain()
        last_entry_index = len(chain) - 1
        parent_block = block_to_bytes(chain(last_entry_index))
        h1.update(parent_block)
        new_block.previous_hash = h1.digest()
        new_block.timestamp = new_block.getTimeStamp()
        new_block.case_ID = bytes.fromhex(case_id)
        if sys.argv[i] != '-i':
            exit(29)
        new_block.evidence_item_ID = int(sys.argv[i+1]).to_bytes(4,'big')
        new_block.state = new_block.checkedInState()
        new_block.data_length = (0).to_bytes(4, 'big')
        new_block.data = b''
        blockstring = block_to_bytes(new_block)
        with open('blockchain', 'ab') as f:
            f.write(blockstring)
        print('Case: ' + blockstring[0:7].decode('utf-8') + '-' + blockstring[8:12].decode('utf-8') + blockstring[12:16].decode('utf-8') 
              + blockstring[16:20].decode('utf-8') + blockstring[20:32].decode('utf-8'))
        item_id = int.from_bytes(new_block.evidence_item_ID,'big')
        print('Added item: ' + str(item_id))
        print('\tStatus: ' + new_block.state.decode('utf-8'))
        formatted_time = temporenc.unpackb(new_block.timestamp)
        print('\tTime of action: ' + formatted_time.date() + 'T' + formatted_time.time() + 'Z')
        i = i + 2
        
if sys.argv[1] == 'checkout':
    if sys.argv[2] != '-i':
        exit(28)
    item_id = sys.argv[3].encode()
    chain = readBlockchain()
    j : Block
    for j  in chain:
        if j.evidence_item_ID == item_id:
            if j.status == b'CHECKEDIN\x00\x00\x00':
                blockstring = block_to_bytes(new_block)
                print('Case: ' + blockstring[0:7].decode('utf-8') + '-' + blockstring[8:12].decode('utf-8') + blockstring[12:16].decode('utf-8') 
                    + blockstring[16:20].decode('utf-8') + blockstring[20:32].decode('utf-8'))
                j.status == j.checkedOutState()
                j.timestamp = j.getTimeStamp()
                new_item_id = int.from_bytes(item_id,'big')
                print('Checked out item: ' + str(new_item_id))
                print('\tStatus: ' + new_block.state.decode('utf-8'))
                formatted_time = temporenc.unpackb(j.timestamp)
                print('\tTime of action: ' + formatted_time.date() + 'T' + formatted_time.time() + 'Z')
            else:
                print('Error: Cannot check out a checked out item. Must check it in first.')
            

if sys.argv[1] == 'checkin':
    if sys.argv[2] != '-i':
        exit(28)
    item_id = sys.argv[3].encode()
    chain = readBlockchain()
    j : Block