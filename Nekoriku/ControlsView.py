import discord.ext.commands
import wavelink
import discord

import discord.ext
from .embeds import NekorikuEmbeds

class NekorikuControls(discord.ui.View):
    def __init__(self, bot: discord.ext.commands.Bot, player: wavelink.Player):
        super().__init__()
        self.bot = bot
        self.player = player

        # ปุ่มสำหรับเปิด Autoplay
        self.autoplay_button = discord.ui.Button(label="🎶 Autoplay", style=discord.ButtonStyle.secondary)
        self.autoplay_button.callback = self.toggle_autoplay
        self.add_item(self.autoplay_button)

        # ปุ่มสำหรับเปิด Filters
        self.filters: wavelink.Filters = self.player.filters
        self.select_filter = {
            "🎶 Nightcore": ("ปรับให้เพลงเร็ว และ เสียงร้องแหลมขึ้น", lambda: self.filters.timescale.set(speed=1.2, pitch=1.2, rate=1)),
            "🎶 Slow": ("ปรับให้เพลงช้าขึ้น และ เสียงร้องต่ำลง", lambda: self.filters.timescale.set(speed=0.8, pitch=0.9, rate=1)),
            "🎶 Karaoke": ("ตัดเสียงร้องของเพลงออก เหลือแค่ดนตรี", lambda: self.filters.karaoke.set(level=2, mono_level=1, filter_band=220, filter_width=100)),
            "🎶 Lowpass": ("ปรับให้เพลงสมูทขึ้น และ เพราะขึ้น", lambda: self.filters.low_pass.set(smoothing=20)),
            "🎶 Clear Filters": ("ล้างฟิลเตอร์ทั้งหมดที่คุณเปิดไม่ว่าจะเป็นตัวไหนก็ตาม", lambda: self.filters.reset())
        }

        self.select = discord.ui.Select(
            placeholder="🎶 เลือกฟิลเตอร์..",
            options=[discord.SelectOption(label=name, description=desc, value=name) for name, (desc, _) in self.select_filter.items()]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def toggle_autoplay(self, interaction: discord.Interaction):
        if self.player.autoplay == wavelink.AutoPlayMode.disabled:
            self.player.autoplay = wavelink.AutoPlayMode.enabled
            self.autoplay_button.style = discord.ButtonStyle.green
        else:
            self.player.autoplay = wavelink.AutoPlayMode.disabled
            self.autoplay_button.style = discord.ButtonStyle.secondary
        
        # แก้ใข view
        await interaction.response.edit_message(view=self)

        # ส่งข้อความใหม่เป็น embed
        embed = NekorikuEmbeds.player_autoplay_embed(interaction.user, self.bot, self.player.autoplay.name)
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def select_callback(self, interaction: discord.Interaction):
        selected_filter = self.select.values[0]
        # เรียกใช้งานฟังก์ชั่นการเลือกฟิลเตอร์
        filter_function = None
        for option in self.select.options:
            if option.label == selected_filter:
                filter_function = self.select_filter[option.label][1]
                break

        if filter_function:
            filter_function()
        # เว้นระยะ
        await self.player.set_filters(self.filters)
        embed = NekorikuEmbeds.filters_music_embed(interaction.user, self.bot, selected_filter)
        await interaction.response.send_message(embed=embed, ephemeral=True)