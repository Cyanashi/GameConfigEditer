#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time

APP_CONFIG = {}
PROPERTY_CODE = {}
SAVE_NEW_CONTENT = {}
SAVE_NEW = {}


def mv(src, dst):
    try:
        os.rename(src, dst)
    except Exception as e:
        print(e)
        print("<Error>: Rename fail! %s" % src)
    else:
        pass  # print("<Info> : Rename success! %s" % src)


def init():
    global APP_CONFIG, SAVE_NEW_CONTENT, SAVE_NEW
    APP_CONFIG = get_app_config()
    APP_CONFIG['Save'] = os.path.join(APP_CONFIG['Root'], APP_CONFIG['Save'])
    read_property()
    SAVE_NEW_CONTENT = read_save_new()
    SAVE_NEW = SAVE_NEW_CONTENT['_allSaveActors'].popitem()[1]
    os.chdir(APP_CONFIG['Save'])  # 切换到 对应 目录
    print("<Info> : 当前工作目录 [ %s ]" % os.getcwd())


def get_app_config(local_config="config"):
    try:  # print("尝试读取 %s.json" % local_config)
        with open('./' + local_config + '.json', 'r', -1, 'utf-8') as f:
            config_data = json.load(f)
        return config_data
    except json.decoder.JSONDecodeError:
        print("<Error>: 校验铭刻存档文件成功<%s>json格式失败" % local_config)
        print("[ tips ] 请确认%s为合法json格式" % local_config)
    except UnicodeDecodeError:
        print("<Error>: 校验铭刻存档文件成功<%s>编码格式失败" % local_config)
        print("[ tips ] 请确认%s编码格式为utf-8" % local_config)
    except IOError:
        print("<Error>: 读取铭刻存档文件成功<%s>失败" % local_config)
        print("[ tips ] 请重新尝试读取%s" % local_config)
    return None


def read_property():
    global PROPERTY_CODE
    try:
        with open('./特质代码参考.txt', 'r', -1, 'utf-8') as lines:
            property_code = {}
            for line in lines:
                if line != '\n':
                    key, value = line.split(",", 2)
                    # TODO 找出下面这个问题究竟是什么原因导致的
                    """
                    test = "print(test.stirp()) : test不是你妈的字符串吗 凭什么test.strip()就你妈没问题\n"
                    if type(test) == type(value):
                        print("难道 test类型%s 跟 value类型%s 两个字符串类型他妈的不一样吗\n要是真他妈的不一样就不会过 "
                              "if type(test) == type(value) 的判断然后他妈的打印这一句\n" % (type(test), type(value)))
                    print(test.strip())
                    try:
                        print(value.stirp())
                    except AttributeError:
                        print("print(value.stirp()): value不是你妈的字符串吗 "
                              "凭什么就你妈要报错AttributeError: 'str' object has no attribute 'stirp'")
                        exit(-1)
                    """
                    PROPERTY_CODE[key] = value.replace('\n', '')
    except UnicodeDecodeError:
        print("<Error>: 校验特质代码参考.txt编码UTF-8失败")
    except IOError:
        print("<Error>: 读取特质代码参考.txt失败")
    return None


def read_save_new():
    config_path = os.path.join(APP_CONFIG['Save'], APP_CONFIG['SaveActorNew'])
    try:
        with open(config_path, 'r', -1, 'utf-8') as f:
            save_new = json.load(f)
        # print("<Info> : 读取铭刻存档文件成功 [ %s ]" % config_path)
        return save_new
    except json.decoder.JSONDecodeError:
        print("<Error>: 校验铭刻存档文件json格式失败")
        print("[ tips ] 请确认%s为合法json格式" % config_path)
    except UnicodeDecodeError:
        print("<Error>: 校验铭刻存档文件编码格式失败")
        print("[ tips ] 请确认%s编码格式为utf-8" % config_path)
    except IOError:
        print("<Error>: 读取铭刻存档文件失败")
        print("[ tips ] 请重新尝试读取%s" % config_path)
    return None


def backup_game_config(origin_path):
    file_path, temp_filename = os.path.split(origin_path)
    file_name, file_type = os.path.splitext(temp_filename)
    backup_file = file_name + ".backup" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_type
    mv(origin_path, os.path.join(file_path, backup_file))
    print("\n<Info> : 旧的铭刻存档文件成功已备份为 %s" % os.path.join(file_path, backup_file))


def write_game_config(json_dict):
    config_path = os.path.join(APP_CONFIG['Root'], APP_CONFIG['setting'])
    backup_game_config(config_path)
    try:
        with open(config_path, "a+", -1, 'utf-8') as f:
            f.write(json.dumps(json_dict, indent=4))
            # json.dump(json_dict, f)
    except IOError:
        print("<Error>: 写入输出游戏配置失败! %s" % config_path)


def process(debug=False):
    print()
    print("姓名: %s 寿命%s" % (SAVE_NEW['5'] + ' ' + SAVE_NEW['0'], SAVE_NEW['13']))
    print("主要属性: 膂力%s 体质%s 灵敏%s 根骨%s 悟性%s 定力%s" % (
        SAVE_NEW['-61'], SAVE_NEW['-62'], SAVE_NEW['-63'], SAVE_NEW['-64'], SAVE_NEW['-65'], SAVE_NEW['-66']))
    print("技艺资质: 音律%s 弈棋%s 诗书%s 绘画%s 术数%s 品鉴%s 锻造%s 制木%s 医术%s 毒术%s 织锦%s 巧匠%s 道法%s 佛学%s 厨艺%s 杂学%s" % (
        SAVE_NEW['-501'], SAVE_NEW['-502'], SAVE_NEW['-503'], SAVE_NEW['-504'], SAVE_NEW['-505'], SAVE_NEW['-506'],
        SAVE_NEW['-507'], SAVE_NEW['-508'], SAVE_NEW['-509'], SAVE_NEW['-510'], SAVE_NEW['-511'], SAVE_NEW['-512'],
        SAVE_NEW['-513'], SAVE_NEW['-514'], SAVE_NEW['-515'], SAVE_NEW['-516']))
    print("功法资质: 内功%s 身法%s 绝技%s 拳掌%s 指法%s 腿法%s 暗器%s 剑法%s 刀法%s 长兵%s 奇门%s 软兵%s 御射%s 乐器%s" % (
        SAVE_NEW['-601'], SAVE_NEW['-602'], SAVE_NEW['-603'], SAVE_NEW['-604'], SAVE_NEW['-605'], SAVE_NEW['-606'],
        SAVE_NEW['-607'], SAVE_NEW['-608'], SAVE_NEW['-609'], SAVE_NEW['-610'], SAVE_NEW['-611'], SAVE_NEW['-612'],
        SAVE_NEW['-613'], SAVE_NEW['-614']))
    have_property_temp = ""
    have_property_code = SAVE_NEW['101'].split('|')
    for item in have_property_code:
        if item in PROPERTY_CODE:
            have_property_temp += PROPERTY_CODE[item] + '|'
        else:
            have_property_temp += item + '|'
    have_property_temp = have_property_temp.rstrip('|')
    print("出生特质: %s" % have_property_temp)


def main():
    init()
    # print(APP_CONFIG)  # 显示本地配置项
    print("<Info> : 读取游戏铭刻存档文件成功... [%s]" % os.path.join(APP_CONFIG['Save'], APP_CONFIG['SaveActorNew']))
    process()
    # 更新mod https://github.com/phorcys/Taiwu_mods/releases
    return
    write_game_config(SAVE_NEW)
    print("<Info> : 修改结束! 可直接退出或继续修改...")


if __name__ == "__main__":
    main()
