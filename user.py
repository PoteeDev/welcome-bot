import json
class user_model:
        def __init__(self,chat_id):
                self.FIO        = ""
                self.group      = ""
                self.isCommand  = False
                self.ifCommand  = ""
                self.status     = -1
                self.chat_id    = chat_id
        def setName(self, FIO):
                self.FIO = FIO
        def setGroup(self, group):
                self.group = group
        def setStatusCommand(self, isCommand):
                self.isCommand = isCommand
        def setifCommand(self, ifCommand):
                self.ifCommand = ifCommand
        def sendToFile(self):
                with open('data.txt', 'a') as f:
                    f.write(self.FIO + " " + self.group + " " +  str(self.isCommand) + " " + self.ifCommand + '\n')