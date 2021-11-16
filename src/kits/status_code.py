# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class Code(Enum):
    FEEDBACK = (400, '')  # 用于给前端提示，不能使用200，否则不会触发前端组件提示
    SUCCESS = (200, 'success')
    UNAUTHORIZED = (401, '身份认证信息未提供。')
    FORBIDDEN = (403, '无权限')
    NOT_FOUND = (404, '无法找到页面')
    METHODNOTSUPPORT = (405, "请求方式不允许")

    # 全局的业务代码，以 10 开头
    SYSTEM_ERROR = (500, '服务器开小差了，请稍后重试~')
    PARAM_MISS = (10102, '参数错误！')
    PARAM_ERROR = (10101, '参数错误！')
    OVER_FLOW = (10103, '超出访问次数限制！')
    NO_AUTH = (10201, '没有权限！')
    NO_USER = (10202, '获取不到用户！')
    NO_COMPANY = (10203, '获取不到该用户的企业！')
    intranet_limit = (10103, "内部接口请求id不能超过100！")
    uuid_error = (10103, "参数不是UUID！")

    # 导入文件报错
    over_limit_lines = (299993, "您导入的文件数据行过大，请拆分后再执行导入。确保每个文件内容不超过1万行有效数据")
    import_empty_error = (500005, "导入的文件数据为空")
    import_fail = (500006, "导入失败，数据错误，请重新检查或稍后重试")
    not_found_data_id = (500007, "您导入的文件无效，无法完成更新")
    import_template_error = (124010, '导入的文件格式错误')
    non_standard_template = (500008, '模板有误，请下载系统标准模板')

    # 导出文件报错
    fail_load_file = (230006, "文件加载失败")
    file_update_fail = (230002, "异动记录文件上传失败")
    FILE_UPLOAD_FAIL = (230002, u'七牛文件上传失败')
    FILE_DOWNLOAD_FAIL = (230003, u'七牛文件下载失败')

    # api 接口 300 开头

    # employee 接口 500 开头

    # 内部接口 600 开头
