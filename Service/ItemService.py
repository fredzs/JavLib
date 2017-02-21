import logging
import os
from functools import reduce
from urllib.request import urlretrieve

from Entity.Config import Config
from Entity.Statistic import Statistic
from Entity.Status import Status
from Utility.Utility import Utility


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
                urlretrieve(item.get_img_src, path)
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
