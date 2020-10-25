from discord.ext import commands


class Developer(commands.Cog, command_attrs={"hidden": True}):
    """All commands for the developer(s)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def dev(self, ctx):
        pass

    @dev.command(name="load")
    @commands.is_owner()
    async def dev_load(self, ctx, *cogs: str):
        """Loads all given cogs"""

        success = []
        for cog in cogs:
            try:
                self.bot.load_extension(cog)
                success.append(f"`{cog}`")
            except Exception as e:
                await ctx.send(f"{type(e).__name__} - {e}")

        await ctx.send(f"Successfully loaded: {', '.join(success)}")

    @dev.command(name="unload")
    @commands.is_owner()
    async def dev_unload(self, ctx, *cogs: str):
        """Unloads all given cogs"""
        success = []
        for cog in cogs:
            try:
                self.bot.unload_extension(cog)
                success.append(f"`{cog}`")
            except Exception as e:
                await ctx.send(f"{type(e).__name__} - {e}")
        await ctx.send(f"Successfully unloaded: {', '.join(success)}")

    @dev.command(name="reload")
    @commands.is_owner()
    async def dev_reload(self, ctx, *cogs: str):
        """Reloads all given cogs. If none is given it'll reload all cogs in bot.exts"""

        if len(cogs) == 0:
            success = []
            for ext in self.bot.exts:
                try:
                    self.bot.reload_extension(ext)
                    success.append(f"`{ext}`")
                except Exception as e:
                    await ctx.send(f"{type(e).__name__} - {e}")

            await ctx.send(f"Successfully reloaded {', '.join(success)}")
        else:
            success = []
            for ext in cogs:
                try:
                    self.bot.reload_extension(ext)
                    success.append(f"`{ext}`")
                except Exception as e:
                    await ctx.send(f"{type(e).__name__} - {e}")

            await ctx.send(f"Successfully reloaded {', '.join(success)}")


def setup(bot):
    bot.add_cog(Developer(bot))
