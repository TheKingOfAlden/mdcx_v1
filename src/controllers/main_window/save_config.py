import os
import platform
import re
import traceback

from PyQt5.QtCore import Qt

from models.base.path import get_main_path
from models.base.utils import convert_path
from models.config.config import config
from models.core.flags import Flags
from models.core.utils import get_movie_path_setting
from models.core.web import check_proxyChange
from models.signals import signal
from models.tools.actress_db import ActressDB


def save_config(self):
    # region media & escape
    config.tree_file = self.Ui.lineEdit_tree_file.text()
    config.tree_file_prefix = self.Ui.lineEdit_tree_file_prefix.text()
    config.media_path = self.Ui.lineEdit_movie_path.text()  # 待刮削目录
    config.softlink_path = self.Ui.lineEdit_movie_softlink_path.text()  # 软链接目录目录
    config.success_output_folder = self.Ui.lineEdit_success.text()  # 成功输出目录
    config.failed_output_folder = self.Ui.lineEdit_fail.text()  # 失败输出目录
    config.extrafanart_folder = self.Ui.lineEdit_extrafanart_dir.text().strip()  # 剧照目录
    config.media_type = self.Ui.lineEdit_movie_type.text().lower()  # 视频格式
    config.sub_type = self.Ui.lineEdit_sub_type.text()  # 字幕格式
    config.folders = self.Ui.lineEdit_escape_dir.text()  # 排除文件夹
    config.string = self.Ui.lineEdit_escape_string.text()  # 过滤字符
    config.scrape_softlink_path = 1 if self.Ui.checkBox_scrape_softlink_path.isChecked() else ""

    try:  # 过滤小文件大小
        config.file_size = float(self.Ui.lineEdit_escape_size.text())
    except:
        config.file_size = 0.0
    config.no_escape = ""
    if self.Ui.checkBox_no_escape_file.isChecked():  # 不过滤文件、文件夹，检测软链接
        config.no_escape += "no_skip_small_file,"
    if self.Ui.checkBox_no_escape_dir.isChecked():
        config.no_escape += "folder,"
    if self.Ui.checkBox_skip_success_file.isChecked():
        config.no_escape += "skip_success_file,"
    if self.Ui.checkBox_record_success_file.isChecked():
        config.no_escape += "record_success_file,"
    if self.Ui.checkBox_check_symlink.isChecked():
        config.no_escape += "check_symlink,"
    if self.Ui.checkBox_check_symlink_definition.isChecked():
        config.no_escape += "symlink_definition,"
    # endregion

    # region clean
    config.clean_ext = self.Ui.lineEdit_clean_file_ext.text().strip(" |｜")  # 清理扩展名
    config.clean_name = self.Ui.lineEdit_clean_file_name.text().strip(" |｜")  # 清理文件名
    config.clean_contains = self.Ui.lineEdit_clean_file_contains.text().strip(" |｜")  # 清理文件名包含
    try:
        config.clean_size = float(self.Ui.lineEdit_clean_file_size.text().strip(" |｜"))  # 清理文件大小小于等于
    except:
        config.clean_size = 0.0
    config.clean_ignore_ext = self.Ui.lineEdit_clean_excluded_file_ext.text().strip(" |｜")  # 不清理扩展名
    config.clean_ignore_contains = self.Ui.lineEdit_clean_excluded_file_contains.text().strip(
        " |｜"
    )  # 不清理文件名包含
    config.clean_enable = ""
    if self.Ui.checkBox_clean_file_ext.isChecked():
        config.clean_enable += "clean_ext,"
    if self.Ui.checkBox_clean_file_name.isChecked():
        config.clean_enable += "clean_name,"
    if self.Ui.checkBox_clean_file_contains.isChecked():
        config.clean_enable += "clean_contains,"
    if self.Ui.checkBox_clean_file_size.isChecked():
        config.clean_enable += "clean_size,"
    if self.Ui.checkBox_clean_excluded_file_ext.isChecked():
        config.clean_enable += "clean_ignore_ext,"
    if self.Ui.checkBox_clean_excluded_file_contains.isChecked():
        config.clean_enable += "clean_ignore_contains,"
    if self.Ui.checkBox_i_understand_clean.isChecked():
        config.clean_enable += "i_know,"
    if self.Ui.checkBox_i_agree_clean.isChecked():
        config.clean_enable += "i_agree,"
    if self.Ui.checkBox_auto_clean.isChecked():
        config.clean_enable += "auto_clean,"
    # endregion

    # region website
    config.website_single = self.Ui.comboBox_website_all.currentText()  # 指定单个网站
    config.website_youma = self.Ui.lineEdit_website_youma.text()  # 有码番号刮削网站
    config.website_wuma = self.Ui.lineEdit_website_wuma.text()  # 无码番号刮削网站
    config.website_suren = self.Ui.lineEdit_website_suren.text()  # 素人番号刮削网站
    config.website_fc2 = self.Ui.lineEdit_website_fc2.text()  # FC2番号刮削网站
    config.website_oumei = self.Ui.lineEdit_website_oumei.text()  # 欧美番号刮削网站
    config.website_guochan = self.Ui.lineEdit_website_guochan.text()  # 国产番号刮削网站

    if self.Ui.radioButton_scrape_speed.isChecked():  # 刮削偏好
        config.scrape_like = "speed"
    elif self.Ui.radioButton_scrape_info.isChecked():
        config.scrape_like = "info"
    else:
        config.scrape_like = "single"

    config.website_set = ""
    if self.Ui.checkBox_use_official_data.isChecked():  # 使用官网数据
        config.website_set += "official,"
    config.title_website = self.Ui.lineEdit_title_website.text()  # 标题字段网站优先级
    config.title_zh_website = self.Ui.lineEdit_title_zh_website.text()  # 中文标题字段网站优先级
    config.title_website_exclude = self.Ui.lineEdit_title_website_exclude.text()  # 标题字段排除网站
    if self.Ui.radioButton_title_zh_cn.isChecked():  # 标题语言
        config.title_language = "zh_cn"
    elif self.Ui.radioButton_title_zh_tw.isChecked():
        config.title_language = "zh_tw"
    else:
        config.title_language = "jp"
    if self.Ui.checkBox_title_sehua.isChecked():  # 标题翻译-sehua
        config.title_sehua = "on"
    else:
        config.title_sehua = "off"
    if self.Ui.checkBox_title_yesjav.isChecked():  # 标题翻译-yesjav
        config.title_yesjav = "on"
    else:
        config.title_yesjav = "off"
    if self.Ui.checkBox_title_translate.isChecked():  # 标题翻译-翻译引擎
        config.title_translate = "on"
    else:
        config.title_translate = "off"
    if self.Ui.checkBox_title_sehua_2.isChecked():  # 标题翻译-优先sehua
        config.title_sehua_zh = "on"
    else:
        config.title_sehua_zh = "off"

    config.outline_website = self.Ui.lineEdit_outline_website.text()  # 简介字段网站优先级
    config.outline_zh_website = self.Ui.lineEdit_outline_zh_website.text()  # 中文简介字段网站优先级
    config.outline_website_exclude = self.Ui.lineEdit_outline_website_exclude.text()  # 简介字段排除网站
    if self.Ui.radioButton_outline_zh_cn.isChecked():  # 简介语言
        config.outline_language = "zh_cn"
    elif self.Ui.radioButton_outline_zh_tw.isChecked():
        config.outline_language = "zh_tw"
    else:
        config.outline_language = "jp"
    if self.Ui.checkBox_outline_translate.isChecked():  # 简介翻译-翻译引擎
        config.outline_translate = "on"
    else:
        config.outline_translate = "off"
    config.outline_show = ""
    if self.Ui.checkBox_show_translate_from.isChecked():  # 简介翻译-翻译来源、双语显示
        config.outline_show += "show_from,"
    if self.Ui.radioButton_trans_show_zh_jp.isChecked():  # 简介翻译-翻译来源、双语显示
        config.outline_show += "show_zh_jp,"
    elif self.Ui.radioButton_trans_show_jp_zh.isChecked():
        config.outline_show += "show_jp_zh,"

    config.actor_website = self.Ui.lineEdit_actor_website.text()  # 演员字段网站优先级
    config.actor_website_exclude = self.Ui.lineEdit_actor_website_exclude.text()  # 演员字段排除网站
    if self.Ui.radioButton_actor_zh_cn.isChecked():  # 演员语言
        config.actor_language = "zh_cn"
    elif self.Ui.radioButton_actor_zh_tw.isChecked():
        config.actor_language = "zh_tw"
    else:
        config.actor_language = "jp"
    if self.Ui.checkBox_actor_realname.isChecked():  # 演员使用真实名字
        config.actor_realname = "on"
    else:
        config.actor_realname = "off"
    if self.Ui.checkBox_actor_translate.isChecked():  # 演员-映射表
        config.actor_translate = "on"
    else:
        config.actor_translate = "off"

    config.tag_website = self.Ui.lineEdit_tag_website.text()  # 标签字段网站优先级
    config.tag_website_exclude = self.Ui.lineEdit_tag_website_exclude.text()  # 标签字段排除网站
    if self.Ui.radioButton_tag_zh_cn.isChecked():  # 标签语言
        config.tag_language = "zh_cn"
    elif self.Ui.radioButton_tag_zh_tw.isChecked():
        config.tag_language = "zh_tw"
    else:
        config.tag_language = "jp"
    if self.Ui.checkBox_tag_translate.isChecked():  # 标签-映射表
        config.tag_translate = "on"
    else:
        config.tag_translate = "off"
    config.tag_include = ""  # 写入标签字段的信息
    if self.Ui.checkBox_tag_actor.isChecked():
        config.tag_include += "actor,"
    if self.Ui.checkBox_tag_letters.isChecked():
        config.tag_include += "letters,"
    if self.Ui.checkBox_tag_series.isChecked():
        config.tag_include += "series,"
    if self.Ui.checkBox_tag_studio.isChecked():
        config.tag_include += "studio,"
    if self.Ui.checkBox_tag_publisher.isChecked():
        config.tag_include += "publisher,"
    if self.Ui.checkBox_tag_cnword.isChecked():
        config.tag_include += "cnword,"
    if self.Ui.checkBox_tag_mosaic.isChecked():
        config.tag_include += "mosaic,"
    if self.Ui.checkBox_tag_definition.isChecked():
        config.tag_include += "definition,"

    config.series_website = self.Ui.lineEdit_series_website.text()  # 系列字段网站优先级
    config.series_website_exclude = self.Ui.lineEdit_series_website_exclude.text()  # 系列字段排除网站
    if self.Ui.radioButton_series_zh_cn.isChecked():  # 系列字段语言
        config.series_language = "zh_cn"
    elif self.Ui.radioButton_series_zh_tw.isChecked():
        config.series_language = "zh_tw"
    else:
        config.series_language = "jp"
    if self.Ui.checkBox_series_translate.isChecked():  # 系列-映射表
        config.series_translate = "on"
    else:
        config.series_translate = "off"

    config.studio_website = self.Ui.lineEdit_studio_website.text()  # 片商字段网站优先级
    config.studio_website_exclude = self.Ui.lineEdit_studio_website_exclude.text()  # 片商字段排除网站
    if self.Ui.radioButton_studio_zh_cn.isChecked():  # 片商字段语言
        config.studio_language = "zh_cn"
    elif self.Ui.radioButton_studio_zh_tw.isChecked():
        config.studio_language = "zh_tw"
    else:
        config.studio_language = "jp"
    if self.Ui.checkBox_studio_translate.isChecked():  # 片商-映射表
        config.studio_translate = "on"
    else:
        config.studio_translate = "off"

    config.publisher_website = self.Ui.lineEdit_publisher_website.text()  # 发行字段网站优先级
    config.publisher_website_exclude = self.Ui.lineEdit_publisher_website_exclude.text()  # 发行字段排除网站
    if self.Ui.radioButton_publisher_zh_cn.isChecked():  # 发行字段语言
        config.publisher_language = "zh_cn"
    elif self.Ui.radioButton_publisher_zh_tw.isChecked():
        config.publisher_language = "zh_tw"
    else:
        config.publisher_language = "jp"
    if self.Ui.checkBox_publisher_translate.isChecked():  # 发行-映射表
        config.publisher_translate = "on"
    else:
        config.publisher_translate = "off"

    config.director_website = self.Ui.lineEdit_director_website.text()  # 导演字段网站优先级
    config.director_website_exclude = self.Ui.lineEdit_director_website_exclude.text()  # 导演字段排除网站
    if self.Ui.radioButton_director_zh_cn.isChecked():  # 导演字段语言
        config.director_language = "zh_cn"
    elif self.Ui.radioButton_director_zh_tw.isChecked():
        config.director_language = "zh_tw"
    else:
        config.director_language = "jp"
    if self.Ui.checkBox_director_translate.isChecked():  # 导演-映射表
        config.director_translate = "on"
    else:
        config.director_translate = "off"

    config.poster_website = self.Ui.lineEdit_poster_website.text()  # 封面字段网站优先级
    config.poster_website_exclude = self.Ui.lineEdit_poster_website_exclude.text()  # 封面字段排除网站
    config.thumb_website = self.Ui.lineEdit_thumb_website.text()  # 背景字段网站优先级
    config.thumb_website_exclude = self.Ui.lineEdit_thumb_website_exclude.text()  # 背景字段排除网站
    config.extrafanart_website = self.Ui.lineEdit_extrafanart_website.text()  # 剧照字段网站优先级
    config.extrafanart_website_exclude = self.Ui.lineEdit_extrafanart_website_exclude.text()  # 剧照字段排除网站
    config.score_website = self.Ui.lineEdit_score_website.text()  # 评分字段网站优先级
    config.score_website_exclude = self.Ui.lineEdit_score_website_exclude.text()  # 评分字段排除网站
    config.release_website = self.Ui.lineEdit_release_website.text()  # 发行日期字段网站优先级
    config.release_website_exclude = self.Ui.lineEdit_release_website_exclude.text()  # 发行日期字段排除网站
    config.runtime_website = self.Ui.lineEdit_runtime_website.text()  # 时长字段网站优先级
    config.runtime_website_exclude = self.Ui.lineEdit_runtime_website_exclude.text()  # 时长字段排除网站
    config.trailer_website = self.Ui.lineEdit_trailer_website.text()  # 预告片字段网站优先级
    config.trailer_website_exclude = self.Ui.lineEdit_trailer_website_exclude.text()  # 预告片字段排除网站
    config.wanted_website = self.Ui.lineEdit_wanted_website.text()  # 想看人数网站
    config.nfo_tagline = self.Ui.lineEdit_nfo_tagline.text()  # tagline格式
    config.nfo_tag_series = self.Ui.lineEdit_nfo_tag_series.text()  # nfo_tag_series 格式
    config.nfo_tag_studio = self.Ui.lineEdit_nfo_tag_studio.text()  # nfo_tag_studio 格式
    config.nfo_tag_publisher = self.Ui.lineEdit_nfo_tag_publisher.text()  # nfo_tag_publisher 格式

    config.whole_fields = ""
    config.none_fields = ""
    if self.Ui.radioButton_outline_more.isChecked():
        config.whole_fields += "outline,"
    elif self.Ui.radioButton_outline_none.isChecked():
        config.none_fields += "outline,"

    if self.Ui.radioButton_actor_more.isChecked():
        config.whole_fields += "actor,"
    elif self.Ui.radioButton_actor_none.isChecked():
        config.none_fields += "actor,"

    if self.Ui.radioButton_thumb_more.isChecked():
        config.whole_fields += "thumb,"
    elif self.Ui.radioButton_thumb_none.isChecked():
        config.none_fields += "thumb,"

    if self.Ui.radioButton_poster_more.isChecked():
        config.whole_fields += "poster,"
    elif self.Ui.radioButton_poster_none.isChecked():
        config.none_fields += "poster,"

    if self.Ui.radioButton_extrafanart_more.isChecked():
        config.whole_fields += "extrafanart,"
    elif self.Ui.radioButton_extrafanart_none.isChecked():
        config.none_fields += "extrafanart,"

    if self.Ui.radioButton_trailer_more.isChecked():
        config.whole_fields += "trailer,"
    elif self.Ui.radioButton_trailer_none.isChecked():
        config.none_fields += "trailer,"

    if self.Ui.radioButton_release_more.isChecked():
        config.whole_fields += "release,"
    elif self.Ui.radioButton_release_none.isChecked():
        config.none_fields += "release,"

    if self.Ui.radioButton_runtime_more.isChecked():
        config.whole_fields += "runtime,"
    elif self.Ui.radioButton_runtime_none.isChecked():
        config.none_fields += "runtime,"

    if self.Ui.radioButton_score_more.isChecked():
        config.whole_fields += "score,"
    elif self.Ui.radioButton_score_none.isChecked():
        config.none_fields += "score,"

    if self.Ui.radioButton_tag_more.isChecked():
        config.whole_fields += "tag,"
    elif self.Ui.radioButton_tag_none.isChecked():
        config.none_fields += "tag,"

    if self.Ui.radioButton_director_more.isChecked():
        config.whole_fields += "director,"
    elif self.Ui.radioButton_director_none.isChecked():
        config.none_fields += "director,"

    if self.Ui.radioButton_series_more.isChecked():
        config.whole_fields += "series,"
    elif self.Ui.radioButton_series_none.isChecked():
        config.none_fields += "series,"

    if self.Ui.radioButton_studio_more.isChecked():
        config.whole_fields += "studio,"
    elif self.Ui.radioButton_studio_none.isChecked():
        config.none_fields += "studio,"

    if self.Ui.radioButton_publisher_more.isChecked():
        config.whole_fields += "publisher,"
    elif self.Ui.radioButton_publisher_none.isChecked():
        config.none_fields += "publisher,"

    if self.Ui.radioButton_wanted_none.isChecked():
        config.none_fields += "wanted,"

    # region nfo
    config.nfo_include_new = ""  # 写入nfo的字段：
    if self.Ui.checkBox_nfo_sorttitle.isChecked():
        config.nfo_include_new += "sorttitle,"
    if self.Ui.checkBox_nfo_originaltitle.isChecked():
        config.nfo_include_new += "originaltitle,"
    if self.Ui.checkBox_nfo_title_cd.isChecked():
        config.nfo_include_new += "title_cd,"
    if self.Ui.checkBox_nfo_outline.isChecked():
        config.nfo_include_new += "outline,"
    if self.Ui.checkBox_nfo_plot.isChecked():
        config.nfo_include_new += "plot_,"
    if self.Ui.checkBox_nfo_originalplot.isChecked():
        config.nfo_include_new += "originalplot,"
    if self.Ui.checkBox_outline_cdata.isChecked():
        config.nfo_include_new += "outline_no_cdata,"
    if self.Ui.checkBox_nfo_release.isChecked():
        config.nfo_include_new += "release_,"
    if self.Ui.checkBox_nfo_relasedate.isChecked():
        config.nfo_include_new += "releasedate,"
    if self.Ui.checkBox_nfo_premiered.isChecked():
        config.nfo_include_new += "premiered,"
    if self.Ui.checkBox_nfo_country.isChecked():
        config.nfo_include_new += "country,"
    if self.Ui.checkBox_nfo_mpaa.isChecked():
        config.nfo_include_new += "mpaa,"
    if self.Ui.checkBox_nfo_customrating.isChecked():
        config.nfo_include_new += "customrating,"
    if self.Ui.checkBox_nfo_year.isChecked():
        config.nfo_include_new += "year,"
    if self.Ui.checkBox_nfo_runtime.isChecked():
        config.nfo_include_new += "runtime,"
    if self.Ui.checkBox_nfo_wanted.isChecked():
        config.nfo_include_new += "wanted,"
    if self.Ui.checkBox_nfo_score.isChecked():
        config.nfo_include_new += "score,"
    if self.Ui.checkBox_nfo_criticrating.isChecked():
        config.nfo_include_new += "criticrating,"
    if self.Ui.checkBox_nfo_actor.isChecked():
        config.nfo_include_new += "actor,"
    if self.Ui.checkBox_nfo_all_actor.isChecked():
        config.nfo_include_new += "actor_all,"
    if self.Ui.checkBox_nfo_director.isChecked():
        config.nfo_include_new += "director,"
    if self.Ui.checkBox_nfo_series.isChecked():
        config.nfo_include_new += "series,"
    if self.Ui.checkBox_nfo_tag.isChecked():
        config.nfo_include_new += "tag,"
    if self.Ui.checkBox_nfo_genre.isChecked():
        config.nfo_include_new += "genre,"
    if self.Ui.checkBox_nfo_actor_set.isChecked():
        config.nfo_include_new += "actor_set,"
    if self.Ui.checkBox_nfo_set.isChecked():
        config.nfo_include_new += "series_set,"
    if self.Ui.checkBox_nfo_studio.isChecked():
        config.nfo_include_new += "studio,"
    if self.Ui.checkBox_nfo_maker.isChecked():
        config.nfo_include_new += "maker,"
    if self.Ui.checkBox_nfo_publisher.isChecked():
        config.nfo_include_new += "publisher,"
    if self.Ui.checkBox_nfo_label.isChecked():
        config.nfo_include_new += "label,"
    if self.Ui.checkBox_nfo_poster.isChecked():
        config.nfo_include_new += "poster,"
    if self.Ui.checkBox_nfo_cover.isChecked():
        config.nfo_include_new += "cover,"
    if self.Ui.checkBox_nfo_trailer.isChecked():
        config.nfo_include_new += "trailer,"
    if self.Ui.checkBox_nfo_website.isChecked():
        config.nfo_include_new += "website,"
    # endregion
    config.translate_by = ""
    if self.Ui.checkBox_youdao.isChecked():  # 有道翻译
        config.translate_by += "youdao,"
    if self.Ui.checkBox_google.isChecked():  # google 翻译
        config.translate_by += "google,"
    if self.Ui.checkBox_deepl.isChecked():  # deepl 翻译
        config.translate_by += "deepl,"
    config.deepl_key = self.Ui.lineEdit_deepl_key.text()  # deepl key
    # endregion

    # region common
    config.thread_number = self.Ui.horizontalSlider_thread.value()  # 线程数量
    config.thread_time = self.Ui.horizontalSlider_thread_time.value()  # 线程延时
    config.javdb_time = self.Ui.horizontalSlider_javdb_time.value()  # javdb 延时
    if self.Ui.radioButton_mode_common.isChecked():  # 普通模式
        config.main_mode = 1
    elif self.Ui.radioButton_mode_sort.isChecked():  # 整理模式
        config.main_mode = 2
    elif self.Ui.radioButton_mode_update.isChecked():  # 整理模式
        config.main_mode = 3
    elif self.Ui.radioButton_mode_read.isChecked():  # 读取模式
        config.main_mode = 4
    else:
        config.main_mode = 1
    config.read_mode = ""
    if self.Ui.checkBox_read_has_nfo_update.isChecked():  # 读取模式有nfo是否执行更新模式
        config.read_mode += "has_nfo_update,"
    if self.Ui.checkBox_read_no_nfo_scrape.isChecked():  # 读取模式无nfo是否刮削
        config.read_mode += "no_nfo_scrape,"
    if self.Ui.checkBox_read_download_file_again.isChecked():  # 读取模式允许下载文件
        config.read_mode += "read_download_again,"
    if self.Ui.checkBox_read_translate_again.isChecked():  # 读取模式启用字段翻译
        config.read_mode += "read_translate_again,"
    if self.Ui.radioButton_update_c.isChecked():  # update 模式
        config.update_mode = "c"
    elif self.Ui.radioButton_update_b_c.isChecked():
        config.update_mode = "bc"
        if self.Ui.checkBox_update_a.isChecked():
            config.update_mode = "abc"
    elif self.Ui.radioButton_update_d_c.isChecked():
        config.update_mode = "d"
    else:
        config.update_mode = "c"
    config.update_a_folder = self.Ui.lineEdit_update_a_folder.text()  # 更新模式 - a 目录
    config.update_b_folder = self.Ui.lineEdit_update_b_folder.text()  # 更新模式 - b 目录
    config.update_d_folder = self.Ui.lineEdit_update_d_folder.text()  # 更新模式 - d 目录
    if self.Ui.radioButton_soft_on.isChecked():  # 软链接开
        config.soft_link = 1
    elif self.Ui.radioButton_hard_on.isChecked():  # 硬链接开
        config.soft_link = 2
    else:  # 软链接关
        config.soft_link = 0
    if self.Ui.radioButton_succ_move_on.isChecked():  # 成功移动开
        config.success_file_move = 1
    elif self.Ui.radioButton_succ_move_off.isChecked():  # 成功移动关
        config.success_file_move = 0
    if self.Ui.radioButton_fail_move_on.isChecked():  # 失败移动开
        config.failed_file_move = 1
    else:
        config.failed_file_move = 0
    if self.Ui.radioButton_succ_rename_on.isChecked():  # 成功重命名开
        config.success_file_rename = 1
    elif self.Ui.radioButton_succ_rename_off.isChecked():  # 成功重命名关
        config.success_file_rename = 0
    if self.Ui.radioButton_del_empty_folder_on.isChecked():  # 结束后删除空文件夹开
        config.del_empty_folder = 1
    elif self.Ui.radioButton_del_empty_folder_off.isChecked():  # 结束后删除空文件夹关
        config.del_empty_folder = 0
    if self.Ui.checkBox_cover.isChecked():  # 显示封面
        config.show_poster = 1
    else:  # 关闭封面
        config.show_poster = 0
    # endregion

    # region download
    config.download_files = ","
    if self.Ui.checkBox_download_poster.isChecked():  # 下载 poster
        config.download_files += "poster,"
    if self.Ui.checkBox_download_thumb.isChecked():  # 下载 thumb
        config.download_files += "thumb,"
    if self.Ui.checkBox_download_fanart.isChecked():  # 下载 fanart
        config.download_files += "fanart,"
    if self.Ui.checkBox_download_extrafanart.isChecked():  # 下载 extrafanart
        config.download_files += "extrafanart,"
    if self.Ui.checkBox_download_trailer.isChecked():  # 下载 trailer
        config.download_files += "trailer,"
    if self.Ui.checkBox_download_nfo.isChecked():  # 下载 nfo
        config.download_files += "nfo,"
    if self.Ui.checkBox_extras.isChecked():  # 下载 剧照附加内容
        config.download_files += "extrafanart_extras,"
    if self.Ui.checkBox_download_extrafanart_copy.isChecked():  # 下载 剧照副本
        config.download_files += "extrafanart_copy,"
    if self.Ui.checkBox_theme_videos.isChecked():  # 下载 主题视频
        config.download_files += "theme_videos,"
    if self.Ui.checkBox_ignore_pic_fail.isChecked():  # 图片下载失败时，不视为刮削失败
        config.download_files += "ignore_pic_fail,"
    if self.Ui.checkBox_ignore_youma.isChecked():  # 有码封面不裁剪
        config.download_files += "ignore_youma,"
    if self.Ui.checkBox_ignore_wuma.isChecked():  # 无码封面不裁剪
        config.download_files += "ignore_wuma,"
    if self.Ui.checkBox_ignore_fc2.isChecked():  # fc2 封面不裁剪
        config.download_files += "ignore_fc2,"
    if self.Ui.checkBox_ignore_guochan.isChecked():  # 国产封面不裁剪
        config.download_files += "ignore_guochan,"
    if self.Ui.checkBox_ignore_size.isChecked():  # 不校验预告片文件大小
        config.download_files += "ignore_size,"

    config.keep_files = ","
    if self.Ui.checkBox_old_poster.isChecked():  # 保留 poster
        config.keep_files += "poster,"
    if self.Ui.checkBox_old_thumb.isChecked():  # 保留 thumb
        config.keep_files += "thumb,"
    if self.Ui.checkBox_old_fanart.isChecked():  # 保留 fanart
        config.keep_files += "fanart,"
    if self.Ui.checkBox_old_extrafanart.isChecked():  # 保留 extrafanart
        config.keep_files += "extrafanart,"
    if self.Ui.checkBox_old_trailer.isChecked():  # 保留 trailer
        config.keep_files += "trailer,"
    if self.Ui.checkBox_old_nfo.isChecked():  # 保留 nfo
        config.keep_files += "nfo,"
    if self.Ui.checkBox_old_extrafanart_copy.isChecked():  # 保留 剧照副本
        config.keep_files += "extrafanart_copy,"
    if self.Ui.checkBox_old_theme_videos.isChecked():  # 保留 主题视频
        config.keep_files += "theme_videos,"

    config.download_hd_pics = ""
    if self.Ui.checkBox_hd_poster.isChecked():  # 高清封面图
        config.download_hd_pics += "poster,"
    if self.Ui.checkBox_hd_thumb.isChecked():  # 高清缩略图
        config.download_hd_pics += "thumb,"
    if self.Ui.checkBox_amazon_big_pic.isChecked():  # amazon
        config.download_hd_pics += "amazon,"
    if self.Ui.checkBox_official_big_pic.isChecked():  # google 以图搜图
        config.download_hd_pics += "official,"
    if self.Ui.checkBox_google_big_pic.isChecked():  # google 以图搜图
        config.download_hd_pics += "google,"
    if self.Ui.radioButton_google_only.isChecked():  # google 只下载
        config.download_hd_pics += "goo_only,"

    config.google_used = self.Ui.lineEdit_google_used.text()  # google 下载词
    config.google_exclude = self.Ui.lineEdit_google_exclude.text()  # google 过滤词
    # endregion

    # region name
    config.folder_name = self.Ui.lineEdit_dir_name.text()  # 视频文件夹命名
    config.naming_file = self.Ui.lineEdit_local_name.text()  # 视频文件名命名
    config.naming_media = self.Ui.lineEdit_media_name.text()  # nfo标题命名
    config.prevent_char = self.Ui.lineEdit_prevent_char.text()  # 防屏蔽字符

    config.fields_rule = ""  # 字段规则
    if self.Ui.checkBox_title_del_actor.isChecked():  # 去除标题后的演员名
        config.fields_rule += "del_actor,"
    if self.Ui.checkBox_actor_del_char.isChecked():  # 去除演员括号
        config.fields_rule += "del_char,"
    if self.Ui.checkBox_actor_fc2_seller.isChecked():  # fc2 卖家
        config.fields_rule += "fc2_seller,"
    if self.Ui.checkBox_number_del_num.isChecked():  # 素人番号去除番号前缀数字
        config.fields_rule += "del_num,"
    config.suffix_sort = self.Ui.lineEdit_suffix_sort.text()  # 后缀字段顺序
    config.actor_no_name = self.Ui.lineEdit_actor_no_name.text()  # 未知演员
    config.actor_name_more = self.Ui.lineEdit_actor_name_more.text()  # 等演员
    release_rule = self.Ui.lineEdit_release_rule.text()  # 发行日期
    config.release_rule = re.sub(r'[\\/:*?"<>|\r\n]+', "-", release_rule).strip()

    config.folder_name_max = int(self.Ui.lineEdit_folder_name_max.text())  # 长度命名规则-目录
    config.file_name_max = int(self.Ui.lineEdit_file_name_max.text())  # 长度命名规则-文件名
    config.actor_name_max = int(self.Ui.lineEdit_actor_name_max.text())  # 长度命名规则-演员数量

    config.umr_style = self.Ui.lineEdit_umr_style.text()  # 无码破解版本命名
    config.leak_style = self.Ui.lineEdit_leak_style.text()  # 无码流出版本命名
    config.wuma_style = self.Ui.lineEdit_wuma_style.text()  # 无码版本命名
    config.youma_style = self.Ui.lineEdit_youma_style.text()  # 有码版本命名
    config.show_moword = ""
    if self.Ui.checkBox_foldername_mosaic.isChecked():  # 视频目录名显示版本命名字符
        config.show_moword += "folder,"
    if self.Ui.checkBox_filename_mosaic.isChecked():  # 视频文件名显示版本命名字符
        config.show_moword += "file,"
    config.show_4k = ""
    if self.Ui.checkBox_foldername_4k.isChecked():  # 视频目录名显示4k
        config.show_4k += "folder,"
    if self.Ui.checkBox_filename_4k.isChecked():  # 视频文件名显示4k
        config.show_4k += "file,"

    if self.Ui.radioButton_cd_part_lower.isChecked():  # 分集命名规则-小写
        config.cd_name = 0
    elif self.Ui.radioButton_cd_part_upper.isChecked():  # 分集命名规则-小写
        config.cd_name = 1
    else:
        config.cd_name = 2
    config.cd_char = ""
    if self.Ui.checkBox_cd_part_a.isChecked():  # 字母结尾的分集
        config.cd_char += "letter,"
    if self.Ui.checkBox_cd_part_c.isChecked():  # 字母C结尾的分集
        config.cd_char += "endc,"
    if self.Ui.checkBox_cd_part_01.isChecked():  # 两位数字结尾的分集
        config.cd_char += "digital,"
    if self.Ui.checkBox_cd_part_1_xxx.isChecked():  # 中间数字的分集
        config.cd_char += "middle_number,"
    if self.Ui.checkBox_cd_part_underline.isChecked():  # 下划线分隔符
        config.cd_char += "underline,"
    if self.Ui.checkBox_cd_part_space.isChecked():  # 空格分隔符
        config.cd_char += "space,"
    if self.Ui.checkBox_cd_part_point.isChecked():  # 小数点分隔符
        config.cd_char += "point,"

    if self.Ui.radioButton_pic_with_filename.isChecked():  # 图片命名规则-加文件名
        config.pic_name = 0
    else:  # 图片命名规则-不加文件名
        config.pic_name = 1
    if self.Ui.radioButton_trailer_with_filename.isChecked():  # 预告片命名规则-加文件名
        config.trailer_name = 0
    else:  # 预告片命名规则-不加文件名
        config.trailer_name = 1
    if self.Ui.radioButton_definition_height.isChecked():  # 画质命名规则-高度
        config.hd_name = "height"
    else:  # 画质命名规则-清晰度
        config.hd_name = "hd"
    if self.Ui.radioButton_videosize_video.isChecked():  # 分辨率获取方式-视频
        config.hd_get = "video"
    elif self.Ui.radioButton_videosize_path.isChecked():  # 分辨率获取方式-路径
        config.hd_get = "path"
    else:  # 分辨率获取方式-无
        config.hd_get = "none"
    # endregion

    # region subtitle
    config.cnword_char = self.Ui.lineEdit_cnword_char.text()  # 中文字幕判断字符
    config.cnword_style = self.Ui.lineEdit_cnword_style.text()  # 中文字幕字符样式
    if self.Ui.checkBox_foldername.isChecked():  # 视频目录名显示中文字幕
        config.folder_cnword = "on"
    else:
        config.folder_cnword = "off"
    if self.Ui.checkBox_filename.isChecked():  # 视频文件名显示中文字幕
        config.file_cnword = "on"
    else:
        config.file_cnword = "off"
    config.subtitle_folder = self.Ui.lineEdit_sub_folder.text()  # 字幕文件目录
    if self.Ui.radioButton_add_sub_on.isChecked():  # 自动添加字幕
        config.subtitle_add = "on"
    elif self.Ui.radioButton_add_sub_off.isChecked():
        config.subtitle_add = "off"
    if self.Ui.checkBox_sub_add_chs.isChecked():  # 字幕添加.chs后缀
        config.subtitle_add_chs = "on"
    else:
        config.subtitle_add_chs = "off"
    if self.Ui.checkBox_sub_rescrape.isChecked():  # 重新刮削新添加字幕的视频
        config.subtitle_add_rescrape = "on"
    else:
        config.subtitle_add_rescrape = "off"
    # endregion

    # region emby
    if self.Ui.radioButton_server_emby.isChecked():
        config.server_type = "emby"
    else:
        config.server_type = "jellyfin"
    config.emby_url = self.Ui.lineEdit_emby_url.text()  # emby地址
    config.emby_url = config.emby_url.replace("：", ":").strip("/ ")
    if config.emby_url and "://" not in config.emby_url:
        config.emby_url = "http://" + config.emby_url
    config.api_key = self.Ui.lineEdit_api_key.text()  # emby密钥
    config.user_id = self.Ui.lineEdit_user_id.text()  # emby用户ID
    config.actor_photo_folder = self.Ui.lineEdit_actor_photo_folder.text()  # 头像图片目录
    config.gfriends_github = self.Ui.lineEdit_net_actor_photo.text().strip(" /")  # gfriends github 项目地址
    config.info_database_path = self.Ui.lineEdit_actor_db_path.text()  # 信息数据库
    if not config.gfriends_github:
        config.gfriends_github = "https://github.com/gfriends/gfriends"
    elif "://" not in config.gfriends_github:
        config.gfriends_github = "https://" + config.gfriends_github
    if self.Ui.checkBox_actor_db.isChecked():
        config.use_database = 1
        ActressDB.init_db()
    else:
        config.use_database = 0
    config.emby_on = ""
    if self.Ui.radioButton_actor_info_zh_cn.isChecked():
        config.emby_on += "actor_info_zh_cn,"
    elif self.Ui.radioButton_actor_info_zh_tw.isChecked():
        config.emby_on += "actor_info_zh_tw,"
    else:
        config.emby_on += "actor_info_ja,"
    if self.Ui.checkBox_actor_info_translate.isChecked():
        config.emby_on += "actor_info_translate,"
    if self.Ui.radioButton_actor_info_all.isChecked():
        config.emby_on += "actor_info_all,"
    else:
        config.emby_on += "actor_info_miss,"
    if self.Ui.checkBox_actor_info_photo.isChecked():
        config.emby_on += "actor_info_photo,"

    if self.Ui.radioButton_actor_photo_net.isChecked():
        config.emby_on += "actor_photo_net,"
    else:
        config.emby_on += "actor_photo_local,"
    if self.Ui.checkBox_actor_photo_ne_backdrop.isChecked():
        config.emby_on += "graphis_backdrop,"
    if self.Ui.checkBox_actor_photo_ne_face.isChecked():
        config.emby_on += "graphis_face,"
    if self.Ui.checkBox_actor_photo_ne_new.isChecked():
        config.emby_on += "graphis_new,"
    if self.Ui.radioButton_actor_photo_all.isChecked():
        config.emby_on += "actor_photo_all,"
    else:
        config.emby_on += "actor_photo_miss,"
    if self.Ui.checkBox_actor_photo_auto.isChecked():
        config.emby_on += "actor_photo_auto,"
    if self.Ui.checkBox_actor_pic_replace.isChecked():
        config.emby_on += "actor_replace,"

    if self.Ui.checkBox_actor_photo_kodi.isChecked():
        config.actor_photo_kodi_auto = 1
    else:
        config.actor_photo_kodi_auto = 0
    # endregion

    # region mark
    if self.Ui.checkBox_poster_mark.isChecked():  # 封面添加水印
        config.poster_mark = 1
    else:  # 关闭封面添加水印
        config.poster_mark = 0
    if self.Ui.checkBox_thumb_mark.isChecked():  # 缩略图添加水印
        config.thumb_mark = 1
    else:  # 关闭缩略图添加水印
        config.thumb_mark = 0
    if self.Ui.checkBox_fanart_mark.isChecked():  # 艺术图添加水印
        config.fanart_mark = 1
    else:  # 关闭艺术图添加水印
        config.fanart_mark = 0
    config.mark_size = self.Ui.horizontalSlider_mark_size.value()  # 水印大小
    config.mark_type = ""
    if self.Ui.checkBox_sub.isChecked():  # 字幕
        config.mark_type += "sub,"
    if self.Ui.checkBox_censored.isChecked():  # 有码
        config.mark_type += "youma,"
    if self.Ui.checkBox_umr.isChecked():  # 破解
        config.mark_type += "umr,"
    if self.Ui.checkBox_leak.isChecked():  # 流出
        config.mark_type += "leak,"
    if self.Ui.checkBox_uncensored.isChecked():  # 无码
        config.mark_type += "uncensored,"
    if self.Ui.checkBox_hd.isChecked():  # 4k/8k
        config.mark_type += "hd,"
    if self.Ui.radioButton_not_fixed_position.isChecked():  # 水印位置
        config.mark_fixed = "off"
    elif self.Ui.radioButton_fixed_corner.isChecked():  # 水印位置
        config.mark_fixed = "corner"
    else:
        config.mark_fixed = "on"
    if self.Ui.radioButton_top_left.isChecked():  # 首个水印位置-左上
        config.mark_pos = "top_left"
    elif self.Ui.radioButton_top_right.isChecked():  # 首个水印位置-右上
        config.mark_pos = "top_right"
    elif self.Ui.radioButton_bottom_left.isChecked():  # 首个水印位置-左下
        config.mark_pos = "bottom_left"
    elif self.Ui.radioButton_bottom_right.isChecked():  # 首个水印位置-右下
        config.mark_pos = "bottom_right"
    if self.Ui.radioButton_top_left_corner.isChecked():  # 固定一个位置-左上
        config.mark_pos_corner = "top_left"
    elif self.Ui.radioButton_top_right_corner.isChecked():  # 固定一个位置-右上
        config.mark_pos_corner = "top_right"
    elif self.Ui.radioButton_bottom_left_corner.isChecked():  # 固定一个位置-左下
        config.mark_pos_corner = "bottom_left"
    elif self.Ui.radioButton_bottom_right_corner.isChecked():  # 固定一个位置-右下
        config.mark_pos_corner = "bottom_right"
    if self.Ui.radioButton_top_left_hd.isChecked():  # hd水印位置-左上
        config.mark_pos_hd = "top_left"
    elif self.Ui.radioButton_top_right_hd.isChecked():  # hd水印位置-右上
        config.mark_pos_hd = "top_right"
    elif self.Ui.radioButton_bottom_left_hd.isChecked():  # hd水印位置-左下
        config.mark_pos_hd = "bottom_left"
    elif self.Ui.radioButton_bottom_right_hd.isChecked():  # hd水印位置-右下
        config.mark_pos_hd = "bottom_right"
    if self.Ui.radioButton_top_left_sub.isChecked():  # 字幕水印位置-左上
        config.mark_pos_sub = "top_left"
    elif self.Ui.radioButton_top_right_sub.isChecked():  # 字幕水印位置-右上
        config.mark_pos_sub = "top_right"
    elif self.Ui.radioButton_bottom_left_sub.isChecked():  # 字幕水印位置-左下
        config.mark_pos_sub = "bottom_left"
    elif self.Ui.radioButton_bottom_right_sub.isChecked():  # 字幕水印位置-右下
        config.mark_pos_sub = "bottom_right"
    if self.Ui.radioButton_top_left_mosaic.isChecked():  # 马赛克水印位置-左上
        config.mark_pos_mosaic = "top_left"
    elif self.Ui.radioButton_top_right_mosaic.isChecked():  # 马赛克水印位置-右上
        config.mark_pos_mosaic = "top_right"
    elif self.Ui.radioButton_bottom_left_mosaic.isChecked():  # 马赛克水印位置-左下
        config.mark_pos_mosaic = "bottom_left"
    elif self.Ui.radioButton_bottom_right_mosaic.isChecked():  # 马赛克水印位置-右下
        config.mark_pos_mosaic = "bottom_right"
    # endregion

    # region network
    if self.Ui.radioButton_proxy_http.isChecked():  # http proxy
        config.type = "http"
    elif self.Ui.radioButton_proxy_socks5.isChecked():  # socks5 proxy
        config.type = "socks5"
    elif self.Ui.radioButton_proxy_nouse.isChecked():  # no use proxy
        config.type = "no"
    proxy = self.Ui.lineEdit_proxy.text()  # 代理地址
    config.proxy = proxy.replace("https://", "").replace("http://", "")
    config.timeout = self.Ui.horizontalSlider_timeout.value()  # 超时时间
    config.retry = self.Ui.horizontalSlider_retry.value()  # 重试次数

    custom_website_name = self.Ui.comboBox_custom_website.currentText()
    custom_website_url = self.Ui.lineEdit_custom_website.text()
    if custom_website_url:
        custom_website_url = custom_website_url.strip("/ ")
        setattr(config, f"{custom_website_name}_website", custom_website_url)
    elif hasattr(config, f"{custom_website_name}_website"):
        delattr(config, f"{custom_website_name}_website")
    config.javdb = self.Ui.plainTextEdit_cookie_javdb.toPlainText()  # javdb cookie
    config.javbus = self.Ui.plainTextEdit_cookie_javbus.toPlainText()  # javbus cookie
    config.theporndb_api_token = self.Ui.lineEdit_api_token_theporndb.text()  # api token
    if config.javdb:
        config.javdb = config.javdb.replace("locale=en", "locale=zh")
    # endregion

    # region other
    config.rest_count = int(self.Ui.lineEdit_rest_count.text())  # 间歇刮削文件数量
    config.rest_time = self.Ui.lineEdit_rest_time.text()  # 间歇刮削休息时间
    config.timed_interval = self.Ui.lineEdit_timed_interval.text()  # 循环任务间隔时间

    # 开关汇总
    config.switch_on = ""
    if self.Ui.checkBox_auto_start.isChecked():
        config.switch_on += "auto_start,"
    if self.Ui.checkBox_auto_exit.isChecked():
        config.switch_on += "auto_exit,"
    if self.Ui.checkBox_rest_scrape.isChecked():
        config.switch_on += "rest_scrape,"
    if self.Ui.checkBox_timed_scrape.isChecked():
        config.switch_on += "timed_scrape,"
    if self.Ui.checkBox_remain_task.isChecked():
        config.switch_on += "remain_task,"
    if self.Ui.checkBox_show_dialog_exit.isChecked():
        config.switch_on += "show_dialog_exit,"
    if self.Ui.checkBox_show_dialog_stop_scrape.isChecked():
        config.switch_on += "show_dialog_stop_scrape,"
    if not self.Ui.textBrowser_log_main_2.isHidden():
        config.switch_on += "show_logs,"
    if self.Ui.checkBox_sortmode_delpic.isChecked():
        config.switch_on += "sort_del,"
    if self.Ui.checkBox_net_ipv4_only.isChecked():
        config.switch_on += "ipv4_only,"
    if self.Ui.checkBox_dialog_qt.isChecked():
        config.switch_on += "qt_dialog,"
    if self.Ui.checkBox_theporndb_hash.isChecked():
        config.switch_on += "theporndb_no_hash,"
    if self.Ui.radioButton_hide_close.isChecked():
        config.switch_on += "hide_close,"
    elif self.Ui.radioButton_hide_mini.isChecked():
        config.switch_on += "hide_mini,"
    else:
        config.switch_on += "hide_none,"
    if self.Ui.checkBox_hide_dock_icon.isChecked():
        config.switch_on += "hide_dock,"
    if self.Ui.checkBox_highdpi_passthrough.isChecked():
        config.switch_on += "passthrough,"
    if self.Ui.checkBox_hide_menu_icon.isChecked():
        config.switch_on += "hide_menu,"
    if self.Ui.checkBox_dark_mode.isChecked():
        config.switch_on += "dark_mode,"
    if self.Ui.checkBox_copy_netdisk_nfo.isChecked():
        config.switch_on += "copy_netdisk_nfo,"

    if self.Ui.checkBox_show_web_log.isChecked():  # 显示字段刮削过程信息
        config.show_web_log = "on"
    else:
        config.show_web_log = "off"
    if self.Ui.checkBox_show_from_log.isChecked():  # 显示字段来源网站信息
        config.show_from_log = "on"
    else:
        config.show_from_log = "off"
    if self.Ui.checkBox_show_data_log.isChecked():  # 显示字段内容信息
        config.show_data_log = "on"
    else:
        config.show_data_log = "off"
    if self.Ui.radioButton_log_on.isChecked():  # 开启日志
        config.save_log = "on"
    elif self.Ui.radioButton_log_off.isChecked():  # 关闭日志
        config.save_log = "off"
    if self.Ui.radioButton_update_on.isChecked():  # 检查更新
        config.update_check = "on"
    elif self.Ui.radioButton_update_off.isChecked():  # 不检查更新
        config.update_check = "off"
    config.local_library = self.Ui.lineEdit_local_library_path.text()  # 本地资源库
    config.actors_name = self.Ui.lineEdit_actors_name.text().replace("\n", "")  # 演员名
    config.netdisk_path = self.Ui.lineEdit_netdisk_path.text()  # 网盘路径
    config.localdisk_path = self.Ui.lineEdit_localdisk_path.text()  # 本地磁盘路径
    if self.Ui.checkBox_hide_window_title.isChecked():  # 隐藏窗口标题栏
        config.window_title = "hide"
    else:  # 显示窗口标题栏
        config.window_title = "show"
    # endregion

    # 保存115目录树文件和前缀配置
    config.tree_file = self.Ui.lineEdit_tree_file.text()
    config.tree_file_prefix = self.Ui.lineEdit_tree_file_prefix.text()

    if self.Ui.checkBox_create_link.isChecked():
        config.auto_link = 1
    else:
        config.auto_link = 0

    config_folder = self.Ui.lineEdit_config_folder.text()  # 配置文件目录
    if not os.path.exists(config_folder):
        config_folder = config.folder
    config.path = convert_path(os.path.join(config_folder, config.file))
    config.version = self.localversion
    config.save_config()
    config.update_config()

    try:
        scrape_like_text = Flags.scrape_like_text
        if config.scrape_like == "single":
            scrape_like_text += f" · {config.website_single}"
        if config.soft_link == 1:
            scrape_like_text += " · 软连接开"
        elif config.soft_link == 2:
            scrape_like_text += " · 硬连接开"
        signal.show_log_text(
            f" 🛠 当前配置：{config.path} 保存完成！\n "
            f"📂 程序目录：{get_main_path()} \n "
            f"📂 刮削目录：{get_movie_path_setting()[0]} \n "
            f"💠 刮削模式：{Flags.main_mode_text} · {scrape_like_text} \n "
            f"🖥️ 系统信息：{platform.platform()} \n "
            f"🐰 软件版本：{self.localversion} \n"
        )
    except:
        signal.show_traceback_log(traceback.format_exc())
    try:
        check_proxyChange()  # 更新代理信息
        self._windows_auto_adjust()  # 界面自动调整
    except:
        signal.show_traceback_log(traceback.format_exc())
    self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    self.activateWindow()
    try:
        self.set_label_file_path.emit(
            "🎈 当前刮削路径: \n %s" % get_movie_path_setting()[0]
        )  # 主界面右上角显示提示信息
    except:
        signal.show_traceback_log(traceback.format_exc())
