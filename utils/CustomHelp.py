import discord
from discord.ext import commands


# noinspection PyTypeChecker
class CustomHelp(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    def get_ending_note(self):
        return f"Use {self.clean_prefix}{self.invoked_with} [command|category] for more info on a command/category."

    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def command_not_found(self, string):
        if len(string) >= 50:
            return f"I was unable to find the command `{string[:20]}[...]`."
        else:
            return f"I was unable to find the command `{string}`."

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(title="Bot Commands",
                              colour=ctx.bot.colours["MAIN"])
        embed.description = f"{ctx.bot.description}"

        for cog, cmds in mapping.items():
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                all_cmds = " - ".join(f"{c.name}" for c in cmds)
                if cog and cog.description:
                    embed.add_field(
                        name=f"► {name}",
                        value=f"```md\n{all_cmds}```\n",
                        inline=False
                    )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        ctx = self.context
        embed = discord.Embed(
            title=f"Showing commands for: {cog.qualified_name}",
            colour=ctx.bot.colours["MAIN"]
        )

        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        for command in filtered:
            embed.add_field(
                name=f"{command.qualified_name}",
                value=f"{command.help.format(prefix=self.clean_prefix)}",
                inline=False
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        ctx = self.context
        embed = discord.Embed(
            title=f"{self.clean_prefix}{group.qualified_name} {group.signature}",
            colour=ctx.bot.colours["MAIN"])

        if group.help:
            aliases = (
                f"*Aliases: {' | '.join(f'`{x}`' for x in group.aliases)}*"
                if group.aliases
                else ""
            )
            group_category = group.cog.qualified_name
            embed.description = (
                str(group.help).format(prefix=self.clean_prefix)
                + "\n"
                + aliases
                + "\n"
                + f"Category: {group_category}"
            )

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=str(command.short_doc) or "...",
                    inline=False
                )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    send_command_help = send_group_help
