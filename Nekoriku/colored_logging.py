import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """
    TH:
    `ColoredFormatter` เป็นคลาสที่ใช้เพื่อเพิ่มสีให้กับข้อความที่บันทึกด้วย logging ใน Python โดยการเปลี่ยนสีของข้อความตามระดับความสำคัญของ 
    log เช่น DEBUG, INFO, WARNING, ERROR, หรือ CRITICAL ซึ่งช่วยให้การอ่านและแยกแยะข้อความ log ในคอนโซลทำได้ง่ายขึ้น

    EN:
    `ColoredFormatter` It is a class used to add color to text recorded with logging in Python by changing the color of the text based on its importance level. 
    log such as DEBUG, INFO, WARNING, ERROR, or CRITICAL, which makes it easier to read and distinguish log messages in the console.

    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    def __init___(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)

    def format(self, record):
        """
        TH:
        จัดรูปแบบบันทึกการล็อกด้วยสีสำหรับแต่ละส่วน"

        EN:
        Format the log record with colors for different components.

        TH / EN:
        **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
        **As for other languages You can continue adding it yourself. If you are a translator**
        """
        if record.levelname == "DEBUG":
            levelname_color = Fore.LIGHTBLUE_EX
        elif record.levelname == "INFO":
            levelname_color = Fore.LIGHTMAGENTA_EX
        elif record.levelname == "WARNING":
            levelname_color = Fore.LIGHTYELLOW_EX
        elif record.levelname == "ERROR":
            levelname_color = Fore.RED
        elif record.levelname == "CRITICAL":
            levelname_color = Fore.MAGENTA
        else:
            levelname_color = Fore.WHITE
        
        message_color = Fore.WHITE
        asctime_color = Fore.LIGHTGREEN_EX
        name_color = Fore.LIGHTYELLOW_EX

        def colorize(text: str, color: str) -> str:
            """
            TH:
            เพิ่มสีให้กับข้อความที่กำหนด

            EN:
            Apply color to the given text.
            
            TH / EN:
            **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
            **As for other languages You can continue adding it yourself. If you are a translator**
            """
            return f"{color}{text}{Style.RESET_ALL}"

        formatted_message = super().format(record)

        formatted_message = formatted_message.replace(record.levelname, colorize(record.levelname, levelname_color))
        formatted_message = formatted_message.replace(record.message, colorize(record.message, message_color))
        formatted_message = formatted_message.replace(record.asctime, colorize(record.asctime, asctime_color))
        formatted_message = formatted_message.replace(record.name, colorize(record.name, name_color))

        return formatted_message

def get_logger(name: str):
    """
    TH:
    `get_logger` เป็นฟังก์ชันที่สร้างและคืนค่าตัวจัดการ log (logger) ที่กำหนดค่าแล้ว ซึ่งพร้อมใช้งานสำหรับการบันทึกข้อความ 
    log ไปยังคอนโซล โดยจะติดตั้งการจัดรูปแบบข้อความที่มีสีสันเพื่อให้สามารถแยกแยะระดับของ log ได้ง่ายขึ้น

    EN:
    `get_logger` is a function that creates and returns a configured log handler (logger). Available for logging 
    log messages to the console, it implements colorful text formatting to make log levels easier to distinguish.
    
    TH / EN:
    **ภาษาอื่นๆ คุณสามารถมาเพิ่มต่อเองได้นะ**
    **As for other languages You can continue adding it yourself. If you are a translator**
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        formatter = ColoredFormatter('[%(asctime)s] -> [%(levelname)s] -> %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger