#   Copyright 2012-2013 OpenStack, LLC.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Identity v3 OAuth action implementations"""

import logging
import sys

from cliff import command
from cliff import lister
from cliff import show

from openstackclient.common import utils


class AuthorizeRequestToken(show.ShowOne):
    """Authorize request token command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.AuthorizeRequestToken')

    def get_parser(self, prog_name):
        parser = super(AuthorizeRequestToken, self).get_parser(prog_name)
        parser.add_argument(
            '--request-key',
            metavar='<request-key>',
            help='Consumer key',
            required=True
        )
        parser.add_argument(
            '--user-token',
            metavar='<user-token>',
            help='Token of authorizing user',
            required=True
        )
        parser.add_argument(
            '--roles',
            metavar='<roles>',
            help='Role to authorize',
            required=True
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        oauth_client = self.app.client_manager.identity.oauths

        verifier_pin = oauth_client.authorize_request_token(
            parsed_args.request_key, parsed_args.user_token,
            parsed_args.roles)
        info = {}
        info.update(verifier_pin._info)
        return zip(*sorted(info.iteritems()))


class CreateAccessToken(show.ShowOne):
    """Create access token command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.CreateAccessToken')

    def get_parser(self, prog_name):
        parser = super(CreateAccessToken, self).get_parser(prog_name)
        parser.add_argument(
            '--consumer-key',
            metavar='<consumer-key>',
            help='Consumer key',
            required=True
        )
        parser.add_argument(
            '--request-key',
            metavar='<request-key>',
            help='Consumer key',
            required=True
        )
        parser.add_argument(
            '--verifier',
            metavar='<verifier>',
            help='Verifier Pin',
            required=True
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        oauth_client = self.app.client_manager.identity.oauths
        access_token = oauth_client.create_access_token(
            parsed_args.consumer_key, parsed_args.request_key,
            parsed_args.verifier)
        info = {}
        info.update(access_token._info)
        return zip(*sorted(info.iteritems()))


class CreateConsumer(show.ShowOne):
    """Create consumer command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.CreateConsumer')

    def get_parser(self, prog_name):
        parser = super(CreateConsumer, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<consumer-name>',
            help='New consumer name',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        identity_client = self.app.client_manager.identity
        consumer = identity_client.oauths.create_consumer(
            parsed_args.name
        )
        info = {}
        info.update(consumer._info)
        return zip(*sorted(info.iteritems()))


class CreateRequestToken(show.ShowOne):
    """Create request token command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.CreateRequestToken')

    def get_parser(self, prog_name):
        parser = super(CreateRequestToken, self).get_parser(prog_name)
        parser.add_argument(
            '--consumer-key',
            metavar='<consumer-key>',
            help='Consumer key',
            required=True
        )
        parser.add_argument(
            '--roles',
            metavar='<roles>',
            help='Role requested',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        oauth_client = self.app.client_manager.identity.oauths
        request_token = oauth_client.create_request_token(
            parsed_args.consumer_key, parsed_args.roles)
        info = {}
        info.update(request_token._info)
        return zip(*sorted(info.iteritems()))


class DeleteConsumer(command.Command):
    """Delete consumer command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.DeleteConsumer')

    def get_parser(self, prog_name):
        parser = super(DeleteConsumer, self).get_parser(prog_name)
        parser.add_argument(
            'consumer',
            metavar='<consumer>',
            help='Name or ID of consumer to delete',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        identity_client = self.app.client_manager.identity
        consumer = utils.find_resource(
            identity_client.oauths, parsed_args.consumer)
        identity_client.oauths.delete_consumer(consumer.id)
        return


class ListConsumer(lister.Lister):
    """List consumer command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.ListConsumer')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        columns = ('ID', 'Name', 'Consumer Key', 'Consumer Secret')
        data = self.app.client_manager.identity.oauths.list_consumers()
        return (columns,
                (utils.get_item_properties(
                    s, columns,
                    formatters={},
                ) for s in data))


class SetConsumer(command.Command):
    """Set consumer command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.SetConsumer')

    def get_parser(self, prog_name):
        parser = super(SetConsumer, self).get_parser(prog_name)
        parser.add_argument(
            'consumer',
            metavar='<consumer>',
            help='Name or ID of consumer to change',
        )
        parser.add_argument(
            '--name',
            metavar='<new-consumer-name>',
            help='New consumer name',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        identity_client = self.app.client_manager.identity
        consumer = utils.find_resource(
            identity_client.oauths, parsed_args.consumer)
        kwargs = {}
        if parsed_args.name:
            kwargs['name'] = parsed_args.name

        if not len(kwargs):
            sys.stdout.write("Consumer not updated, no arguments present")
            return
        identity_client.oauths.update_consumer(consumer.id, **kwargs)
        return


class ShowConsumer(show.ShowOne):
    """Show consumer command"""

    api = 'identity'
    log = logging.getLogger(__name__ + '.ShowConsumer')

    def get_parser(self, prog_name):
        parser = super(ShowConsumer, self).get_parser(prog_name)
        parser.add_argument(
            'consumer',
            metavar='<consumer>',
            help='Name or ID of consumer to display',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)
        identity_client = self.app.client_manager.identity
        consumer = utils.find_resource(
            identity_client.oauths, parsed_args.consumer)

        info = {}
        info.update(consumer._info)
        return zip(*sorted(info.iteritems()))
