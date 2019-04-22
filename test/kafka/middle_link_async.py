#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron
import logging
import random
import time


class MiddleLinkAsync(Link):
    @staticmethod
    def dummy_log(message):
        logging.info(f'MiddleLinkAsync -> {message}')

    def remote_method(self, context, message):
        logging.info(f'RPC invocation of remote_method(message): {message}.\Context: {context}')

    def remote_add_input_topic(self, context, topic):
        self.add_input_topic(topic)

    def setup(self):
        logging.debug(f'{self.__class__.__name__} -> setup()')
        logging.debug(f'{self.__class__.__name__} -> input_topics: {self.input_topics}')
        logging.debug(f'{self.__class__.__name__} -> output_topics: {self.output_topics}')

        self.loop(self.dummy_log, args=['hello'], interval=5, wait=True)
        time.sleep(6)
        self.loop(self.dummy_log, kwargs={'message': 'world'}, interval=5, wait=False)

        self.add_input_topic('input1')

        wait = random.randint(5, 15)
        logging.debug(f'{self.__class__.__name__} -> Waiting {wait} seconds...')
        time.sleep(wait)

    def transform(self, electron):
        logging.debug(f'{self.__class__.__name__} -> transform()')
        logging.debug(f'{self.__class__.__name__} -> received key: {electron.key}, value: {electron.value}')
        electron.key = str(electron.key) + '_transformed_async'
        electron.value = str(electron.value) + '_transformed_async'
        logging.debug(f'{self.__class__.__name__} -> previous topic: {electron.previous_topic}')

        if random.randint(0, 100) == 84:
            if "input2" not in self.input_topics:
                self.add_input_topic("input2")
                logging.debug(f'{self.__class__.__name__} -> INPUT CHANGED {self.input_topics}')
            else:
                self.remove_input_topic("input2")
                logging.debug(f'{self.__class__.__name__} -> INPUT CHANGED {self.input_topics}')

        self.send(electron)


if __name__ == "__main__":
    MiddleLinkAsync(log_level='DEBUG', consumer_group='custom_group_1').start()
