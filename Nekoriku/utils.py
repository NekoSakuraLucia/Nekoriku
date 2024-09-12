import re
from typing import Optional

class Nekoriku_Utils:
    """
    TH:
    คลาส `Nekoriku_Utils` ใช้เพื่อเก็บฟังก์ชันที่ช่วยในการทำงานซึ่งสามารถใช้ได้ทั่วทั้งโค้ด ปัจจุบันมีฟังก์ชันเช่น 
    convert_time ที่แปลงเวลาจากรูปแบบ MM:SS เป็นมิลลิวินาที คลาสนี้ช่วยให้การจัดระเบียบและเข้าถึงฟังก์ชันที่เกี่ยวข้องทำได้ง่าย โดยไม่ต้องสร้างออบเจ็กต์ของคลาส. หรือ อื่นๆ..

    EN:
    The `Nekoriku_Utils` class is used to store utility functions that can be accessed throughout the codebase. Currently, it includes functions like 
    convert_time, which converts time from the MM:SS format to milliseconds. 
    This class helps in organizing and accessing related functions easily without needing to create an instance of the class, and it can also accommodate additional utility functions.
    
    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    @staticmethod
    def convert_time(time_str: str) -> Optional[int]:
        """
        TH:
        ฟังก์ชัน `convert_time` แปลงเวลาจากรูปแบบ MM:SS เป็นมิลลิวินาที ถ้าเวลาที่ให้มาตรงตามรูปแบบ ฟังก์ชันจะคำนวณเป็นมิลลิวินาทีและส่งค่ากลับมา
        ถ้าไม่ตรงตามรูปแบบ จะคืนค่าเป็น None.

        EN:
        The `convert_time` function converts a time string in the format MM:SS into milliseconds. If the input time string matches the format,
        the function calculates the time in milliseconds and returns it. If the format is incorrect, it returns None.

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        match = re.match(r'^(\d{1,2}):(\d{2})$', time_str)
        if not match:
            return None
        
        minutes, seconds = map(int, match.groups())

        total_ms = (minutes * 60 + seconds) * 1000
        return total_ms
    
    @staticmethod
    def format_duration(ms: int) -> str:
        """
        TH:
        ฟังก์ชัน format_duration รับพารามิเตอร์เป็นจำนวนมิลลิวินาที (ms) และแปลงเป็นสตริงที่แสดงเวลาในรูปแบบ HH:MM:SS หรือ MM:SS 
        ขึ้นอยู่กับจำนวนชั่วโมง ถ้ามีชั่วโมงมากกว่าศูนย์ จะคืนค่าในรูปแบบ HH:MM:SS หากไม่มีชั่วโมง ก็จะคืนค่าในรูปแบบ MM:SS

        EN:
        The format_duration function takes a parameter in milliseconds (ms) and converts it into a string that shows time in the format HH:MM:SS or MM:SS, 
        depending on whether there are hours. If there are more than zero hours, it returns the format HH:MM:SS. If there are no hours, it returns the format MM:SS.

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        total_seconds = ms // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"