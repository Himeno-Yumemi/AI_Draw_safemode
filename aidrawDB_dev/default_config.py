# 以下是默认配置，仅用作注释参考和生成默认配置文件，请不要在这里修改，请在config.json文件中修改配置才能生效！！！
config_default = {
    "base": {
        "daily_max": 20,  # 每日上限次数
        "freq_limit": 10,  # 频率限制
        "freq_cd":10,   # 使用CD
    },
    "default": {
        "arrange_tags": True,  # 是否开启tags整理（默认开启，暂时无法关闭）
        "add_db": True,  # 是否开启数据录入（默认开启，暂时无法关闭）
        "quality":100,  # 生成图片质量
        "bot_name":"梦美酱",    #转发消息bot名字
        "bot_uid":2854196306,   #转发消息显示的QQ头像
    },
    "NovelAI": {
        "api": "",  # 设置api，例如："http://11.222.333.444:5555/"
        "token": ""  # 设置你的token，例如："ADGdsvSFGsaA5S2D"，（若你的api无需使用token，留空即可）
    },
    "Tencent": {
        "TencentAI_check": True,  # 腾讯AI鉴黄开关
        "secretId": "",  # 自己的腾讯云账户secretId
        "secretKey": "",  # 自己的腾讯云账户secretKey
    },
    "Baidu": {
        "BaiduAI_check": False, # 百度AI鉴黄开关
        "api_key": "",  # 自己的百度云鉴黄api_key
        "secret_key": ""    # 自己的百度云鉴黄secret_key
    },
    "default_tags": {
        "tags": "miku"  # 如果没有指定tag的话，默认的tag
    },
    "default_ntags":{
        "ntags_stats":True, #默认负面tags开关
        "ntags":"extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad anatomy,bad hands,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit,,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet"
    },  #默认负面tags
    "ban_word": {
        "wordlist": [
            "r18",
            "naked",
            "vagina",
            "penis",
            "nsfw",
            "genital",
            "nude",
            "NSFW",
            "R18",
            "NAKED",
            "VAGINA",
            "PENIS",
            "GENITAL",
            "NUDE",
            "tentacle",
            "hairjob",
            "oral/fellatio",
            "deepthroat",
            "gokkun",
            "gag",
            "ballgag",
            "bitgag",
            "ring_gag",
            "cleave_gag",
            "panty_gag",
            "tapegag",
            "facial",
            "leash",
            "handjob",
            "groping",
            "areolae",
            "nipples",
            "puffy_nipples",
            "small_nipples",
            "nipple_pull",
            "nipple_torture",
            "nipple_tweak",
            "nipple_piercing",
            "breast_grab",
            "lactation",
            "breast_sucking/nipple_suck",
            "breast_feeding",
            "paizuri",
            "multiple_paizuri",
            "breast_smother",
            "piercing",
            "navel_piercing",
            "thigh_sex",
            "footjob",
            "mound_of_venus",
            "wide_hips",
            "masturbation",
            "clothed_masturbation",
            "penis",
            "testicles",
            "ejaculation",
            "cum",
            "cum_inside",
            "cum_on_breast",
            "cum_on_hair",
            "cum_on_food",
            "tamakeri",
            "pussy/vaginal",
            "pubic_hair",
            "shaved_pussy",
            "no_pussy",
            "clitoris",
            "fat_mons",
            "cameltoe",
            "pussy_juice",
            "female_ejaculation",
            "grinding",
            "crotch_rub",
            "facesitting",
            "cervix",
            "cunnilingus",
            "insertion",
            "anal_insertion",
            "fruit_insertion",
            "large_insertion",
            "penetration",
            "fisting",
            "fingering",
            "multiple_insertions",
            "double_penetration",
            "triple_penetration",
            "double_vaginal",
            "peeing",
            "have_to_pee",
            "ass",
            "huge_ass",
            "spread_ass",
            "buttjob",
            "spanked",
            "anus",
            "anal",
            "double_anal",
            "anal_fingering",
            "anal_fisting",
            "anilingus",
            "enema",
            "stomach_bulge",
            "x-ray",
            "cross-section/internal_cumshot",
            "wakamezake",
            "public",
            "humiliation",
            "bra_lift",
            "panties_around_one_leg",
            "caught",
            "walk-in",
            "body_writing",
            "tally",
            "futanari",
            "incest",
            "twincest",
            "pegging",
            "femdom",
            "ganguro",
            "bestiality",
            "gangbang",
            "hreesome",
            "group_sex",
            "orgy/teamwork",
            "tribadism",
            "molestation",
            "voyeurism",
            "exhibitionism",
            "rape",
            "about_to_be_raped",
            "sex",
            "clothed_sex",
            "happy_sex",
            "underwater_sex",
            "spitroast",
            "cock_in_thighhigh",
            "doggystyle",
            "leg_lock/upright_straddle",
            "missionary",
            "girl_on_top",
            "cowgirl_position",
            "reverse_cowgirl",
            "virgin",
            "slave",
            "shibari",
            "bondage",
            "bdsm",
            "pillory/stocks",
            "rope",
            "bound_arms",
            "bound_wrists",
            "crotch_rope",
            "hogtie",
            "frogtie",
            "suspension",
            "spreader_bar",
            "wooden_horse",
            "anal_beads",
            "dildo",
            "cock_ring",
            "egg_vibrator",
            "artificial_vagina",
            "hitachi_magic_wand",
            "dildo",
            "double_dildo",
            "vibrator",
            "vibrator_in_thighhighs",
            "nyotaimori",
            "vore",
            "amputee",
            "transformation",
            "mind_control",
            "censored",
            "uncensored",
            "asian",
            "faceless_male",
            "blood"
        ]
    },  # 屏蔽词列表
}