#
# Copyright 2016 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from handlers import handler_start, handler_stop
from structlog import get_logger
from jinja2 import Template

from common.utils.dockerhelpers import EventProcessor

class Podder(object):

    log = get_logger()

    def __init__(self, args, slave_config):
        self.log.info('Initializing Podder')
        self.running = False
        self.events = EventProcessor()
        self.handlers = { 'podder_config' : Template(slave_config) }

    def run(self):
        if self.running:
            return
        self.running = True

        self.initialize()

    def shutdown(self):
        try:
            self.events.stop_listening()
        except:
            self.log.info('Shutting down')

    def initialize(self):
        self.define_handlers()
        while True:
            try:
                self.events.listen_for_events(self.handlers)
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception, e:
                self.log.info('Handler exception', e)

    def define_handlers(self):
        self.handlers['start'] = handler_start
        self.handlers['stop'] = handler_stop
