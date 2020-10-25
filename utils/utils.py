import json

import discord
from discord.ext import commands


def config(what: str):
    """Looks for a specific thing in the config."""

    with open("./config.json", "r") as f:
        data = json.load(f)
        return data[what]


class MemberIDConverter:
    class MemberID(commands.Converter):
        def can_execute_action(self, ctx, user, target):
            return (
                user.id == ctx.bot.owner_id
                or user == ctx.guild.owner
                or user.top_role > target.top_role
            )

        class MemberNotFound(Exception):
            pass

        async def resolve_member(self, guild, member_id):
            member = guild.get_member(member_id)
            if member is None:
                if guild.chunked:
                    raise self.MemberNotFound()
                try:
                    member = await guild.fetch_member(member_id)
                except discord.NotFound:
                    raise self.MemberNotFound() from None
            return member

        async def convert(self, ctx, argument):
            try:
                m = await commands.MemberConverter().convert(ctx, argument)
            except commands.BadArgument:
                try:
                    member_id = int(argument, base=10)
                    m = await self.resolve_member(ctx.guild, member_id)
                except ValueError:
                    raise commands.BadArgument(
                        f"{argument} is not a valid member or member ID."
                    ) from None
                except self.MemberNotFound:
                    # hackban case
                    return type(
                        "_Hackban",
                        (),
                        {"id": member_id, "__str__": lambda s: f"Member ID {s.id}"},
                    )()

            if not self.can_execute_action(ctx, ctx.author, m):
                raise commands.BadArgument(
                    "You cannot do this action on this user due to role hierarchy."
                )
            return m
