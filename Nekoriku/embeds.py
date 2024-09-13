import discord
from discord.ext import commands
import wavelink
from .utils import Nekoriku_Utils

class NekorikuEmbeds:
    """
    TH: Discord Embed คือฟีเจอร์ที่ช่วยให้คุณสร้างข้อความที่มีรูปแบบสวยงามและมีข้อมูลที่เป็นระเบียบ เช่น รูปภาพ, ลิงก์, และข้อความที่จัดรูปแบบ

    EN: Discord Embed is a feature that allows you to create messages with a visually appealing format, including images, links, and well-structured text.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """

    @staticmethod
    def join_voice_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ให้เข้าร่วมช่องเสียงก่อน

           Embed ประกอบด้วย:
           - ชื่อ: "Join Voice Channel"
           - คำอธิบายที่กล่าวถึงผู้ใช้และแนะนำให้เข้าร่วมช่องเสียงก่อนใช้คำสั่ง
           - สีชมพูอ่อน

        EN:
            Creates an embed to inform the user to join a voice channel first.

            The embed includes:
            - A title: "Join Voice Channel"
            - A description mentioning the user and advising them to join a voice channel before using the command
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            title="Join Voice Channel",
            description=f"{member.mention}\nTH: กรุณาเข้าร่วมช่องเสียงก่อนที่จะใช้คำสั่งนี้\nEN: Please join the voice channel before using this command.",
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กรุณาเข้าช่องเสียงก่อน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def playing_music_embed(member: discord.Member, bot: commands.Bot, track: wavelink.Playable) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับเพลงที่กำลังเล่น

            Embed ประกอบด้วย:
            - ชื่อ: "Now Playing.."
            - คำอธิบายที่กล่าวถึงผู้ใช้และบอกว่ามีเพลง **`{track.title}`** ถูกเพิ่มเข้าคิวเพลงแล้ว
            - สีชมพูอ่อน

        EN:
            Creates an embed to notify the user about the currently playing track.

            The embed includes:
            - A title: "Now Playing.."
            - A description mentioning the user and indicating that the track **`{track.title}`** has been added to the queue
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        track_length_formatted = Nekoriku_Utils.format_duration(track.length)
        embed = discord.Embed(
            title="Now Playing..",
            description=f"{member.mention}\nเพิ่มเพลง **`{track.title}`** เข้าคิวเพลงแล้ว | ระยะเวลา **`{track_length_formatted}`**",
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กำลังเล่นเพลง..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed

    @staticmethod
    def leave_music_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับทำลายเพลง

            Embed ประกอบด้วย:
            - ชื่อ: "Leave Room Channel Music"
            - คำอธิบายที่กล่าวถึงผู้ใช้และบอกว่าทำลายเพลงและออกจากช่องเสียง
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about destroying music.

            The embed should include:
            - A title: 'Leave Room Channel Music
            - A description mentioning the user and stating that the music will be destroyed and the voice channel will be left
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            title="Leave Room Channel Music",
            description=f'{member.mention}\n\nTH: ทำลายเพลงและออกจากช่องเสียงแล้ว\nEN: Destroyed the song and left the sound room.',
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ออกจากช่องเสียงแล้ว..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def skip_music_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับการข้ามเพลง

            Embed ประกอบด้วย:
            - ชื่อ: "Skip the song"
            - คำอธิบายที่กล่าวถึงผู้ใช้และบอกว่าข้ามไปยังเพลงถัดไป
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about skipping a song.

            The embed should include:
            - A title: "Skip the song"
            - A description addressing the user and informing them to skip to the next song
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            title="Skip the song",
            description=f"{member.mention}\n\nTH: ข้ามไปยังเพลงถัดไปแล้ว\nEN: Skip to the next song.",
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ข้ามเพลงแล้ว..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def filters_music_embed(member: discord.Member, bot: commands.Bot, filter: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับการเลือกฟิลเตอร์ของเพลง

            Embed ประกอบด้วย:
            - ชื่อ: "Current song Filters"
            - คำอธิบายที่กล่าวถึงผู้ใช้และบอกว่าเลือกฟิลเตอร์ปัจจุบันแล้ว
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about selecting a song filter.
            
            The embed should include:
            - A title: "Current Song Filters"
            - A description mentioning the user and indicating that the current filter has been selected
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            title="Current song Filters",
            description=f"{member.mention}\n\nเลือกฟิลเตอร์ **`{filter}`** แล้ว.",
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ฟิลเตอร์ปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def repeat_music_embed(member: discord.Member, bot: commands.Bot, mode: str) -> discord.Embed:
        embed = discord.Embed(
            title="Repeat Songs",
            description=f"เลือกโหมดวนเพลงซ้ำเป็น **`{mode}`** แล้ว",
            color=0xFFC0CB
        )
        embed.set_author(name=f'{member.name}', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="วนเพลงซ้ำเป็นปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed