import discord
from discord.ui import Button, View

class PaginationView(View):
    def __init__(self, items, ctx):
        super().__init__()
        self.items = items
        self.ctx = ctx
        self.per_page:int = 10
        self.current_page:int = 0
        self.total_pages = (len(items) - 1) // self.per_page

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.items)

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.items)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.items)

    def create_embed(self, data):
        start = self.current_page * self.per_page
        end = start + self.per_page
        items = data[start:end]
        
        embed = discord.Embed(
            title="🎬 Filmes Adicionados",
            color=discord.Color.dark_gray()
        )
        embed.set_footer(text=f"Página {self.current_page + 1}/{self.total_pages + 1}")

        for i, item in enumerate(items, start=start + 1):
            embed.add_field(name=f"{i}. {item[0]}", value=f"⏳ {item[1]} - ⭐ {item[3]}", inline=False)

        return embed
    
    def update_buttons(self):
        self.children[0].disabled = self.current_page == 0
        self.children[1].disabled = self.current_page == self.total_pages