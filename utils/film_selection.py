import discord
from discord.ui import View, Button

class FilmSelectionView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.response = None

    @discord.ui.button(label="❌", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Você não pode interagir com esse filme", ephemeral=True)
            return
        
        await interaction.response.defer()
        self.response = False
        self.stop()
    
    @discord.ui.button(label="✅", style=discord.ButtonStyle.gray)
    async def select(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Você não pode interagir com esse filme", ephemeral=True)
            return
        
        await interaction.response.defer()
        self.response = True
        self.stop()

