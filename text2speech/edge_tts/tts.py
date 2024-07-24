import os
import asyncio
import utils.utils as proj_utils
import edge_tts
from edge_tts import VoicesManager

TEXT = "副总统哈里斯作为民主党可能的总统候选人，近期筹款活动取得巨大成功，收到超1.4亿美元的捐款。最大支持者集团筹得了巨额承诺资金，显示出新的活力。虽然存在一些捐赠人的分歧"
VOICE = "zh-CN-YunyangNeural"
OUTPUT_FILE = "speech.mp3"
WEBVTT_FILE = "subtitle.vtt"


async def speech_with_subtitles(text, folder_path) -> None:
    """Main function"""
    if not os.path.exists(folder_path):
        # 如果文件夹不存在，则创建
        os.makedirs(folder_path)
    # voices = await VoicesManager.create()
    # voice = voices.find(Gender="Male", Language="es")
    communicate = edge_tts.Communicate(text, VOICE)
    sub_maker = edge_tts.SubMaker()
    with open(folder_path + OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(folder_path + WEBVTT_FILE, "w", encoding="utf-8") as file:
        file.write(folder_path + sub_maker.generate_subs())


if __name__ == "__main__":
    asyncio.run(speech_with_subtitles(TEXT, 'generate/debug/'))
