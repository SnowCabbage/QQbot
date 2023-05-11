import logging

logger = logging.getLogger("Mylogger")  # 定义一个logger
logger.setLevel(logging.INFO)  # 设置等级限制

ch = logging.StreamHandler()  # 定义一个处理器
ch.setLevel(logging.INFO)  # 设置处理器的等级限制

# 设置格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)  # 为处理器装配上格式器，定义输出格式

logger.addHandler(ch)  # 为日志器装配上一个处理器


def main():
    logger.info("Hello World")


if __name__ == '__main__':
    main()
