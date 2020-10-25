from discord.ext import commands
import utils


class Help(commands.Cog):
    """This place."""

    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot

        self.bot._original_help_command = bot.help_command
        bot.help_command = utils.CustomHelp(
            command_attrs={
                "hidden": True,
                "aliases": ["h"]
            }
        )
        bot.help_command.cog = self

    # noinspection PyProtectedMember
    def cog_unload(self):
        self.bot.help_command = self.bot._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
