import logging

def setup_logger(name: str = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # 重複防止
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


        # コンソールにも出力
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger