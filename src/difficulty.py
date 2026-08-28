# ====== 难度配置 ======
DIFFICULTY_CONFIG = {
    '简单': {
        'size': 11,
        'max_walls': 5,
        'extra_paths': 8,
        'desc': '11×11，允许撞墙5次',
        'hint_time': 30,
        'hint_cooldown': 10
    },
    '普通': {
        'size': 21,
        'max_walls': 8,
        'extra_paths': 15,
        'desc': '21×21，允许撞墙8次',
        'hint_time': 25,
        'hint_cooldown': 12
    },
    '困难': {
        'size': 31,
        'max_walls': 12,
        'extra_paths': 25,
        'desc': '31×31，允许撞墙12次',
        'hint_time': 20,
        'hint_cooldown': 15
    },
    '专家': {
        'size': 51,
        'max_walls': 8,
        'extra_paths': 40,
        'desc': '51×51，允许撞墙8次',
        'hint_time': 15,
        'hint_cooldown': 18
    },
    '地狱': {
        'size': 81,
        'max_walls': 5,
        'extra_paths': 60,
        'desc': '81×81，允许撞墙5次',
        'hint_time': 10,
        'hint_cooldown': 20
    }
}
