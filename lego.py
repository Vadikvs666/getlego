import pathlib
from urllib import request, error
import argparse
import logging
import datetime
import sys
import time
import  socket

socket.setdefaulttimeout(30)

logger = logging.getLogger("FileLog")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(datetime.date.today().__str__() + ".log")
handler_sys = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler_sys.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(handler_sys)
logger.setLevel("INFO")

parser = argparse.ArgumentParser()
parser.add_argument("--dest_folder", required=False, help="Insert destination folder name ", default="image")
parser.add_argument("--lego", required=False, help="Lego number ", default="42092")
parser.add_argument("--start_image", type=int, required=False, help="start image ", default="1")
parser.add_argument("--end_image", type=int, required=False, help="end image ", default="200")
parser.add_argument("--base_url", required=False, help="base url ", default="https://media.brickinstructions.com")
args = parser.parse_args()


def get_image(url, dest):
    try:
        logger.info("Get image -  " + url)
        local_file, response_headers = request.urlretrieve(url, dest)
    except OSError as er:
         logger.error("Erorr while downloding")
    except error.ContentTooShortError as shortError:
        logger.error("content too short error")
    except error.HTTPError as e:
        logger.error(e)
    except error.URLError as ue:  # such as timeout
        logger.error("fail to download!")
    except socket.timeout as se:  # very important
        logger.error("socket timeout")
    except Exception as ee:
        logger.error(ee)


def get_lego_url(lego):
    lego_series = int(lego) // 1000 * 1000
    return args.base_url + "/" + lego_series.__str__() + "/" + lego + "/"


def create_image_dest(dest, image):
    image_dest = dest + "\\" + args.lego
    if not pathlib.Path(image_dest).exists():
        try:
            logger.info("Creating destination folder :" + pathlib.Path(image_dest).name)
            pathlib.Path(image_dest).mkdir()
        except OSError as er1:
            logger.error(
                "Permission error. Exit" + pathlib.Path(image_dest).__str__())
            sys.exit(1)
    return image_dest + "\\" + image


def gen_image_name(i):
    str_i = i.__str__()
    str_with_null = ""
    for j in range(len(str_i), 3):
        str_with_null = str_with_null + "0"
    return str_with_null + str_i + ".jpg"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info("Start downloding lego number - " + args.lego + " base url - " + args.base_url + "from start image - " +
                args.start_image.__str__() + " to end image - " + args.end_image.__str__())
    for i in range(args.start_image, args.end_image):
        image = gen_image_name(i)
        url = get_lego_url(args.lego) + image
        dest_file = create_image_dest(args.dest_folder, image)
        logger.info("start url - " + url + " to file  - " + dest_file.__str__())
        get_image(url, dest_file)
        time.sleep(3)
    logger.info("Stop script" + args.lego)