from setuptools import setup, find_packages

setup(
    name="nekoriku",
    version="0.1",
    description="แพ็คเกจสำหรับบอทดิสคอร์ดที่มีฟีเจอร์คำสั่งสำหรับเล่นเพลงครบถ้วน",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'discord.py',
        'wavelink',
        'colorama'
    ],
    author="NekoSakuraLucia",
    packages=find_packages(),
    url="https://github.com/NekoSakuraLucia/Nekoriku",
    python_requires=">=3.10"
)