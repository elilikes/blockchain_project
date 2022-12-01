#!/usr/bin/env python3
import os
import sys
import datetime as dt
import struct
from os.path import exists
import hashlib

file_path = os.getenv('BCHOC_FILE_PATH') 

#Block class that represents blocks and their fields, also contains initial states for initializing...
class Block:
    previous_hash = b""
    timestamp = b""
    case_ID = b""
    evidence_item_ID = b""
    state = b""
    data_length = b""
    data = b""
    def initPrev(self):
       return b'\x00' * 32

    def initTimeStamp(self):
        return b'\x00' * 8
    
    def getTimeStamp(self):
        now = dt.datetime.now().timestamp()
        return struct.pack('d', now)

    def initCaseID(self):
        return b'\x00' * 16

    def initEvidenceItemID(self):
        return b'\x00' * 4
    
    def initState(self):
        return(b'INITIAL\0\x00\x00\x00\x00')
    

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
        return (b'\x0e\x00\x00\x00')

    def initData(self):
        return(b'Initial block\0')
 
#Creates the initial block
#returns a block
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

#initializes chain      
def init_chain():
    with open(file_path, 'wb') as f:
        first = create_init_block()
        init_bytestr = block_to_bytes(first)
        f.write(init_bytestr)
        f.close()
        
#Hashes a block as a parameter
#returns a byte string          
def hash_block(block : Block):
    bytes_of_block = block_to_bytes(block)
    h1 = hashlib.sha256()
    h1.update(bytes_of_block)
    return h1.digest()

#takes a block as input
#returns bytes
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

#takes two blocks as input and compares equality
#returns boolean
def block_equals(b1 : Block, b2 : Block):
    if (b1.previous_hash == b2.previous_hash):
                if (b1.state.decode() == b2.state.decode()):
                    if (b1.data_length.decode() == b2.data_length.decode()):
                        if (b1.data.decode() == b2.data.decode()):
                            return True
    return False    

#reads the blockchain file
#returns an array of block objects representing the chain
def readBlockchain():
    blockchain = []
    with open(file_path, 'rb') as f:  
        blockchain_bytes =  f.read()
        f.close()  
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
        data_int_val = int.from_bytes(entry.data_length, 'little')
        entry.data = blockchain_bytes[entry_length + 76 : (76 + entry_length) + data_int_val]
        blockchain.append(entry)
        entry_length = entry_length + 76 + data_int_val
    return blockchain                            

#takes block as parameter, converts to bytestring and appends to file
def write_block_to_chain(block: Block):
    blockstring = block_to_bytes(block) 
    with open(file_path, 'rb') as f:
        chain_bytes = f.read()
        f.close()
    with open(file_path, 'wb') as f:
        f.write(chain_bytes + blockstring)
        f.close()    

#print function for adding
def print_add(block: Block):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    formatted_time = struct.unpack('d',block.timestamp)
    asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
    print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
    print('Added item: ' + str(item_id))
    print('\tStatus: ' + block.state.decode('utf-8'))
    print('\tTime of action: ' + asd + 'Z')

#print function for checkout
def print_checkout(block: Block):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    formatted_time = struct.unpack('d',block.timestamp)
    asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
    print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
    print('Checked out item: ' + str(item_id))
    print('\tStatus: ' + block.state.decode('utf-8'))
    print('\tTime of action: ' + asd + 'Z')

#print function for checkin
def print_checkin(block: Block):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    formatted_time = struct.unpack('d',block.timestamp)
    asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
    print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
    print('Checked in item: ' + str(item_id))
    print('\tStatus: ' + block.state.decode('utf-8'))
    print('\tTime of action: ' + asd + 'Z')

#print function for checkin   
def print_remove(block: Block):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    formatted_time = struct.unpack('d',block.timestamp)
    asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
    print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
    print('Removed item: ' + str(item_id))
    print('\tStatus: ' + block.state.decode('utf-8'))
    print('\tOwner info: ' + block.data.decode('utf-8'))
    print('\tTime of action: ' + asd + 'Z')
 
#print function for checkin    
def print_log(block: Block):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    formatted_time = struct.unpack('d',block.timestamp)
    asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
    print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
    print('Item: ' + str(item_id))
    bs = block.state.decode('utf-8').rstrip('\x00')
    print('Action: ' + bs)
    print('Time: ' + asd + 'Z')
    print()

#print function for checkin
def print_log_case_item(block : Block, case : str, item : int):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    if case == casestring:
        item_id = int.from_bytes(block.evidence_item_ID,'little')
        if item_id == item:
            formatted_time = struct.unpack('d',block.timestamp)
            asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
            print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
            print('Item: ' + str(item_id))
            bs = block.state.decode('utf-8').rstrip('\x00')
            print('Action: ' + bs)
            print('Time: ' + asd + 'Z')
            print()

#print function for checkin
def print_log_case(block : Block, case : str):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    if case == casestring:
        item_id = int.from_bytes(block.evidence_item_ID,'little')
        formatted_time = struct.unpack('d',block.timestamp)
        asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
        print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
        print('Item: ' + str(item_id))
        bs = block.state.decode('utf-8').rstrip('\x00')
        print('Action: ' + bs)
        print('Time: ' + asd + 'Z')
        print()

#print function for checkin 
def print_log_item(block : Block, item : int):
    ba = block.case_ID[::-1]
    casestring = ba.hex()
    item_id = int.from_bytes(block.evidence_item_ID,'little')
    if item_id == item:
        formatted_time = struct.unpack('d',block.timestamp)
        asd = dt.datetime.fromtimestamp(formatted_time[0]).isoformat()
        print('Case: ' + casestring[0:8] + '-' + casestring[8:12] + '-' + casestring[12:16] + '-' + casestring[16:20] + '-' + casestring[20:32])
        print('Item: ' + str(item_id))
        bs = block.state.decode('utf-8').rstrip('\x00')
        print('Action: ' + bs)
        print('Time: ' + asd + 'Z')
        print()
 
#creates a block from case id and item id
#returns a block struct    
def add_block(case_id, evidence_id):
    temp = Block()
    temp.timestamp = temp.getTimeStamp()
    chain = readBlockchain()
    last_entry_index = len(chain) - 1
    
    parent_block = chain[last_entry_index]
    temp_init = create_init_block()
    if block_equals(parent_block, temp_init):
        temp.previous_hash = b'\x00' * 32    
    else:
        temp.previous_hash = hash_block(parent_block)
    temp.case_ID = case_id
    temp.evidence_item_ID = evidence_id.to_bytes(4,'little')
    temp.data_length = b'\x00' * 4
    temp.data = b''
    return temp

#parses command line and handles logic for bchoc init
if sys.argv[1] == "init":
    if len(sys.argv) > 2:
        exit(50)
    if exists(file_path):
        chain = readBlockchain()
        temp_init = create_init_block()
        first_block : Block = chain[0]
        if block_equals(temp_init, first_block):
            print("Blockchain file found with INITIAL block")
            for i in chain:
                tempblock : Block = i
                #print(tempblock.previous_hash)
                #print(tempblock.timestamp)
                #print(tempblock.case_ID)
                #print(tempblock.evidence_item_ID)
                #print(tempblock.state)
                #print(tempblock.data_length)
                #print(tempblock.data)            
        else:
            exit(60)                  
    else:       
        init_chain()   
        print("Blockchain file not found. Created INITIAL block.")

#parses command line and handles logic for bchoc add
if sys.argv[1] == 'add':
    if exists(file_path) == False:
        init_chain()
    if len(sys.argv) < 5:
        exit(4)
    case_id = bytes.fromhex(sys.argv[3].replace("-",""))[::-1]
    arg_length = len(sys.argv)
    incr = 4
    while incr < arg_length:
        if sys.argv[incr] != '-i':
            exit(13)
        evidence_id = int(sys.argv[incr+1])
        temp = add_block(case_id, evidence_id)
        temp.state = temp.checkedInState()
        chain = readBlockchain()
        for i in chain:
            temp_block : Block = i
            if temp.evidence_item_ID == temp_block.evidence_item_ID:
                exit(8)  
        write_block_to_chain(temp) 
        print_add(temp)
        incr = incr + 2

#parses command line and handles logic for bchoc checkout
if sys.argv[1] == 'checkout':
    if sys.argv[2] != '-i':
        exit(43)
    item_id = int(sys.argv[3])
    chain = readBlockchain()
    chain = chain[::-1]
    i : Block
    for i in chain:
        chain_item = int.from_bytes(i.evidence_item_ID,'little')
        if chain_item == item_id:
            if i.state.decode('utf-8') == 'CHECKEDIN\x00\x00\x00':
                temp = add_block(i.case_ID,item_id)
                temp.state = temp.checkedOutState()
                write_block_to_chain(temp)
                print_checkout(temp)
                exit(0)
            else:
                exit(44)
    exit(45)

#parses command line and handles logic for bchoc checkin
if sys.argv[1] == 'checkin':
    if sys.argv[2] != '-i':
        exit(46)
    item_id = int(sys.argv[3])
    chain = readBlockchain()
    chain = chain[::-1]
    i : Block
    for i in chain:
        chain_item = int.from_bytes(i.evidence_item_ID,'little')
        if chain_item == item_id:
            if i.state.decode('utf-8') == 'CHECKEDOUT\x00\x00':
                temp = add_block(i.case_ID,item_id)
                temp.state = temp.checkedInState()
                write_block_to_chain(temp)
                print_checkin(temp)
                exit(0)
            else:
                exit(47)
    exit(48)                

#parses command line and handles logic for bchoc remove
if sys.argv[1] == 'remove':
    if sys.argv[2] != '-i':
        exit(49)
    item_id = int(sys.argv[3])
    chain = readBlockchain()
    chain = chain[::-1]
    i : Block
    for i in chain:
        chain_item = int.from_bytes(i.evidence_item_ID,'little')
        if chain_item == item_id:
            if i.state.decode('utf-8') == 'CHECKEDIN\x00\x00\x00':
                temp = add_block(i.case_ID,item_id)
                if sys.argv[5] == "RELEASED":
                    temp.state = temp.ReleasedState()
                elif sys.argv[5] == "DESTROYED":
                    temp.state = temp.destroyedState()
                elif sys.argv[5] == "DISPOSED":
                    temp.state = temp.disposedState()
                else:
                    exit(80)
                if len(sys.argv) > 6:          
                    if sys.argv[6] == '-o':
                        owner_info =  sys.argv[7] 
                        temp.data = owner_info.encode() + b'\x00'
                        temp.data_length = (len(owner_info) + 1).to_bytes(4,'little')
                elif sys.argv[5] == "RELEASED":
                    exit(52)
                write_block_to_chain(temp)
                print_remove(temp)
                exit(0)
            else:
                exit(50)
    exit(51)

#parses command line and handles logic for bchoc log
if sys.argv[1] == 'log':
    arg_len = len(sys.argv)
    i = 2
    rev = False
    case_use = False
    item_use = False
    print_nums = False
    while i < arg_len:
        if sys.argv[i] == '-r':
            rev = True
            i = i + 1
        elif sys.argv[i] == '--reverse':
            rev = True
            i = i + 1
        elif sys.argv[i] == '-c':
            case = sys.argv[i + 1].replace("-","")
            case_use = True
            i = i + 2
        elif sys.argv[i] == '-i':
            item = int(sys.argv[i+1])
            item_use = True
            i = i + 2
        elif sys.argv[i] == '-n':
            numPrints = int(sys.argv[i+1])
            print_nums = True
            i = i + 2
        else:
            exit(66)
    chain = readBlockchain()
    if rev:
        chain = chain[::-1] 
    if print_nums:
        if numPrints < len(chain):
            for i in range(numPrints):
                print_log(chain[i])
            exit(0)
    if case_use:
        if item_use:
            for i in chain:
                print_log_case_item(i,case,item)
        else:
            for i in chain:
                print_log_case(i,case)
    elif item_use:
        for i in chain:
            print_log_item(i,item)
    else:
        for i in chain:
            print_log(i)       

#parses command line and handles logic for bchoc verify
if sys.argv[1] == 'verify':
    chain = readBlockchain()
    temp_init = create_init_block()
    
    #checking if initial block is not good  
    if block_equals(chain[0],temp_init) == False:
        exit(68)
    
    #checking if released with no owner   
    for i in chain:
        if i.state.decode('utf-8') == 'RELEASED\x00\x00\x00\x00':
            if len(i.data) < 1:
                exit(70)
    
    #checking for doing something on an already removed item   
    for k in range(len(chain)):
        checker = False
        if chain[k].state.decode() == 'RELEASED\x00\x00\x00\x00':
            item_id = int.from_bytes(chain[k].evidence_item_ID,'little')
            checker = True
        if chain[k].state.decode() == 'DISPOSED\x00\x00\x00\x00':
            checker = True
            item_id = int.from_bytes(chain[k].evidence_item_ID,'little')
        if chain[k].state.decode() == 'DESTROYED\x00\x00\x00':
            checker = True
            item_id = int.from_bytes(chain[k].evidence_item_ID,'little')
        if checker: 
            for l in range(k+1,len(chain)):
                next_item_id = int.from_bytes(chain[l].evidence_item_ID,'little')
                if next_item_id == item_id:
                    if chain[l].state.decode() == 'CHECKEDOUT\x00\x00':
                        exit(71)
                    if chain[l].state.decode() == 'CHECKEDIN\x00\x00\x00':
                        exit(72)
                    if chain[l].state.decode() == 'RELEASED\x00\x00\x00\x00':
                        exit(73)
                    if chain[l].state.decode() == 'DISPOSED\x00\x00\x00\x00':
                        exit(74)
                    if chain[l].state.decode() == 'DESTROYED\x00\x00\x00':
                        exit(75)
    
    #checking for ching in a checked in item
    for k in range(len(chain)):
        checker = False      
        if chain[k].state.decode() == 'CHECKEDIN\x00\x00\x00':
            item_id = int.from_bytes(chain[k].evidence_item_ID,'little')
            checker = True
        if checker: 
            for l in range(k+1,len(chain)):
                next_item_id = int.from_bytes(chain[l].evidence_item_ID,'little')
                if next_item_id == item_id:
                    if chain[l].state.decode() == 'CHECKEDOUT\x00\x00':
                        break
                    if chain[l].state.decode() == 'CHECKEDIN\x00\x00\x00':
                        exit(76)

    #checking for checking out a checked out item
    for k in range(len(chain)):
        checker = False
        if chain[k].state.decode() == 'CHECKEDOUT\x00\x00':
            item_id = int.from_bytes(chain[k].evidence_item_ID,'little')
            checker = True
        if checker: 
            for l in range(k+1,len(chain)):
                next_item_id = int.from_bytes(chain[l].evidence_item_ID,'little')
                if next_item_id == item_id:
                    if chain[l].state.decode() == 'CHECKEDIN\x00\x00\x00':
                        break                    
                    if chain[l].state.decode() == 'CHECKEDOUT\x00\x00':
                        exit(77)
    
    #checking for duplicate parent                     
    for k in range(len(chain)):   
        parent_hash = chain[k].previous_hash
        for l in range(k+1,len(chain)):
            if chain[k].previous_hash == chain[l].previous_hash:
                exit(78)
    
    #checking for correct hashing
    m = 2
    while m < len(chain):
        hashed_block = hash_block(chain[m])
        if chain[m+1] != hashed_block:
            exit(79)
        m = m + 1
        
        
         
                
            
            
