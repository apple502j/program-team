import discord,aiohttp
from discord.ext import commands

import m10s_util as ut

class MEE6(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession(loop=bot.loop)


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.guild)
    async def levels(self,ctx,start=1,end=10):
        start -= 1
        async with self.bot.session.get("https://mee6.xyz/api/plugins/levels/leaderboard/{0}".format(ctx.guild.id)) as resp:
            js = await resp.json()
            if "status_code" in js:
                if js["status_code"] == 404:
                    await ctx.send(embed=discord.Embed(title=ut.textto("cmd-error-t",ctx.author),description=ut.textto("mee6-notfound",ctx.author)))
                    return

            else:
                l = []
                for row in js["players"][start:end]:
                    l.append("{0}: {1}Lv {2}/{3}exp".format(ctx.guild.get_member(row["id"]).name if not ctx.guild.get_member(row["id"]) is None else (row["username"] + "#" + row["discriminator"])
                        ,row["level"],row["detailed_xp"][0],row["detailed_xp"][1]))
                await ctx.send(embed=discord.Embed(title="MEE6 LeaderBoard",description="\n".join(l),color=0x05FF05))
def setup(bot):
    bot.add_cog(MEE6(bot))
