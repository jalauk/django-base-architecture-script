from django.utils.timezone import localtime
from django.conf import settings
from loguru import logger
from .constants import Constant
from pytz import timezone
from .helper import Helper


class Logger:
    base_path = f'{settings.BASE_DIR}/logs/{{time:D-MMM-YYYY}}'

    logger.add(
        f'{base_path}/request.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("request")
    )
    logger.add(
        f'{base_path}/error.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("error")
    )
    logger.add(
        f'{base_path}/custom.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("custom")
    )

    request_log = logger.bind(name="request")
    error_log = logger.bind(name="error")
    custom_log = logger.bind(name="custom")

    @classmethod
    def log(cls, request, response, time_taken=None):
        # if settings.DEBUG:
        #     return None
        current_time = localtime(timezone=timezone(
            "Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        data = f"""
            {current_time} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {request.headers}\n"""
        if time_taken is not None:
            data += f"""STATUS [{response.data.get('status')}] | STATUS_CODE [{response.data.get('code')} ~ {Constant.response_messages[response.data.get('code')]}] | TIME_TAKEN [{round(time_taken, 3)} Seconds]\n"""     # noqa
            data += "\n************************************************************************************************************"   # noqa
            cls.request_log.info(data.replace('  ', ''))
        else:
            data += f"""STATUS [False] | STATUS_CODE [500 ~ Server Error]

            xxxxxxxxxxxxxxxxxxxx [ERROR] xxxxxxxxxxxxxxxxxxxxxxxxxx
            {response}"""
            data += "\n************************************************************************************************************"   # noqa
            cls.error_log.info(data.replace('  ', ''))

    @classmethod
    def custom(cls, request, output):
        current_time = localtime(timezone=timezone(
            "Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        data = f"""
            {current_time} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {request.headers}\n
            ************************************************************************************************************
            {output}
            \n************************************************************************************************************\n
            """
        cls.custom_log.info(data.replace('  ', ''))
