#!/usr/bin/env python

"""
chatbot.py: This is the main engine of the bot, which communicates with the various plugins.
"""

import asyncio
import importlib
import logging
import pkgutil

import chatbot.db as db
from .parser import Parser


"""
Main Bot Class
"""
class ChatBot:
    def __init__(self):
        print('Initializing core modules...')
        logging.basicConfig(filename='twitch.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
        self.parser = Parser(db)
        self.db     = db

        print('Initializing plugin modules...')
        self.plugins = {}
        modules = pkgutil.iter_modules(path=['chatbot/plugins'])
        for module in modules:
            print(f'\tLoading Module {module.name}')
            settings = db.getConnectionSettings(module.name)
            if settings.isOk():
                self.plugins[module.name] = importlib.import_module('chatbot.plugins.'+module.name).Plugin(self, settings.get())
                print(f'\tModule {module.name} loaded')
            else:
                for error in settings.getErrors():
                    logging.error(f'Error loading module {module.name}: {error}')
                    print(f'Error loading module {module.name}: {error}')

        print(f'\n# of plugins loaded: {len(self.plugins)}')

    """
    Runs the bot
    """
    def run(self):
        print('Starting application...')
        for plugin in self.plugins.values():
            asyncio.run(plugin.run())
        print('Chatbot shutting down.')


    def join_channels(self, channels):
        pass

    def part_channels(self, channels):
        pass


if __name__ == "__main__":
    chatty = ChatBot()
    chatty.run()
