#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time

APP_CONFIG = {}
GAME_CONFIG = {}
KEY_MAP = {}
KEY_BIND = {}


def mv(src, dst):
    try:
        os.rename(src, dst)
    except Exception as e:
        print(e)
        print("<Error>: Rename fail! %s" % src)
    else:
        pass  # print("<Info> : Rename success! %s" % src)


def init(mode='LOL'):
    global APP_CONFIG, GAME_CONFIG, KEY_MAP, KEY_BIND
    APP_CONFIG = get_app_config()[mode]
    GAME_CONFIG = read_game_config()
    KEY_MAP = get_app_config('key_map')[mode]
    KEY_BIND = get_app_config('key_bind')[mode]
    os.chdir(APP_CONFIG['root'])  # 切换到 对应 目录
    print("<Info> : 当前工作目录 [ %s ]" % APP_CONFIG['root'])


def get_app_config(local_config="config"):
    try:  # print("尝试读取 %s.json" % local_config)
        with open('./' + local_config + '.json', 'r', -1, 'utf-8') as f:
            config_data = json.load(f)
        return config_data
    except json.decoder.JSONDecodeError:
        print("<Error>: 校验配置文件<%s>json格式失败" % local_config)
        print("[ tips ] 请确认%s为合法json格式" % local_config)
    except UnicodeDecodeError:
        print("<Error>: 校验配置文件<%s>编码格式失败" % local_config)
        print("[ tips ] 请确认%s编码格式为utf-8" % local_config)
    except IOError:
        print("<Error>: 读取配置文件<%s>失败" % local_config)
        print("[ tips ] 请重新尝试读取%s" % local_config)
    return None


def read_game_config():
    config_path = os.path.join(APP_CONFIG['root'], APP_CONFIG['setting'])
    try:
        with open(config_path, 'r', -1, 'utf-8') as f:
            game_config = json.load(f)
        return game_config
    except json.decoder.JSONDecodeError:
        print("<Error>: 校验配置文件json格式失败")
        print("[ tips ] 请确认%s为合法json格式" % config_path)
    except UnicodeDecodeError:
        print("<Error>: 校验配置文件编码格式失败")
        print("[ tips ] 请确认%s编码格式为utf-8" % config_path)
    except IOError:
        print("<Error>: 读取配置文件失败")
        print("[ tips ] 请重新尝试读取%s" % config_path)
    return None


def backup_game_config(origin_path):
    file_path, temp_filename = os.path.split(origin_path)
    file_name, file_type = os.path.splitext(temp_filename)
    backup_file = file_name + ".backup" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_type
    mv(origin_path, os.path.join(file_path, backup_file))
    print("\n<Info> : 旧的配置文件已备份为 %s" % os.path.join(file_path, backup_file))


def write_game_config(json_dict):
    config_path = os.path.join(APP_CONFIG['root'], APP_CONFIG['setting'])
    backup_game_config(config_path)
    try:
        with open(config_path, "a+", -1, 'utf-8') as f:
            f.write(json.dumps(json_dict, indent=4))
            # json.dump(json_dict, f)
    except IOError:
        print("<Error>: 写入输出游戏配置失败! %s" % config_path)


def process(game, key_name, key_bind, debug=False):
    if not isinstance(GAME_CONFIG, dict):
        exit(-1)
    if game == 'LOL':
        game_config = GAME_CONFIG['files'][1]['sections'][0]['settings']
        for index in range(len(game_config)):
            desc = ''
            if game_config[index]['name'] == KEY_MAP['成就表情']:
                desc = "亮狗牌 没什么好说的"
            elif game_config[index]['name'] == KEY_MAP['形态切换']:
                desc = "亚索绑定Q可以自动收刀"
                
            elif game_config[index]['name'] == KEY_MAP['大笑']:
                desc = "锐雯QA 亚索光速E"
            if game_config[index]['name'] == KEY_MAP[key_name]:
                if debug and KEY_MAP[key_name] != '':
                    print("<Debug>: 原来的 [ %s %s ] 键位为 %s %s" % (
                        key_name, KEY_MAP[key_name], game_config[index]['value'], desc))
                if game_config[index]['name'] == KEY_MAP[key_name]:
                    GAME_CONFIG['files'][1]['sections'][0]['settings'][index]['value'] = key_bind
                    print("<Info> : 新的 [ %s ] 键位为 %s" % (
                        key_name, GAME_CONFIG['files'][1]['sections'][0]['settings'][index]['value']))


def main():
    init('LOL')
    # print(APP_CONFIG)  # 显示本地配置项
    print()
    print("<Info> : 读取游戏配置文件... %s" % os.path.join(APP_CONFIG['root'], APP_CONFIG['setting']))
    """手动绑定
    while True:
    key_name = input("<Info> : 输入想要修改的键位名称:>")
    if key_name in KEY_MAP:
        key_bind = input("<Info> : 输入想要修改的绑定按键:>")
        print(key_bind)
        process('LOL', key_name, key_bind, True)
    else:
        print("<Error>: 没有找到这个键位!")
    """
    game = 'LOL'
    for key in KEY_BIND:
        if KEY_BIND[key] != '':
            print()
            process(game, key, KEY_BIND[key], True)
    write_game_config(GAME_CONFIG)
    print("<Info> : 修改结束! 可直接退出或继续修改...")


if __name__ == "__main__":
    main()
