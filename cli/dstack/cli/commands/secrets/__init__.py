import sys
from argparse import Namespace

from rich import print
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from dstack.core.error import check_config, check_git
from dstack.cli.commands import BasicCommand
from dstack.api.repo import load_repo_data
from dstack.api.backend import list_backends
from dstack.core.secret import Secret


class SecretCommand(BasicCommand):
    NAME = "secrets"
    DESCRIPTION = "Manage secrets"

    def __init__(self, parser):
        super(SecretCommand, self).__init__(parser)

    def register(self):
        subparsers = self._parser.add_subparsers()

        subparsers.add_parser("list", help="List secrets")

        add_secrets_parser = subparsers.add_parser("add", help="Add a secret")
        add_secrets_parser.add_argument(
            "secret_name", metavar="NAME", type=str, help="The name of the secret"
        )
        add_secrets_parser.add_argument(
            "secret_value",
            metavar="VALUE",
            type=str,
            help="The value of the secret",
            nargs="?",
        )
        add_secrets_parser.add_argument(
            "-y", "--yes", help="Don't ask for confirmation", action="store_true"
        )
        add_secrets_parser.set_defaults(func=self.add_secret)

        update_secrets_parser = subparsers.add_parser("update", help="Update a secret")
        update_secrets_parser.add_argument(
            "secret_name", metavar="NAME", type=str, help="The name of the secret"
        )
        update_secrets_parser.add_argument(
            "secret_value",
            metavar="VALUE",
            type=str,
            help="The value of the secret",
            nargs="?",
        )
        update_secrets_parser.set_defaults(func=self.update_secret)

        delete_secrets_parser = subparsers.add_parser("delete", help="Delete a secret")
        delete_secrets_parser.add_argument(
            "secret_name", metavar="NAME", type=str, help="The name of the secret"
        )
        delete_secrets_parser.set_defaults(func=self.delete_secret)

    @check_config
    def add_secret(self, args: Namespace):
        repo_data = load_repo_data()
        for backend in list_backends():
            if backend.get_secret(repo_data, args.secret_name):
                if args.yes or Confirm.ask(
                    f"[red]The secret '{args.secret_name}' already exists. "
                    f"Do you want to override it?[/]"
                ):
                    secret_value = args.secret_value or Prompt.ask("Value", password=True)
                    backend.update_secret(repo_data, Secret(args.secret_name, secret_value))
                    print(f"[grey58]OK[/]")
                else:
                    return
            else:
                secret_value = args.secret_value or Prompt.ask("Value", password=True)
                backend.add_secret(repo_data, Secret(args.secret_name, secret_value))
                print(f"[grey58]OK[/]")

    @check_config
    def update_secret(self, args: Namespace):
        repo_data = load_repo_data()
        for backend in list_backends():
            if backend.get_secret(repo_data, args.secret_name):
                secret_value = args.secret_value or Prompt.ask("Value", password=True)
                backend.update_secret(repo_data, Secret(args.secret_name, secret_value))
                print(f"[grey58]OK[/]")
                return
        sys.exit(f"The secret '{args.secret_name}' doesn't exist")

    @check_config
    def delete_secret(self, args: Namespace):
        repo_data = load_repo_data()
        for backend in list_backends():
            secret = backend.get_secret(repo_data, args.secret_name)
            if secret and Confirm.ask(f" [red]Delete the secret '{secret.secret_name}'?[/]"):
                backend.delete_secret(repo_data, secret.secret_name)
                print(f"[grey58]OK[/]")

        sys.exit(f"The secret '{args.secret_name}' doesn't exist")

    @check_config
    @check_git
    def _command(self, args: Namespace):
        console = Console()
        table = Table(box=None)
        repo_data = load_repo_data()
        table.add_column("NAME", style="bold", no_wrap=True)
        for backend in list_backends():
            secret_names = backend.list_secret_names(repo_data)
            for secret_name in secret_names:
                table.add_row(secret_name)
        console.print(table)