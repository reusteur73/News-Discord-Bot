import discord
from discord.ext import commands, tasks
import requests, random

BOT_TOKEN = "bot_token"
API = "api_key"

class NewsLinks(discord.ui.View):
    def __init__(self, ctx: discord.Interaction, links: list):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.links = links

        for i, link in enumerate(self.links):
            self.button = discord.ui.Button(label=f"{i}.", style=discord.ButtonStyle.link, url=link)
            self.add_item(self.button)

def get_random_news():
    """
    return list of list of random new articles
    """
    # url = "https://api.newscatcherapi.com/v2/latest_headlines"

    # querystring = {"when":"16h","lang":"fr","page":"1", "countries": "fr", "page_size": 75}

    # headers = {
    #     "x-api-key": API
    #     }
    # response = requests.request("GET", url, headers=headers, params=querystring).json()
    # print(response)
    # response = response['articles']
    # unique_articles = [dict(t) for t in {tuple(d.items()) for d in response}]
    # i = 0
    new_articles = {}
    # for article in unique_articles:
    #     if article["excerpt"]:
    #         if (len(article["title"]) < 256) and (len(article["title"]) < 1000):
    #             new_articles[i] = [article["title"], article["excerpt"], article["link"]]

    #             i+=1
    # return random.choices(new_articles, k=5)

    
    for i in range(0,5):
        new_articles[i] = [f"arcticle{i+1}", f"arcticle{i+1}", f"https://www.article{i+1}.com"] # since my api limit is reach LoL
    return new_articles

def create_news_embed(news: list):
    """
    return an embed of news articles
    """
    fields = []
    links = []
    print(news)
    for key, val in news.items():
        fields.append({"name": f"{key+1}. {val[0]}", "value": f"- {val[1]}", "inline": False})
        links.append(val[2])

    embed = create_embed(title="Les news", description="", fields=fields)
    return embed, links

def create_embed(title: str, description: str, color=discord.Color.blue(), author=None, thumbnail=None, fields: list=None, footer=None, suggestions: list=None):
    """
        Fields must be :
            [
                {"name": "dataname1", "value": "datavalue1", "inline": False}
            ]
    """
    embed = discord.Embed(title=title, description=description, color=color)
    
    if author:
        embed.set_author(name=author["name"], icon_url=author["icon_url"])
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if fields:
        if len(fields) > 1:
            for i, field in enumerate(fields):
                embed.add_field(name=fields[i]["name"], value=fields[i]["value"], inline=fields[i]["inline"])
        else:
            field = fields[0]
            embed.add_field(name=fields["name"], value=fields["value"], inline=fields["inline"])
    if footer:
        embed.set_footer(text=footer["text"], icon_url=footer["icon_url"])
    else:
        embed.set_footer(text=f"Articles from newscatcherapi.com")
    return embed

intents = discord.Intents()

intents.guilds = True  
intents.members = True 
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.reactions = True
bot = commands.Bot(command_prefix='.', intents=intents)

@tasks.loop(hours=2)
async def send_news():
    news = get_random_news()

    embed, links = create_news_embed(news)

    view = NewsLinks(links=links, ctx=discord.Interaction)

    channel = bot.get_channel("channel id")

    return await channel.send(embed=embed, view=view)    


@bot.event
async def on_ready():
    await bot.tree.sync()
    send_news.start()
    print(f"Logged in as {bot.user}.")

@bot.tree.command(name="news-dev", description=".")
async def newTest(ctx: discord.Interaction):
    news = get_random_news()

    embed, links = create_news_embed(news)

    view = NewsLinks(links=links, ctx=ctx)

    return await ctx.response.send_message(embed=embed, view=view)    


bot.run(BOT_TOKEN)