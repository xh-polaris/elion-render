from enum import Enum


class ErrorCode(Enum):
    """
    ErrorCode 错误码枚举类
    业务过程中遇到并抛出的业务异常，需要在这里定义好错误码和错误信息的枚举项
    """
    # Render 相关
    DEFAULT_RENDER = (2000, "Render Error")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
