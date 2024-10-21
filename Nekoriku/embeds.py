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
    def server_only(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ให้ว่าคำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น

           Embed ประกอบด้วย:
           - ชื่อ: "This command can only be used on the server."
           - คำอธิบายที่กล่าวถึงผู้ใช้ว่าคำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น
           - สีชมพูอ่อน

        EN:
            Creates an embed to addressed to the user states that this command can only be used on the server.

            The embed includes:
            - A title: "This command can only be used on the server."
            - A description addressed to the user states that this command can only be used on the server.
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="TH: คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น\nEN: This command can only be used on the server.",
            color=0xFFC0CB
        )
        embed.set_author(name='This command can only be used on the server.', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="คำสั่งนี้สามารถใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def serach_limit_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ว่าคำค้นหาต้องไม่เกิน 128 ตัวอักษร

           Embed ประกอบด้วย:
           - ชื่อ: "To prevent search errors"
           - คำอธิบายที่กล่าวถึงผู้ใช้ว่าคำค้นหาต้องไม่เกิน 128 ตัวอักษร
           - สีชมพูอ่อน

        EN:
            Creates an embed to That search terms must not exceed 128 characters.

            The embed includes:
            - A title: "To prevent search errors"
            - A description That search terms must not exceed 128 characters.
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="TH: คำค้นหาต้องไม่เกิน 128 ตัวอักษร.\nEN: Search terms must not exceed 128 characters.",
            color=0xFFC0CB
        )
        embed.set_author(name='To prevent search errors', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="คำค้นหาต้องไม่เกิน 128 ตัวอักษร...", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed

    @staticmethod
    def search_url_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ว่าโปรดป้อนคำค้นหาเป็นชื่อเพลง ไม่ใช่ลิงก์.

           Embed ประกอบด้วย:
           - ชื่อ: "To prevent search errors"
           - คำอธิบายที่กล่าวถึงผู้ใช้ว่าโปรดป้อนคำค้นหาเป็นชื่อเพลง ไม่ใช่ลิงก์.
           - สีชมพูอ่อน

        EN:
            Creates an embed to Please enter your search term as a song title, not a link.
            
            The embed includes:
            - A title: "To prevent search errors"
            - A description Please enter your search term as a song title, not a link.
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="TH: โปรดป้อนคำค้นหาเป็นชื่อเพลง ไม่ใช่ลิงก์.\nEN: Please enter your search term as a song title, not a link.",
            color=0xFFC0CB
        )
        embed.set_author(name='Please enter your search term', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="โปรดป้อนคำค้นหาเป็นชื่อเพลง ไม่ใช่ลิงก์.", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed

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
            Creates an embed to mentioning the user and advising them to join a voice channel before using the command

            The embed includes:
            - A title: "Join Voice Channel"
            - A description mentioning the user and advising them to join a voice channel before using the command
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="TH: กรุณาเข้าร่วมช่องเสียงก่อนที่จะใช้คำสั่งนี้\nEN: Please join the voice channel before using this command.",
            color=0xFFC0CB
        )
        embed.set_author(name='Join Voice Channel', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กรุณาเข้าช่องเสียงก่อน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def player_voice_channel(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ว่าคุณต้องอยู่ในช่องเสียงเดียวกับหนูเพื่อใช้คำสั่งนี้

           Embed ประกอบด้วย:
           - ชื่อ: "Player Voice Channel"
           - คำอธิบายที่กล่าวถึงผู้ใช้ว่าคุณต้องอยู่ในช่องเสียงเดียวกับหนูเพื่อใช้คำสั่งนี้
           - สีชมพูอ่อน

        EN:
            Creates an embed to states that you must be on the same voice channel as the me to use this command.

            The embed includes:
            - A title: "Player Voice Channel"
            - A description states that you must be on the same voice channel as the me to use this command.
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="คุณต้องอยู่ในช่องเสียงเดียวกับหนูเพื่อใช้คำสั่งนี้\n\nEN: You must be in the same room as me.",
            color=0xFFC0CB
        )
        embed.set_author(name='Player Voice Channel', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="คุณต้องอยู่ห้องเดียวกับหนู..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def create_player_embed(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
           สร้าง embed เพื่อแจ้งผู้ใช้ว่าหนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้

           Embed ประกอบด้วย:
           - ชื่อ: "Create Player"
           - คำอธิบายที่กล่าวถึงผู้ใช้ว่าหนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้
           - สีชมพูอ่อน

        EN:
            Creates an embed to mentioning I'm not connected to the audio channel or can't access the Player.

            The embed includes:
            - A title: "Create Player"
            - A description mentioning I'm not connected to the audio channel or can't access the Player.
            - A light pink color

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="หนูไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้\n\nEN: I am not connected to the audio channel or cannot access the Player.",
            color=0xFFC0CB
        )
        embed.set_author(name='Create Player', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ไม่ได้เชื่อมต่อกับช่องเสียงหรือไม่สามารถเข้าถึง Player ได้..", icon_url=f'{bot.user.display_avatar.url}?size=256')
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
            description=f"เพิ่มเพลง **`{track.title}`** เข้าคิวเพลงแล้ว | ระยะเวลา **`{track_length_formatted}`**",
            color=0xFFC0CB
        )
        embed.set_author(name='Now Playing..', icon_url=f'{member.display_avatar}?size=512')
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
            description='TH: ทำลายเพลงและออกจากช่องเสียงแล้ว\nEN: Destroyed the song and left the sound room.',
            color=0xFFC0CB
        )
        embed.set_author(name='Leave Room Channel Songs', icon_url=f'{member.display_avatar}?size=512')
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
            description="TH: ข้ามไปยังเพลงถัดไปแล้ว\nEN: Skip to the next song.",
            color=0xFFC0CB
        )
        embed.set_author(name='Skip the song', icon_url=f'{member.display_avatar}?size=512')
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
            description=f"เลือกฟิลเตอร์ **`{filter}`** แล้ว.",
            color=0xFFC0CB
        )
        embed.set_author(name='Current song Filters', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ฟิลเตอร์ปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def repeat_music_embed(member: discord.Member, bot: commands.Bot, mode: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับการเลือกโหมดวนเพลงซ้ำ

            Embed ประกอบด้วย:
            - ชื่อ: "Repeat Songs"
            - คำอธิบายที่เลือกโหมดวนเพลงซ้ำ
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about selecting the repeat song mode.
            
            The embed should include:
            - A title: 'Repeat Songs'
            - A description Select the repeat song mode
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description=f"เลือกโหมดวนเพลงซ้ำเป็น **`{mode}`** แล้ว",
            color=0xFFC0CB
        )
        embed.set_author(name='Repeat Songs', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="วนเพลงซ้ำเป็นปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def forward_music_embed(member: discord.Member, bot: commands.Bot, time: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับการกรอเวลาเพลง

            Embed ประกอบด้วย:
            - ชื่อ: "Forward Songs"
            - คำอธิบายที่เลือกเวลาที่ต้องการกรอ
            - สีชมพูอ่อน

        EN:
            Create an embed to inform users about skipping song time.

            The embed should include:
            - A title: 'Forward Songs'
            - A description: Choose the time you want to skip to
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description=f'กรอเพลงไปยัง **`{time}`** แล้ว',
            color=0xFFC0CB
        )
        embed.set_author(name='Forward Songs', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กรอเพลงไปยังจุดปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def forward_music_embed_error(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อผิดพลาดการใช้รูปแบบเวลา

            Embed ประกอบด้วย:
            - ชื่อ: "Forward Songs"
            - คำอธิบายที่แสดงรูปแบบเวลาไม่ถูกต้อง
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about displaying errors in time format usage

            The embed should include:
            - A title: 'Forward Songs'
            - A description: time format is incorrect
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description='รูปแบบเวลาไม่ถูกต้อง กรุณาใช้รูปแบบ 00:00',
            color=0xFFC0CB
        )
        embed.set_author(name='Forward Songs', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กรอเพลงไปยังจุดปัจจุบัน..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def player_autoplay_embed_error(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อผิดพลาดกรุณาเปิดการใช้งาน autoplay

            Embed ประกอบด้วย:
            - ชื่อ: "Autoplay Mode"
            - คำอธิบายที่แสดงข้อผิดพลาดกรุณาเปิดการใช้งาน autoplay
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about displaying an error message: please enable autoplay.

            The embed should include:
            - A title: 'Forward Songs'
            - A description: the error message: please enable autoplay.
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="กรุณาเปิดการใช้งาน autoplay ก่อนที่จะเปิดโหมดวนเพลงซ้ำ",
            color=0xFFC0CB
        )
        embed.set_author(name='Autoplay Mode', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="กรุณาเปิดการใช้งาน autoplay..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def player_autoplay_embed(member: discord.Member, bot: commands.Bot, autoplay_name: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความเลือกโหมด autoplay

            Embed ประกอบด้วย:
            - ชื่อ: "Autoplay Mode"
            - คำอธิบายที่แสดงข้อความเลือกโหมด autoplay
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about selecting autoplay mode.

            The embed should include:
            - A title: 'Forward Songs'
            - A description: the message: select autoplay mode.
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description=f"เลือกโหมด **`{autoplay_name}`** แล้ว",
            color=0xFFC0CB
        )
        embed.set_author(name='Autoplay Mode', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="เลือกโหมด autoplay..", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def volume_music_embed(member: discord.Member, bot: commands.Bot, volume: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความปรับระดับเสียง

            Embed ประกอบด้วย:
            - ชื่อ: "Volume Set"
            - คำอธิบายที่แสดงข้อความปรับระดับเสียง
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about the volume adjustment message.

            The embed should include:
            - A title: 'Volume Set'
            - A description: displaying the volume adjustment message
            - A light pink color"
            
        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description=f"ปรับระดับเสียงเป็น **`{volume}%`** แล้ว",
            color=0xFFC0CB
        )
        embed.set_author(name='Volume Set', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ปรับระดับเสียงเพลง", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def volume_music_embed_else(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความกรุณาใส่ระดับเสียงที่ถูกต้อง

            Embed ประกอบด้วย:
            - ชื่อ: "Volume Set"
            - คำอธิบายที่แสดงข้อความกรุณาใส่ระดับเสียงที่ถูกต้อง
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about the message asking them to provide a valid volume level.

            The embed should include:
            - A title: 'Volume Set'
            - A description: displaying the message asking to provide a valid volume level
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="กรุณาใส่ระดับเสียงที่ถูกต้องระหว่าง 0 ถึง 100",
            color=0xFFC0CB
        )
        embed.set_author(name='Volume Set', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ปรับระดับเสียงเพลง", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def volume_music_embed_error(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความกรุณาใส่ค่าระดับเสียงเป็นตัวเลข

            Embed ประกอบด้วย:
            - ชื่อ: "Volume Set"
            - คำอธิบายที่แสดงข้อความกรุณาใส่ค่าระดับเสียงเป็นตัวเลขที่ถูกต้อง
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about the message asking them to enter a numeric volume value.

            The embed should include:
            - A title: 'Volume Set'
            - A description: displaying the message asking to enter a correct numeric volume value
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description="กรุณาใส่ค่าระดับเสียงเป็นตัวเลขที่ถูกต้อง",
            color=0xFFC0CB
        )
        embed.set_author(name='Volume Set', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ปรับระดับเสียงเพลง", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def toggle_pause_resume_embed_error(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความไม่มีโหมดที่คุณพิมพ์

            Embed ประกอบด้วย:
            - ชื่อ: "Toggle Mode"
            - คำอธิบายที่แสดงข้อความไม่มีโหมดที่คุณพิมพ์
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about the message stating that the mode you typed does not exist.

            The embed should include:
            - A title: 'Toggle Mode'
            - A description: showing the message that the mode you typed does not exist
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description='ไม่มีโหมดที่คุณพิมพ์มา "pause" หรือ "resume"',
            color=0xFFC0CB
        )
        embed.set_author(name='Toggle Mode', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="สลับโหมด pause หรือ resume", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def toggle_pause_resume_embed(member: discord.Member, bot: commands.Bot, toggle_mode: str) -> discord.Embed:
        """
        TH:
            สร้าง embed เพื่อแจ้งผู้ใช้เกี่ยวกับแสดงข้อความคุณเลือกโหมดแล้ว

            Embed ประกอบด้วย:
            - ชื่อ: "Toggle Mode"
            - คำอธิบายที่แสดงข้อความคุณเลือกโหมดแล้ว
            - สีชมพูอ่อน

        EN:
            Create an embed to notify users about the message stating that you have selected a mode.

            The embed should include:
            - A title: 'Toggle Mode'
            - A description: showing the message that you have selected a mode
            - A light pink color"

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        embed = discord.Embed(
            description=f'คุณเลือกโหมด **`{toggle_mode}`** แล้ว',
            color=0xFFC0CB
        )
        embed.set_author(name='Toggle Mode', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="สลับโหมด pause หรือ resume", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed

    @staticmethod
    def no_player_found_in_voice(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        embed = discord.Embed(
            description=f'TH: ไม่พบผู้เล่นในช่องเสียง\nEN: No player found in voice channel',
            color=0xFFC0CB
        )
        embed.set_author(name='No player found in voice channel', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ไม่พบผู้เล่นในช่องเสียง", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed
    
    @staticmethod
    def no_songs_found_list(member: discord.Member, bot: commands.Bot) -> discord.Embed:
        embed = discord.Embed(
            description=f'TH: ไม่พบเพลงในรายการ\nEN: No songs found in the list.',
            color=0xFFC0CB
        )
        embed.set_author(name='No songs found in the list', icon_url=f'{member.display_avatar}?size=512')
        embed.set_footer(text="ไม่พบเพลงในรายการ", icon_url=f'{bot.user.display_avatar.url}?size=256')
        return embed