import news_material.washington_post.api as wp_api
import llm.baidu.baidu as baidu
import text2speech.edge_tts.tts as edge_tts
import utils.utils as proj_utils
import asyncio


def main():
    print('start fetch news...', end="\n")
    parse_result = wp_api.get_headline_news()
    if parse_result.title == "" or parse_result.url == "":
        print("Get invalid news from washington post, please check code")
    print("washington post:" + str(parse_result))
    print('fetch news success', end="\n")
    print('start get summary...', end="\n")
    llm_out = baidu.get_llm_summary(" ".join(parse_result.content))
    print("[baidu] llm_out:" + llm_out)
    if llm_out == '':
        print('get summary failed...', end="\n")
        return ""
    print('get summary success...', end="\n")
    print('start text to speech...', end="\n")
    asyncio.run(edge_tts.speech_with_subtitles(llm_out, 'text2speech/edge_tts/generate/' +
                                               proj_utils.get_current_date().strftime("%Y-%m-%d") + '/'))
    print('text to speech success', end="\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('program start...', end="\n")
    main()
    print('program end...', end="\n")
