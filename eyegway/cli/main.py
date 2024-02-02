import typer as tp
import eyegway.cli.packer as ecp
import eyegway.cli.streams as ecs

cli = tp.Typer(name="eyegway", pretty_exceptions_enable=False, no_args_is_help=True)
context_settings = {"allow_extra_args": True, "ignore_unknown_options": True}

cli.add_typer(ecp.cli_packer, name="packer")
cli.add_typer(ecs.cli_streams, name="streams")
