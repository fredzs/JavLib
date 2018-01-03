import logging
import os
from functools import reduce
import requests
from urllib.request import urlretrieve

from Entity.Config import Config
from Entity.Statistic import Statistic
from Entity.Status import Status
from Utility.Utility import Utility

headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': "zh-CN,zh;q=0.8,pt;q=0.6,en;q=0.4,th;q=0.2",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Referer': "http://www.javlibrary.com/cn/",
        'Upgrade-Insecure-Requests': "1",
        'Connection': "keep-alive",
        'Host': "www.javlibrary.com"
}
proxies = dict(http='socks5://127.0.0.1:1080', https='socks5://127.0.0.1:1080')

class ItemService(object):
    # 下载图片到本地
    @staticmethod
    def save_image(item, dst_dir):
        item.tidy_title()
        download_path = Utility.get_download_path(dst_dir, item.get_key)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        path = download_path + item.get_title + ".jpg"
        save_times = 3
        result = Status.SAVE_FAILED
        for i in range(0, save_times):
            try:
                #urllib.request.urlretrieve(item.get_img_src, path)

                item_image = requests.get(item.get_img_src, headers=headers, proxies=proxies, stream=True)
                with open(path, mode='wb') as f:
                    for chunk in item_image.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
            except Exception as e:
                Statistic.download_failed()
                logging.error("\t图片保存失败!")
                logging.error(e)
                continue
            else:
                Statistic.download_success()
                logging.info('\t图片保存成功')
                result = Status.SUCCESS
            finally:
                return result

    @staticmethod
    def write_database(item, worksheet):
        ws_rows = worksheet.max_row + 1
        try:
            worksheet.cell(row=ws_rows, column=1).value = item.get_key
            worksheet.cell(row=ws_rows, column=2).value = item.get_code
            worksheet.cell(row=ws_rows, column=3).value = item.get_title
            worksheet.cell(row=ws_rows, column=4).value = item.get_date
            worksheet.cell(row=ws_rows, column=5).value = item.get_rank
            worksheet.cell(row=ws_rows, column=6).value = item.get_duration
            worksheet.cell(row=ws_rows, column=7).value = item.get_link
            worksheet.cell(row=ws_rows, column=8).value = item.get_actor
        except Exception as e:
            logging.error("发生错误" + item.get_code)
            logging.error(e)
        finally:
            pass

    @staticmethod
    def parse_html(item):
        soup = item.get_soup
        try:
            item.set_title(str(soup.find("div", id='video_title').a.string))
            item.set_img_src(soup.find("div", id='video_jacket').img.get("src"))
            item.set_date(soup.find("div", id='video_date').table.tr.findAll('td')[1].text)
            if soup.find("div", id='video_review') is not None:
                item.set_rank(soup.find("div", id='video_review').table.tr.findAll('span', class_="score")[0].text[1:5])
            item.set_link(soup.find("link", rel='shortlink').get("href").split('=')[1])
            item.set_duration(int(soup.find("div", id='video_length').table.tr.findAll('td')[1].span.text))

            actor = soup.find("div", id='video_cast').findAll('span', class_='star')
            if len(actor) > 0:
                actor = actor[0:19]
                item.set_actor(reduce(lambda x, y: x + ',' + y, list(map(lambda x: x.text, actor))))
            else:
                item.set_actor("")
            return True
        except Exception as e:
            logging.error("解析soup错误！")
            logging.error(e)
            return False
