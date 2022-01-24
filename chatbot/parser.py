import logging
from   asgiref.sync import sync_to_async
from   result       import Result, ResultFlag

class Parser:
    def __init__(self, db):
        self.db = db
        self.builtinCommands = {
            '1'              : self.getUserVarCommand1,
            'channel'        : self.getChannelCommand,
            'command'        : self.builtInCommand,
            'if'             : self.ifCommand,
            'join'           : self.joinCommand,
            'part'           : self.partCommand,
            'quote'          : self.quoteCommand,
            'sender'         : self.senderCommand,
            'user'           : self.userCommand,
            'var'            : self.varCommand
        }

        self.subCommands = {
            'get':     self.getCommand,
            'set':     self.setCommand,
            'add':     self.setCommand,
            'edit':    self.setCommand,
            'delete':  self.deleteCommand,
            'unset':   self.deleteCommand,
            'remove':  self.deleteCommand,
            'exists':  self.existsCommand
            }

    async def process(self, bot, message, script=None):
        logging.debug(f'parser.process          | {script}')
        self.bot = bot
        self.message = message
        
        if script is None:
            return self.message
        
        processed_script = script
        subcommand = self.findSubcommand(processed_script)
        while (not subcommand.hasErrors()) and (subcommand.get() is not None):
            # Ssend to the script to the appropriate command function to resolve
            #   Remove the surrounding brackets first
            start, end = subcommand.get()
            result = await self.processCommand(message, processed_script[start+1:end])
            if result.hasErrors():
                return f'Error: {result.getErrors()}'
            logging.debug('Result: {result.get()}')
            if start == 0:
                processed_script = result.get() + processed_script[end+1:]
            else:
                processed_script = processed_script[:start] + result.get() + processed_script[end+1:]
            subcommand = self.findSubcommand(processed_script)

        if subcommand.isOk():
            message.response = processed_script
            message.send_to_server = True
        else:
            message.response = f'Error: {subcommand.getError()}'
        return message


    # Finds first subcommand in script and returns start and end.  This does not process the subcommand at all.
    #   If there are no subcommands, return None
    def findSubcommand(self, script):
        logging.debug(f'parser.findSubcommand    | {script}')
        # If there are no subcommands, return Okay, but none.
        if script.find('{') == -1:
            return Result(ResultFlag.Ok, None)

        start = script.find('{')
        nextstart = start
        nextend = script.find('}', nextstart + 1)
        end = nextend
        depth = 0

        #Cycle through until we have found the full depth.  Return breaks the loop.
        while True:
            # nextend should never = -1 until depth = 1 again, which point we return, so it should never = 1
            #    at the point this if statement is evaluated
            if nextend == -1:
                return Result(ResultFlag.Error, "# opening brackets does not match # closing brackets")
            # if nextstart > nextend, we have completed a subcommnand.  Decrease depth by 1
            elif nextstart > nextend or nextstart == -1:
                end = nextend
                nextstart = script.find('{', nextend)
                nextend   = script.find('}', nextend+1)
                depth    -= 1
                # If we're back to depth == 1, we have found a full subcommand.
                if depth == 0:
                    return Result(ResultFlag.Ok, (start, end))
            # if nextstart < nextend, we have a subcommand within a subcommand.  Increase depth by 1
            elif nextstart < nextend:
                nextend   = script.find('}', nextstart)
                nextstart = script.find('{', nextstart+1)
                depth    += 1

            if depth > 10:
                return Result(ResultFlag.Error, "depth is wrong")

    
    async def processSubcommand(self, message, script):
        logging.debug(f'parser.processSubcommand | {script}')
        command = script
        while True:
            subcommand = self.findSubcommand(command)
            if subcommand.hasErrors():
                return subcommand
            if subcommand.get() is None:
                return Result(ResultFlag.Ok, command)
            start, end = subcommand.get()
            result = await self.processCommand(message, command[start+1:end])
            if result.hasErrors():
                return result
            print(f'processSubcommand result: {str(result.get())}')
            command = command[:start] + result.get() + command[end+1:]
            command = command.strip()
            return Result(ResultFlag.Ok, command)


    async def processCommand(self, message, script):
        logging.debug(f'parser.processCommand    | {script}')
        command = script.split()[0]
        if command not in self.builtinCommands.keys():
            return Result(ResultFlag.Error, f'{command} is not a valid command.')
        result = await self.builtinCommands[command](message, script)
        logging.debug(f'processCommand result: {result.get()}')
        return result
    

    async def parseCommand(self, script):
        pass


    # up to first pipe = condition to process
    # between first & second pipe = command if condition is true
    # after second pipe = command if condition is false
    async def ifCommand(self, message, script):
        logging.debug(f'parser.ifCommand        | {message.text} {script}')
        result = script
        variables = []

        variables = script.split('|')
        # Remove if statement from condition
        variables[0] = variables[0][3:]
        
        # clean up any leading/trailing whitespaces
        for variable in variables:
            variable = variable.strip()

        condition = await self.processSubcommand(message, variables[0])
        if condition.hasErrors():
            return condition

        if condition.get() == 'True':
            command = variables[1]
        elif condition.get() == 'False':
            command = variables[2]
        else:
            return Result(ResultFlag.Error, f'condition {condition.get()} is neither True nor False')

        result = await self.processSubcommand(message, command)
        return result


    async def getUserVarCommand1(self, message, script):
        logging.debug(f'parser.getUserVarCommand1 | {message.text} | {script}')
        variables = message.originaltext.split()
        return variables[1]


    # This function is when a person uses the 'var' command
    async def varCommand(self, message, script):
        logging.debug(f'parser.varCommand        | {message.text} | {script}')
        dbType = await sync_to_async(self.db.getType, thread_sensitive=True)('variables')
        if dbType.hasErrors():
            return dbType
        # Check to see if second word is a db subCommand, e.g. add, remove, exists, etc.
        #    If so, call the appropriate function
        if script.split()[1] in self.subCommands.keys():
            logging.debug('varCommand: subCommand found')
            subcommand = script.split()[1]
            result = await self.subCommands.get(subcommand)(message, dbType.get(), script)

        # Otherwise, assume the second word is the varName that the user is attempting to get.
        else:
            logging.debug('varCommand: subCommand not found')
            var    = await self.getCommand(message, dbType.get(), script)
            result = var.value
        return Result(ResultFlag.Ok, result)


    # This function is when a person uses the 'command' command
    async def builtInCommand(self, message, script):
        logging.debug(f'parser.builtInCommand    | {message.text} {script}')
        #return await self.getsetCommand(sync_to_async(self.db.getType, thread_sensitive=True)('commands'), script)
        dbType = await sync_to_async(self.db.getType, thread_sensitive=True)('commands')
        if dbType.hasErrors:
            return dbType
        return await self.getsetCommand(dbType.get(), script)


    # This function is when a person uses the 'quote' command
    async def quoteCommand(self, message, script):
        logging.debug(f'parser.quoteCommand      | {message.text} | {script}')
        #return await self.getsetCommand(sync_to_async(self.db.getType, thread_sensitive=True)('quotes'), script)
        dbType = await sync_to_async(self.db.getType, thread_sensitive=True)('quotes')
        if dbType.hasErrors:
            return dbType
        return await self.getsetCommand(dbType.get(), script)



    async def getVarName(self, message, script):
        logging.debug(f'parser.getVarName        | {script}')
        # Check to see if there are any subcommands.  if so, process them.
        command = script
        subcommands = self.findSubcommand(command)
        if subcommands.hasErrors():
            return subcommands
        if subcommands.get() is not None:
            start, end = subcommands.get()
            result = await self.processSubcommand(message, command)
            if result.hasErrors():
                return result
            command = result.get()
        
        command_parts = command.split()
        if len(command_parts) < 2:
            logging.debug(f'getVarName: <2 parts')
            return Result(ResultFlag.Error, f'Missing variable name.')

        if len(command_parts) == 2:
            logging.debug(f'getVarName: 2 parts')
            varname = command_parts[1]
        elif len(command_parts) >= 3:
            logging.debug(f'getVarName: 3+ parts')
            varname = command_parts[2]
        logging.debug(f'  varName: {varname}')
        return Result(ResultFlag.Ok, varname)


    async def getCommand(self, message, varType, script):
        logging.debug(f'parser.getCommand        | {varType} {script}')
        varNameResult = await self.getVarName(message, script)
        if varNameResult.hasErrors():
            return varName
        
        varName = varNameResult.get().lower()
        if await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName):
            logging.debug(f'getCommand: {varName} exists')
            var = await sync_to_async(self.db.get, thread_sensitive=True)(varType, varName)
            return Result(ResultFlag.Ok, var.value.value)
        logging.debug(f'getCommand: {varName} does not exist')
        return Result(ResultFlag.Error, f'{varType} {varName} not found!')
        

    async def setCommand(self, message, varType, script):
        logging.debug(f'parser.setCommand        | {varType} {script}')
        varName = await self.getVarName(message, script)
        if varName.hasErrors():
            return varName
        self.db.set(varType, varName, ' '.join(parts[3:]))
        check = await sync_to_async(self.db.get, thread_sensitive=True)(varType, varName)
        if check.isOk():
            if check.getValue() == ' '.join(parts[3:]):
                return Result(ResultFlag.Ok, varType + ' ' + varName + ' succesfully set.')
        return Result(ResultFlag.Error, f'{varType} {varName} was not successfully set.')


    async def deleteCommand(self, varType, script):
        pass


    async def existsCommand(self, message, varType, script):
        logging.debug(f'parser.existsCommand     | {varType} {script}')
        varName = await self.getVarName(message, script)
        if varName.hasErrors():
            return varName
        logging.debug(f'checking if {varName.get()} exists')
        does_it_exist = await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName.get())
        if does_it_exist.hasErrors():
            return does_it_exist
        does_it_exist = str(does_it_exist.get())
        logging.debug(f'Does it exist? {does_it_exist}')
        return does_it_exist
        #return Result(ResultFlag.Ok, does_it_exist)
        #return await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName.get())


    async def getsetCommand(self, varType, script):
        logging.debug(f'parser.getsetCommand     | {varType} {script}')
        parts = script.split()

        # For the variable name, we need to process any { }
        if varType is None:
            return Result(ResultFlag.Error, f'Variable Type {varType} is not recognized.')
        
        # Subcommand = get, set, add, edit, delete, etc.
        # Set varName to parts[2], since most of the following use parts[2].  If not there, then
        #     try parts[1] as varName
        if len(parts) == 2:
            subcommand = None
            varName = parts[1]
        else:
            subcommand = parts[1]
            varName = parts[2]

        # Check to see if user made a command w/o a subcommand, e.g. {var greeting}.
        #    If so, assume the user is attempting to get the variable/command/etc.
        if subcommand is None:
            if await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName):
                result = await sync_to_async(self.db.get, thread_sensitive=True)(varType, varName)
                return result
            return Result(ResultFlag.Error, f'Cannot retrieve {varName} from database')

        if subcommand == 'get':
            if await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName):
                return await sync_to_async(self.db.get, thread_sensitive=True)(varType, varName)
            return Result(ResultFlag.Error, f'{varType} {varName} not found!')

        # For setting a variable, we don't want to process any { }.  We want to store those
        if subcommand == 'set' or parts[1] == 'add' or parts[1] == 'edit':
            self.db.set(varType, varName, ' '.join(parts[3:]))
            check = await sync_to_async(self.db.get, thread_sensitive=True)(varType, varName)
            if check.isOk():
                if check.getValue() == ' '.join(parts[3:]):
                    return Result(ResultFlag.Ok, varType + ' ' + varName + ' succesfully set.')
            return Result(ResultFlag.Error, f'{varType} {varName} was not successfully set.')

        if subcommand == 'delete' or parts[1] == 'unset' or parts[1] == 'remove':
            self.db.delete(varType, varName)

        if subcommand == 'exists':
            return await sync_to_async(self.db.exists, thread_sensitive=True)(varType, varName)



    # script sent only to match the same parameters as the others in the dictionary (see __init__)
    #   It is not actually used.
    async def userCommand(self, message, script):
        logging.debug(f'parser.userCommand       | {message.text} | {script}')
        words = self.message.text.split()
        if len(words) > 1:
            user = words[1]
        else:
            user = self.message.author
                
        if user[0] == '@':
            response = user[1:]
        else:
            response = user
        return Result(ResultFlag.Ok, response)


    async def senderCommand(self, message, script):
        logging.debug(f'parser.senderCommand     | {message.text} | {script}')
        return Result(ResultFlag.Ok, message.author)
        


    async def getChannelCommand(self, message, script):
        logging.debug(f'parser.getChannelCommand | {message.text} {script}')
        user = await self.userCommand(message, script)
        if user.hasErrors():
            return user
        return Result(ResultFlag.Ok, 'https://twitch.tv/' + user.get())


    async def joinCommand(self, message, script):
        logging.debug(f'parser.joinCommand       | {message.text} {script}')
        parts = message.text.split()
        if(len(parts) > 1):
            await self.bot.join_channels(parts[1:])
            channels = ' '.join(parts[1:])
            return Result(ResultFlag.Ok, f'Successfully joined channels {channels}')
        return Result(ResultFlag.Error, 'Please include channel name(s) in !join command')


    async def partCommand(self, message, script):
        logging.debug(f'parser.partCommand       | {messages.text} | {script}')
        parts = message.text.split()
        if(len(parts) > 1):
            await self.bot.part_channels(parts[1:])
            channels = ' '.join(parts[1:])
            return Result(ResultFlag.Ok, f'Successfully parted channels {channels}')
        return Result(ResultFlag.Error, 'Please include channel name(s) in !part command')
