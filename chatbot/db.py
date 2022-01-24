import django
django.setup()

from datetime import datetime
import logging
from random import randint

from chatbot.models import *
from result import Result, ResultFlag
from   asgiref.sync import sync_to_async

dbTableTypes = {
    'commands':  Command,
    'settings':  ConnectionSetting,
    'variables': Variable
}


# Returns the connection settings for a particular plugin
def getConnectionSettings(plugin):
    logging.debug(f'db.getConnectionSettings | {plugin}')
    results = ConnectionSetting.objects.filter(platform=plugin)
    settings = {}
    settings['channels'] = []
    for result in results:
        if result.field == 'channel':
            settings['channels'].append(result.value)
        else:
            settings[result.field] = result.value
    return Result(ResultFlag.Ok, settings)


# Returns the list of commands and the corresponding scripts
def getCommands():
    logging.debug('db.getCommands           |')
    return Result(ResultFlag.Ok, Command.objects.all())


async def getScript(commandName):
    logging.debug(f'db.getScript            | {commandName}')
    command       = await sync_to_async(Command.objects.get, thread_sensitive=True)(name=commandName.strip())
    return Result(ResultFlag.Ok, command.script)


def getType(t):
    logging.debug(f'db.getType              | {t}')
    if t in dbTableTypes:
        return Result(ResultFlag.Ok, dbTableTypes[t])
    return Result(ResultFlag.Error, f'Table Type {t} does not exist.')


def exists(varType, varName):
    logging.debug(f'db.exists                | {varType} {varName}')
    return Result(ResultFlag.Ok, varType.objects.filter(name=varName).exists())


def get(varType, varName):
    logging.debug(f'db.get                  | {varType} {varName}')
    result = varType.objects.filter(name=varName).order_by('?')[0]
    if result is None:
        return Result(ResultFlag.Error, 'No variables of type {varType} named {varName}')
    return Result(ResultFlag.Ok, result)


def set(varType, varName, value):
    logging.debug('db.set - pass')
    pass


def delete(varType, varName):
    logging.debug('db.delete - pass')
    pass
