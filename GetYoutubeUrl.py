from playwright.sync_api import sync_playwright



def on_load():
    print("页面加载完成！")


def getYoutubeUrl(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # 导航
    page.goto("https://www.yudou66.com/")

    page.on('domcontentloaded', on_load)
    # 点击进入最新的一个免费分享
    page.locator('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a').wait_for(state="attached")      # 等待 元素出现
    yudouAElement = page.locator('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a')                 # 最新的一个今日分享A元素
    yudouUrl = yudouAElement.get_attribute("href")                                                 # 最新的一个今日分享A元素的url链接地址




    page.goto(yudouUrl)
    page.locator('//*[@id="post-body"]/p[8]/a').wait_for(state="attached")                         # 等待 元素出现
    youtubeAElement = page.locator('//*[@id="post-body"]/p[8]/a')                                  # 获取youtube视频链接A元素
    youtubeUrl = youtubeAElement.get_attribute("href")                                             # 获取youtube视频链接A元素 url
    print(youtubeUrl)
    print(youtubeUrl)
    browser.close()
    return youtubeUrl

if __name__ == '__main__':
    with sync_playwright() as p:
        youtubeUrl = getYoutubeUrl(p)