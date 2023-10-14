from django.core.management.commands import makemessages


class Command(makemessages.Command):
    msgattrib_options = makemessages.Command.msgattrib_options + [
        "--no-fuzzy",
        "--no-location",
        "--no-wrap",
    ]
    msguniq_options = makemessages.Command.msguniq_options + [
        "--no-wrap",
        "--no-location",
    ]
    msgmerge_options = makemessages.Command.msgmerge_options + [
        "--no-location",
        "--no-wrap",
        "--no-fuzzy-matching",
    ]
    xgettext_options = makemessages.Command.xgettext_options + [
        "--no-location",
        "--no-wrap",
    ]
