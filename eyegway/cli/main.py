import typer as tp
import eyegway.cli.hubs as ech

cli = tp.Typer(name="eyegway", pretty_exceptions_enable=False, no_args_is_help=True)
context_settings = {"allow_extra_args": True, "ignore_unknown_options": True}

cli.add_typer(ech.cli_hubs, name="hubs")
