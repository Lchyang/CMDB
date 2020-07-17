import json
import time
import urllib.parse
import urllib.request
from core import info_collection
from conf import setting


class ArgvHandler:
    """
    处理参数
    """

    def __init__(self, argv):
        self.argv = argv
        self.handler_arg()

    def handler_arg(self):
        print("准备分析参数")
        if len(self.argv) > 1 and hasattr(self, self.argv[1]):
            func = getattr(self, self.argv[1])
            func()
        else:
            self.help_message()

    @staticmethod
    def help_message():
        """
        帮助说明
        """
        msg = '''
                参数名               功能

            collect_data        测试收集硬件信息的功能

            report_data         收集硬件信息并汇报
            '''
        print(msg)

    @staticmethod
    def collect_data():
        """收集硬件信息,用于测试！"""
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        print(asset_data)

    @staticmethod
    def report_data():
        """
        收集硬件信息，然后发送到服务器。
        :return:
        """
        # 收集信息
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        # 将数据打包到一个字典内，并转换为json格式
        data = {"asset_data": json.dumps(asset_data)}
        # 根据settings中的配置，构造url
        url = "http://%s:%s%s" % (setting.Params['server'], setting.Params['port'], setting.Params['url'])
        print('正在将数据发送至： [%s]  ......' % url)
        try:
            # 使用Python内置的urllib.request库，发送post请求。
            # 需要先将数据进行封装，并转换成bytes类型
            data_encode = urllib.parse.urlencode(data).encode()
            response = urllib.request.urlopen(url=url, data=data_encode, timeout=setting.Params['request_timeout'])
            print("\033[31;1m发送完毕！\033[0m ")
            message = response.read().decode()
            print("返回结果：%s" % message)
        except Exception as e:
            message = '发送失败' + "   错误原因：  {}".format(e)
            print("\033[31;1m发送失败，错误原因： %s\033[0m" % e)
        # 记录发送日志
        with open(setting.PATH, 'ab') as f:  # 以byte的方式写入，防止出现编码错误
            log = '发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n' % (time.strftime('%Y-%m-%d %H:%M:%S'), url, message)
            f.write(log.encode())
            print("日志记录成功！")


if __name__ == "__main__":
    ArgvHandler.report_data()
