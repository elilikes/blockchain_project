import sys
from os.path import exists


class Blockchain:
    def initPrev(self):
        previousHash = [
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]
        return previousHash

    def initTimeStamp(self):
        timestamp = [0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00,
                     0x00]
        return timestamp

    def initCaseID(self):
        caseid = [
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]
        return caseid

    def initEvidenceItemID(self):
        evid = [
            0x00,
            0x00,
            0x00,
            0x00]
        return evid

    def initState(self):
        state = [
            0x49,
            0x4e,
            0x49,
            0x54,
            0x49,
            0x41,
            0x4c,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]
        return state

    def checkedInState(self):
        state = [
            0x43,
            0x48,
            0x45,
            0x43,
            0x4b,
            0x45,
            0x44,
            0x49,
            0x4e,
            0x00,
            0x00,
            0x00]
        return state

    def checkedOutState(self):
        state = [
            0x43,
            0x48,
            0x45,
            0x43,
            0x4b,
            0x45,
            0x44,
            0x4f,
            0x55,
            0x54,
            0x00,
            0x00]
        return state

    def disposedState(self):
        state = [
            0x44,
            0x49,
            0x53,
            0x50,
            0x4f,
            0x53,
            0x45,
            0x44,
            0x00,
            0x00,
            0x00,
            0x00]
        return state

    def destroyedState(self):
        state = [
            0x44,
            0x45,
            0x53,
            0x54,
            0x52,
            0x4f,
            0x59,
            0x45,
            0x44,
            0x00,
            0x00,
            0x00]
        return state

    def ReleasedState(self):
        state = [
            0x52,
            0x45,
            0x4c,
            0x45,
            0x41,
            0x53,
            0x45,
            0x44,
            0x00,
            0x00,
            0x00,
            0x00]
        return state

    PreviousHash = ""
    TimeStamp = ""
    CaseID = ""
    EvidenceItemID = ""
    State = ""
    DataLength = 0
    Data = ""


def create_init_block():
    temp_block = Blockchain()

    temp_block.DataLength = 14
    temp_block.PreviousHash = temp_block.initPrev()
    temp_block.TimeStamp = temp_block.initTimeStamp()
    temp_block.State = temp_block.initState()


if sys.arg[1] == "init":
    with open("blockchain", "rb"):
        if exists("blockchain"):
            print("Blockchain file found with INITIAL block")

        else:
            # createInitialBlock
            # createFile
            print("Blockchain file not found. Created INITIAL block.")
