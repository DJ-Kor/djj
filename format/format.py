# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import re
import time
import logging

import os
import sys

import utils.iddx_configs as IddxConfigs

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from multiprocessing.pool import ThreadPool

from pathlib import Path
from logging import handlers

import pymsteams

from elasticsearch import Elasticsearch, helpers
from elasticsearch import logger as es_logger

sys.path.append(IddxConfigs.IDDX_VENV1_PACKAGE_PATH)
from openpyxl import load_workbook


# from logging.config import fileConfig

# fileConfig('logging.ini')
# logger = logging.getLogger('DATA-MANUFACTURING')

LOG_INDEX_NAME = "cc_index_manager"

DUP_MAC_INDEX_NAME = "cc_dup_mac"
NO_DB_MAC_INDEX_NAME = "cc_blob_no_db_mac"
BLOB_DATE_MAC_JOB = "cc_blob_job_date_mac"

PRODUCT_SIGNAGE = "S"
PRODUCT_LED_SIGNAGE = "L"
PRODUCT_COMMERCIAL = "C"
PRODUCT_SIGNAGE_SOLUTION = "SO"
PRODUCT_COMMERCIAL_SOLUTION = "CO"
PRODUCT_NONE = "None"

COUNT_YES = "Y"
COUNT_NO = "N"

RESULT_SUCCESS = 200
RESULT_FAIL = 400

logger = logging.getLogger(__name__)

# all_df['dpc.led.eth_error.id'].unique()


def init():
    logger.info("init()")


def _getSettingFields(before_json, check_fields):
    new_json = {}
    ext_key_list = []
    for key in check_fields:
        try:
            new_json[key] = before_json[key]
        except:
            continue
    return new_json


def _minDimJson(before_json):
    after_json = {}
    if "event_time" in before_json:
        after_json["event_time"] = before_json["event_time"]
    if "mac_sn" in before_json:
        after_json["mac_sn"] = before_json["mac_sn"]
    if "event_date" in before_json:
        after_json["event_date"] = before_json["event_date"]
    if "dpi" in before_json:
        dpi = before_json["dpi"]
        if dpi is not None:
            if "aud" in dpi:
                aud = dpi["aud"]
                if "a_vol" in aud:
                    after_json["dpi.aud.a_vol"] = aud["a_vol"]
                if "audioout" in aud:
                    after_json["dpi.aud.audioout"] = aud["audioout"]
                if "bal" in aud:
                    after_json["dpi.aud.bal"] = aud["bal"]
                if "bass" in aud:
                    after_json["dpi.aud.bass"] = aud["bass"]
                if "digital_audio_input" in aud:
                    after_json["dpi.aud.digital_audio_input"] = aud["digital_audio_input"]
                if "mode" in aud:
                    after_json["dpi.aud.mode"] = aud["mode"]
                if "sound_out" in aud:
                    after_json["dpi.aud.sound_out"] = aud["sound_out"]
                if "spk" in aud:
                    after_json["dpi.aud.spk"] = aud["spk"]
                if "tr" in aud:
                    after_json["dpi.aud.tr"] = aud["tr"]
                if "vol" in aud:
                    after_json["dpi.aud.vol"] = aud["vol"]
            if "baudrate" in dpi:
                after_json["baudrate"] = dpi["baudrate"]
            if "fail_over" in dpi:
                fail_over = dpi["fail_over"]
                if "backup_via_storage" in fail_over:
                    after_json["dpi.fail_over.backup_via_storage"] = fail_over["backup_via_storage"]
                if "backup_via_str_file" in fail_over:
                    after_json["dpi.fail_over.backup_via_str_file"] = fail_over["backup_via_str_file"]
                if "backup_via_str_interval" in fail_over:
                    after_json["dpi.fail_over.backup_via_str_interval"] = fail_over["backup_via_str_interval"]
                if "fail_over" in fail_over:
                    after_json["dpi.fail_over.fail_over"] = fail_over["fail_over"]
                if "priority_1" in fail_over:
                    priority_1 = fail_over["priority_1"]
                    if "key" in priority_1:
                        after_json["dpi.fail_over.priority_1.key"] = priority_1["key"]
                    if "name" in priority_1:
                        after_json["dpi.fail_over.priority_1.name"] = priority_1["name"]
            if "firm_ver" in dpi:
                after_json["dpi.firm_ver"] = dpi["firm_ver"]
            if "options_spec" in dpi:
                options_spec = dpi["options_spec"]
                if "advanced" in options_spec:
                    advanced = options_spec["advanced"]
                    if "digitalAudioInput" in advanced:
                        after_json["dpi.options_spec.advanced.digitalAudioInput"] = advanced["digitalAudioInput"]
                    if "pmMode" in advanced:
                        after_json["dpi.options_spec.advanced.pmMode"] = advanced["pmMode"]
                    if "powerOnStatus" in advanced:
                        after_json["dpi.options_spec.advanced.powerOnStatus"] = advanced["powerOnStatus"]
                    if "soundOut" in advanced:
                        soundOut = advanced["soundOut"]
                        if "type" in soundOut:
                            after_json["dpi.options_spec.advanced.soundOut.type"] = soundOut["type"]
                        if "value" in soundOut:
                            after_json["dpi.options_spec.advanced.soundOut.value"] = soundOut["value"]
                if "failOver" in options_spec:
                    failOver = options_spec["failOver"]
                    if "backupViaStorageInterval" in failOver:
                        after_json["dpi.options_spec.failOver.backupViaStorageInterval"] = failOver["backupViaStorageInterval"]
            if "pic" in dpi:
                pic = dpi["pic"]
                if "b_gain" in pic:
                    after_json["dpi.pic.b_gain"] = pic["b_gain"]
                if "b_off" in pic:
                    after_json["dpi.pic.b_off"] = pic["b_off"]
                if "brgt" in pic:
                    after_json["dpi.pic.brgt"] = pic["brgt"]
                if "color" in pic:
                    after_json["dpi.pic.color"] = pic["color"]
                if "color_t" in pic:
                    after_json["dpi.pic.color_t"] = pic["color_t"]
                if "cont" in pic:
                    after_json["dpi.pic.cont"] = pic["cont"]
                if "ext_rotation" in pic:
                    after_json["dpi.pic.ext_rotation"] = pic["ext_rotation"]
                if "g_gain" in pic:
                    after_json["dpi.pic.g_gain"] = pic["g_gain"]
                if "g_off" in pic:
                    after_json["dpi.pic.g_off"] = pic["g_off"]
                if "ism" in pic:
                    after_json["dpi.pic.ism"] = pic["ism"]
                if "mode" in pic:
                    after_json["dpi.pic.mode"] = pic["mode"]
                if "p_h" in pic:
                    after_json["dpi.pic.p_h"] = pic["p_h"]
                if "p_v" in pic:
                    after_json["dpi.pic.p_v"] = pic["p_v"]
                if "r_gain" in pic:
                    after_json["dpi.pic.r_gain"] = pic["r_gain"]
                if "r_off" in pic:
                    after_json["dpi.pic.r_off"] = pic["r_off"]
                if "s_h" in pic:
                    after_json["dpi.pic.s_h"] = pic["s_h"]
                if "s_v" in pic:
                    after_json["dpi.pic.s_v"] = pic["s_v"]
                if "scr_rotation" in pic:
                    after_json["dpi.pic.scr_rotation"] = pic["scr_rotation"]
                if "sharp" in pic:
                    after_json["dpi.pic.sharp"] = pic["sharp"]
                if "tint" in pic:
                    after_json["dpi.pic.tint"] = pic["tint"]
            if "play_via_url" in dpi:
                play_via_url = dpi["play_via_url"]
                if "mode" in play_via_url:
                    after_json["dpi.play_via_url.mode"] = play_via_url["mode"]
                if "url" in play_via_url:
                    after_json["dpi.play_via_url.url"] = play_via_url["url"]
            if "power" in dpi:
                power = dpi["power"]
                if "pm_mode" in power:
                    after_json["dpi.power.pm_mode"] = power["pm_mode"]
                if "power_on_status" in power:
                    after_json["dpi.power.power_on_status"] = power["power_on_status"]
            if "setid" in dpi:
                after_json["dpi.setid"] = dpi["setid"]
            if "si_server" in dpi:
                si_server = dpi["si_server"]
                if "app_launch_mode" in si_server:
                    after_json["dpi.si_server.app_launch_mode"] = si_server["app_launch_mode"]
                if "app_type" in si_server:
                    after_json["dpi.si_server.app_type"] = si_server["app_type"]
                if "autoset" in si_server:
                    after_json["dpi.si_server.autoset"] = si_server["autoset"]
                if "fqdn_addr" in si_server:
                    after_json["dpi.si_server.fqdn_addr"] = si_server["fqdn_addr"]
                if "fqdn_mode" in si_server:
                    after_json["dpi.si_server.fqdn_mode"] = si_server["fqdn_mode"]
                if "proxy_exceptions" in si_server:
                    after_json["dpi.si_server.proxy_exceptions"] = si_server["proxy_exceptions"]
                if "proxy_ip_addr" in si_server:
                    after_json["dpi.si_server.proxy_ip_addr"] = si_server["proxy_ip_addr"]
                if "proxy_passwd" in si_server:
                    after_json["dpi.si_server.proxy_passwd"] = si_server["proxy_passwd"]
                if "proxy_port" in si_server:
                    after_json["dpi.si_server.proxy_port"] = si_server["proxy_port"]
                if "proxy_server_enable" in si_server:
                    after_json["dpi.si_server.proxy_server_enable"] = si_server["proxy_server_enable"]
                if "proxy_username" in si_server:
                    after_json["dpi.si_server.proxy_username"] = si_server["proxy_username"]
                if "secure" in si_server:
                    after_json["dpi.si_server.secure"] = si_server["secure"]
                if "server_ip" in si_server:
                    after_json["dpi.si_server.server_ip"] = si_server["server_ip"]
                if "server_port" in si_server:
                    after_json["dpi.si_server.server_port"] = si_server["server_port"]
            if "sys" in dpi:
                sys = dpi["sys"]
                if "blit" in sys:
                    after_json["dpi.sys.blit"] = sys["blit"]
                if "ir" in sys:
                    after_json["dpi.sys.ir"] = sys["ir"]
                if "lang" in sys:
                    after_json["dpi.sys.lang"] = sys["lang"]
                if "osd" in sys:
                    after_json["dpi.sys.osd"] = sys["osd"]
                if "usb_lock" in sys:
                    after_json["dpi.sys.usb_lock"] = sys["usb_lock"]
                if "wol" in sys:
                    after_json["dpi.sys.wol"] = sys["wol"]
            if "tile" in dpi:
                tile = dpi["tile"]
                if "id" in tile:
                    after_json["dpi.tile.id"] = tile["id"]
                if "mode" in tile:
                    after_json["dpi.tile.mode"] = tile["mode"]
                if "natural" in tile:
                    after_json["dpi.tile.natural"] = tile["natural"]
            if "timer" in dpi:
                timer = dpi["timer"]
                if "delay" in timer:
                    after_json["dpi.timer.delay"] = timer["delay"]
                if "detect_sch" in timer:
                    after_json["dpi.timer.detect_sch"] = timer["detect_sch"]
                if "off" in timer:
                    after_json["dpi.timer.off"] = timer["off"]
                if "off_sch" in timer:
                    after_json["dpi.timer.off_sch"] = timer["off_sch"]
                if "on_sch" in timer:
                    after_json["dpi.timer.on_sch"] = timer["on_sch"]
                if "on" in timer:
                    after_json["dpi.timer.on"] = timer["on"]
                if "on_input" in timer:
                    after_json["dpi.timer.on_input"] = timer["on_input"]
                if "onoff_sch" in timer:
                    after_json["dpi.timer.onoff_sch"] = timer["onoff_sch"]
            if "play_via_url" in dpi:
                play_via_url = dpi["play_via_url"]
                if "mode" in play_via_url:
                    after_json["dpi.play_via_url.mode"] = play_via_url["mode"]
                if "" in play_via_url:
                    after_json["dpi.play_via_url."] = play_via_url[""]
                if "" in play_via_url:
                    after_json["dpi.play_via_url."] = play_via_url[""]
        else:
            after_json["dpi"] = ""
    if "dpc" in before_json:
        dpc = before_json["dpc"]
        if dpc is not None:
            if "timer" in dpc:
                timer = dpc["timer"]
                if "auto_off" in timer:
                    after_json["dpc.timer.auto_off"] = timer["auto_off"]
                if "dpm" in timer:
                    after_json["dpc.timer.dpm"] = timer["dpm"]
                if "sleep" in timer:
                    after_json["dpc.timer.sleep"] = timer["sleep"]
                if "standby" in timer:
                    after_json["dpc.timer.standby"] = timer["standby"]
            if "agnt_ver" in dpc:
                after_json["dpc.agnt_ver"] = dpc["agnt_ver"]
            if "daylight" in dpc:
                daylight = dpc["daylight"]
                if "off_time" in daylight:
                    after_json["dpc.daylight.off_time"] = daylight["off_time"]
                if "on_time" in daylight:
                    after_json["dpc.daylight.on_time"] = daylight["on_time"]
            if "edid" in dpc:
                edid = dpc["edid"]
                if "checksum" in edid:
                    after_json["dpc.edid.checksum"] = edid["checksum"]
                if "inputName" in edid:
                    after_json["dpc.edid.inputName"] = edid["inputName"]
            if "fan" in dpc:
                after_json["dpc.fan"] = dpc["fan"]
            if "firm_ver" in dpc:
                after_json["dpc.firm_ver"] = dpc["firm_ver"]
            if "hdmi" in dpc:
                hdmi = dpc["hdmi"]
                if "checksum" in hdmi:
                    after_json["dpc.hdmi.hdcp"] = hdmi["hdcp"]
            if "power_on_off" in dpc:
                power_on_off = dpc["power_on_off"]
                if "action" in power_on_off:
                    after_json["dpc.power_on_off.action"] = power_on_off["action"]
                if "date" in power_on_off:
                    after_json["dpc.power_on_off.date"] = power_on_off["date"]
                if "method" in power_on_off:
                    after_json["dpc.power_on_off.method"] = power_on_off["method"]
            if "signal" in dpc:
                after_json["dpc.signal"] = dpc["signal"]
            if "sys" in dpc:
                sys = dpc["sys"]
                if "ar" in sys:
                    after_json["dpc.sys.ar"] = sys["ar"]
                if "date" in sys:
                    after_json["dpc.sys.date"] = sys["date"]
                if "energy" in sys:
                    after_json["dpc.sys.energy"] = sys["energy"]
                if "input" in sys:
                    after_json["dpc.sys.input"] = sys["input"]
                if "lamp" in sys:
                    after_json["dpc.sys.lamp"] = sys["lamp"]
                if "pwr" in sys:
                    after_json["dpc.sys.pwr"] = sys["pwr"]
                if "scr_off" in sys:
                    after_json["dpc.sys.scr_off"] = sys["scr_off"]
                if "time" in sys:
                    after_json["dpc.sys.time"] = sys["time"]
            if "tcon" in dpc:
                after_json["dpc.tcon"] = dpc["tcon"]
            if "temp" in dpc:
                after_json["dpc.temp"] = dpc["temp"]
        else:
            after_json["dpc"] = ""
    if "mpc" in before_json:
        mpc = before_json["mpc"]
        if mpc is not None:
            if "app1" in mpc:
                app1 = mpc["app1"]
                if "stat" in app1:
                    after_json["mpc.app1.stat"] = app1["stat"]
            if "disconnectedHisotry" in mpc:
                after_json["mpc.disconnectedHisotry"] = mpc["disconnectedHisotry"]
            if "time" in mpc:
                after_json["mpc.time"] = mpc["time"]
            if "timezone" in mpc:
                after_json["mpc.timezone"] = mpc["timezone"]
            if "uptime" in mpc:
                after_json["mpc.uptime"] = mpc["uptime"]
            if "agnt_ver" in mpc:
                after_json["mpc.agnt_ver"] = mpc["agnt_ver"]
        else:
            after_json["mpc"] = ""
    if "mpi" in before_json:
        mpi = before_json["mpi"]
        if mpi is not None:
            if "agnt_ver" in mpi:
                after_json["mpi.agnt_ver"] = mpi["agnt_ver"]
            if "firm_ver" in mpi:
                after_json["mpi.firm_ver"] = mpi["firm_ver"]
            if "location" in mpi:
                location = mpi["location"]
                if "ip" in location:
                    after_json["mpc.location.ip"] = app1["ip"]
            if "remote_access_ready" in mpi:
                after_json["mpi.remote_access_ready"] = mpi["remote_access_ready"]
        else:
            after_json["mpi"] = ""
    return after_json


def get_series_name(model, product_type=PRODUCT_SIGNAGE):
    if model is None or model == PRODUCT_NONE or pd.isna(model):
        return PRODUCT_NONE

    model_name = str(model).strip().upper()

    if model_name.startswith("PCS-"):
        model_name = "PCS"
    elif model_name.startswith("PCD-"):
        model_name = "PCD"
    elif model_name.startswith("STB-"):
        model_name = "STB"
    elif model_name.startswith("HSP-"):
        model_name = "HSP"
    else:
        if len(model_name) < 3 or model_name.find("년") != -1:
            return model_name
        numeric_name = "0123456789"
        secname = model_name[1:]
        if any(secname.startswith(x) for x in numeric_name):
            model_name = model_name[2:]

        # Commercial TV 향지 정보 제외
        if product_type == PRODUCT_COMMERCIAL and len(model_name) > 8:
            model_name = model_name[:-3]

    return model_name


def get_product_category(product_type, model):
    if product_type == PRODUCT_NONE and model != PRODUCT_NONE:
        model_name = str(model).strip().upper().replace(" ", "")
        if model_name.find("SUPERSIGN") != -1 or model_name.find("365CARE") != -1 or model_name.find("LEDASSISTANT") != -1:
            return "Signage Solution"
        if model_name.find("PCD") != -1 or model_name.find("PCA") != -1 or model_name.find("HSP") != -1:
            return "Hotel Solution"
        return PRODUCT_NONE

    if model is None or model == PRODUCT_NONE or pd.isna(model):
        return PRODUCT_NONE

    signage_series = {
        "S": "일반형(Standard)",
        "U": "일반형(UHD)",
        "B": "이형(Ultra Stretch)",
        "X": "Outdoor(고휘도)",
        "V": "비디오월",
        "T": "터치(전자칠판)",
        "E": "OLED",
        "W": "투명",
        "R": "미러",
        "K": "키오스크",
        "L": "LED",
    }

    tv_series = {
        "H": "Hotel",
        "C": "Commercial Lite",
        "M": "Hospital",
        "V": "Cruise",
        "S": "Smart TV Signage",
        "N": "Tuner-less",
        "A": "ARM TV",
        "L": "Long Term Care TV",
    }

    model_name = get_series_name(model, product_type)
    model_name = model_name.replace(" ", "")

    p_category = PRODUCT_NONE
    if model_name.find("SUPERSIGN") != -1 or model_name.find("365CARE") != -1 or model_name.find("LED ASSISTANT") != -1:
        p_category = "Signage Solution"
    elif model_name.find("PCD") != -1 or str(model).find("PCA") != -1 or str(model).find("HSP") != -1:
        p_category = "Commercial Solution"
    elif model_name.startswith("ACC-"):
        p_category = "Accessory"
    elif model_name.startswith("WP"):
        p_category = "Signage Box"
    elif model_name.startswith("STB-"):
        p_category = "Settop Box"
    else:
        if product_type == PRODUCT_SIGNAGE:
            p_category = signage_series.get(model_name[0], PRODUCT_NONE)
        elif product_type == PRODUCT_COMMERCIAL and len(model_name) > 5:
            p_category = tv_series.get(model_name[5], PRODUCT_NONE)

    return p_category


def get_model_year(product_type, model):
    if model is None or model == PRODUCT_NONE or pd.isna(model) or product_type == PRODUCT_NONE:
        return "None"
    if len(model) < 3 or model.find("년") != -1 or model.startswith("ACC-"):
        return "None"

    signage_year = {"A": "2014", "B": "2015", "C": "2016", "D": "2017", "E": "2018", "F": "2019", "G": "2020"}
    tv_year = {"X": "2015", "W": "2016", "V": "2017", "U": "2018", "T": "2019", "S": "2020"}
    stb_year = {"2": "2014", "3": "2015", "4": "-", "5": "2016", "6": "2020", "7": "2021"}

    model_name = get_series_name(model, product_type)
    if model_name.startswith("STB-"):
        return stb_year.get(model_name[4], "None")
    if product_type == PRODUCT_SIGNAGE:
        return signage_year.get(model_name[-1], "None")
    if product_type == PRODUCT_COMMERCIAL and len(model_name) > 2:
        return tv_year.get(model_name[1], "None")
    return "None"


def save_csv_file(file_loc, data_frame):
    logger.info(f"Save to csv: {file_loc}")
    data_frame.to_csv(file_loc, encoding="utf-8", header=True, index=False)
    logger.info("End saving")


def convert_digit_to_date(datestr, master_year):
    def validate_y_m(date_text):
        try:
            datetime.strptime(date_text, "%Y-%m")
            return True
        except ValueError:
            return False

    def validate_y_m2(date_text):
        try:
            datetime.strptime(date_text, "%y.%m월")
            return True
        except ValueError:
            return False

    if isinstance(datestr, int):
        datestr = str(datestr)
    if isinstance(datestr, str):
        datestr = datestr.strip().replace(" ", "").replace("`", "").replace("->", "→").upper()
        numeric_name = "0123456789"
        if any(datestr.startswith(x) for x in numeric_name):
            if validate_y_m2(datestr):
                _date = datetime.strptime(datestr, "%y.%m월")
                _date = _date + relativedelta(day=31)
                datestr = _date.strftime("%Y-%m-%d")
            else:
                dstr = str(master_year) + "-" + datestr
                if dstr.endswith("월"):
                    dstr = dstr[:-1]
                if validate_y_m(dstr):
                    _date = datetime.strptime(dstr, "%Y-%m")
                    _date = _date + relativedelta(day=31)
                    datestr = _date.strftime("%Y-%m-%d")
    try:
        if isinstance(datestr, str):
            datetime.strptime(datestr, "%Y-%m-%d")
            return datestr
        return np.nan
    except ValueError:
        return np.nan


def convert_signage_date_str(datestr, master_year):
    # 17년 8월 -> 2017.08.31
    def validate_y_m_d(date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S,%Z")
            return True
        except ValueError:
            return False

    def validate_y_m(date_text):
        try:
            datetime.strptime(date_text, "%Y년%m월")
            return True
        except ValueError:
            return False

    def validate_m(date_text):
        try:
            datetime.strptime(date_text, "%m월")
            return True
        except ValueError:
            return False

    def validate_y_m2(date_text):
        try:
            datetime.strptime(date_text, "%y.%m월")
            return True
        except ValueError:
            return False

    d_strpt = None
    if isinstance(datestr, str):
        datestr = datestr.strip().replace("`", "").replace("->", "→").upper()
        # numeric_name = '0123456789'
        # if any(datestr.startswith(x) for x in numeric_name):
        #     datestr = datestr.replace(' ','')
        datestr = datestr.replace(" ", "")
        index = datestr.find("→")
        if index >= 0:
            date_arr = datestr.split("→")
            datestr = date_arr[-1]

        index = datestr.find("(")
        if index >= 0:
            datestr = datestr[:index]

        # year.month/weekW, year/month/weekW 6/4W
        # without W year/month/day

        if isinstance(datestr, str):
            if datestr.find("년") > 0:
                datestr = "20" + datestr

            if validate_y_m_d(datestr) is True:
                d_strpt = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S,%Z")
                # datestr = d.strftime('%Y-%m-%d')

            elif validate_y_m(datestr) is True:
                #  2017-07-31  12:00:00 AM ->2017-07-31
                d_strpt = datetime.strptime(datestr, "%Y년%m월")
                d_strpt = d_strpt + relativedelta(day=31)
                # datestr = d_strpt.strftime('%Y-%m-%d')

            elif validate_y_m2(datestr) is True:
                #  2017-07-31  12:00:00 AM ->2017-07-31
                d_strpt = datetime.strptime(datestr, "%y.%m월")
                d_strpt = d_strpt + relativedelta(day=31)
                # datestr = d_strpt.strftime('%Y-%m-%d')

            elif validate_m(datestr) is True:
                datestr = str(master_year) + "-" + datestr
                d_strpt = datetime.strptime(datestr, "%Y-%m월")
                d_strpt = d_strpt + relativedelta(day=31)
                # datestr = d.strftime('%Y-%m-%d')

            if d_strpt is not None and isinstance(d_strpt, date):
                datestr = str(d_strpt.strftime("%Y-%m-%d"))

    try:
        if isinstance(datestr, str):
            datetime.strptime(datestr, "%Y-%m-%d")
            return datestr
        return np.nan
    except ValueError:
        return np.nan


def convert_commercial_date_str(datestr, master_year):
    #  6/4W => 2017-6-23
    #  yyyy-MM-dd HH:mm:ss -> yyyy-MM-dd
    # curstr = datestr

    def validate_y(date_text):
        try:
            datetime.strptime(date_text, "%Y년")
            return True
        except ValueError:
            return False

    def validate(date_text):
        index = date_text.find(",")
        if index > 0:
            date_text = date_text[:index]
        try:
            datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S,%Z")
            return True
        except ValueError:
            return False

    if isinstance(datestr, datetime):
        return datestr.strftime("%Y-%m-%d")

    if isinstance(datestr, str) is False:
        return np.nan

    datestr = datestr.strip().replace("`", "").replace("->", "→").replace("=>", "→").upper()
    # print(datestr)
    # numeric_name = '0123456789'
    # if any(datestr.startswith(x) for x in numeric_name):
    #     datestr = datestr.replace(' ','')
    # datestr = datestr.replace(' ','')

    # 2016년, 2017년
    if validate_y(datestr) is True:
        d_strpt = datetime.strptime(datestr + "-01-01", "%Y-%m-%d")
        datestr = str(d_strpt.strftime("%Y-%m-%d"))
        return datestr

    # 날짜 변경 이력
    if datestr.find("→") >= 0:
        date_arr = datestr.split("→")
        datestr = date_arr[-1]

    # 지역별 정보가 여러개인 경우 'EU 11/2W, MEA 11/2W', 첫번째 데이터만 변환
    if datestr.find(",") >= 0:
        date_arr = datestr.split(",")
        datestr = date_arr[0]

    # 날짜 정보에 부가적으로 붙은 정보는 무시
    index = datestr.find("(")
    if index >= 0:
        datestr = datestr[:index]

    # '아시아 : 10/1W'
    index = datestr.find(":")
    if index >= 0:
        date_arr = datestr.split(":")
        datestr = date_arr[-1]

    # 5월
    datestr = datestr.strip()
    if datestr.find("월") >= 0:
        datestr = datestr + "-01"
        try:
            d_strpt = datetime.strptime(datestr, "%m월-%d")
            datestr = str(d_strpt.strftime("%Y-%m-%d"))
            return datestr
        except ValueError:
            return np.nan

    # '16/1Q
    index = datestr.find("'")
    if index != -1:
        if datestr.find("Q") >= 0:
            datestr = datestr.replace("'", "")
            index = datestr.find("/")
            if index >= 0:
                date_arr = datestr.split("/")
                year = get_master_year(date_arr[0])
                months = {"1Q": "3", "2Q": "6", "3Q": "9", "4Q": "12"}
                key = date_arr[1]
                key = key.upper()
                month = "12"
                if key in months.keys():
                    month = months[key]
                try:
                    d_strpt = datetime.strptime(year + "-" + month + "-01", "%Y-%m-%d")
                    datestr = str(d_strpt.strftime("%Y-%m-%d"))
                    return datestr
                except ValueError:
                    return np.nan
        else:
            date_arr = datestr.split(" ")
            datestr = date_arr[-1]

    # year.month/weekW, year/month/weekW 6/4W
    # without W year/month/day
    if isinstance(datestr, str):
        datestr = datestr.strip()
        index = datestr.find("/")
        if index >= 0:
            datestr = datestr.replace(".", "/")
            date_arr = datestr.split("/")
            if len(date_arr) < 3:
                date_arr.insert(0, master_year)
            year = get_master_year(date_arr[0])
            month = date_arr[1]
            if month.find(" ") >= 0:  # 'EU 11/2W'
                month = month.split(" ")[-1]
            week = date_arr[2]

            if week.find("W") >= 0:
                week = week.replace("W", "")
                try:
                    # 월/주 단위를 연간 주 단위로 변환
                    weeknumber = datetime.strptime(year + "-" + month + "-01", "%Y-%m-%d").date().isocalendar()[1]
                    weeknumber = weeknumber + int(week) - 1
                    d_strpt = year + "-" + str(weeknumber)
                    day = datetime.strptime(d_strpt + "-1", "%Y-%W-%w").date()
                    # Friday
                    d_strpt = day + timedelta(days=4)
                    # 다음달로 넘어가는 경우 해당 달의 마지막 날로 변경
                    if str(month) != str(d_strpt.month):
                        d_strpt = d_strpt.replace(day=1) - timedelta(days=1)
                except ValueError:
                    # 6/23W: 월/일W로 표시된 경우
                    d_strpt = datetime.strptime(year + "-" + month + "-" + week, "%Y-%m-%d")
                    # return ''
            else:  # 월/일
                index = datestr.find(" ")
                if index >= 0:  # '`15 1/25'
                    date_arr = datestr.split(" ")
                    year = get_master_year(date_arr[0])
                    datestr = date_arr[-1]
                try:
                    d_strpt = datetime.strptime(year + "/" + datestr, "%Y/%m/%d")
                except ValueError:
                    try:
                        d_strpt = datetime.strptime(year + "-" + month + "-01", "%Y-%m-%d")
                    except ValueError:
                        return np.nan

            datestr = str(d_strpt.strftime("%Y-%m-%d"))

        elif validate(datestr) is True:
            #  2017-07-31  12:00:00 AM ->2017-07-31
            # print (datestr)
            index = datestr.find(",")
            if index > 0:
                datestr = datestr[:index]
            d_strpt = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S,%Z")
            datestr = str(d_strpt.strftime("%Y-%m-%d"))

    try:
        if isinstance(datestr, str):
            datetime.strptime(datestr, "%Y-%m-%d")
            return datestr
        return np.nan
    except ValueError:
        return np.nan


def convert_consumer_date_str(datestr):
    if datestr == np.nan or datestr == "-" or str(datestr).find("/") >= 0:
        return datestr

    try:
        d_strpt = datetime.strptime(str(datestr), "%Y-%m-%d %H:%M:%S")
        datestr = str(d_strpt.strftime("%Y-%m-%d"))
        return datestr
    except ValueError:
        return datestr


def search_all_issue_key_from_db(dbutil, table_name):
    jira_list = []
    try:
        ret_val = dbutil.execute("SELECT issue_key, updated FROM " + table_name)
        cursor = ret_val.cursor
        jira_list = dict(cursor.fetchall())
        # jira_list = [item[0] for item in cursor.fetchall()]
        # jira_list = [dict((zip(*cursor.description)[0], row[0])) for row in cursor.fetchall()]
    except Exception as ex:
        logger.error(ex)

    return jira_list


def get_product_grade(gradestr):
    grade = np.nan
    if isinstance(gradestr, str):
        # LED Outsourcing 등급
        if gradestr == "Y":
            grade = gradestr
        elif gradestr == "TBD" or len(gradestr) == 0:
            grade = np.nan
        else:
            match = re.search(r"BOM\s*파생", gradestr.upper())
            if match:
                grade = "D_AV"
            else:
                grade = gradestr
            #     match = re.findall(r"\w+_\w+", gradestr.upper())
            #     if len(match) > 0:
            #         grade = match[-1]

    return grade


def get_last_name_value(model_name):
    conv_name = np.nan
    if isinstance(model_name, str):
        conv_name = model_name.replace("->", "→").replace("=>", "→").replace(",", "").strip()
        index = conv_name.find("→")
        if index >= 0:
            str_arr = conv_name.split("→")
            conv_name = str_arr[-1]

    return conv_name


def get_master_year(master_year):
    now = datetime.now()
    if len(master_year) == 0 or master_year is None:
        return now.strftime("%Y")
    if len(master_year) < 4:
        return "20" + master_year
    return master_year


def get_model_name_list(model_name):
    conv_name = np.nan
    str_arr = [model_name]
    if isinstance(model_name, str):
        conv_name = model_name.replace("->", "→").replace("=>", "→").replace(",", "").strip()
        index = conv_name.find("→")
        if index >= 0:
            str_arr = conv_name.split("→")

    return str_arr


def save_data_to_excel(df_temp, output_path, filename, index=False):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    now = datetime.now()
    n_time = now.strftime("%y%m%d_%H%M")

    file_loc = os.path.join(output_path, filename + "_" + n_time + ".xlsx")
    logger.info(f"save_data_to_excel: filename={file_loc}")
    # print(f"save_data_to_excel: filename={file_loc}")
    df_temp.to_excel(file_loc, sheet_name=filename[:10], header=True, index=index)
    # df.to_csv(file_loc, encoding='utf-8', header=True, index=False)


def parse_master_year_version(filename, file_type="consumer"):
    logger.info(f"parse_master_year_version: filename={filename}")
    # Master Year
    master_year = ""
    if file_type == "material":  # 18년 19년 20년
        match = re.findall(r"\d\d(?:년|Y)", filename.upper())
        if match:
            master_year = match[-1][:-1]
    else:
        match = re.search(r"\d\d(?:년|Y)", filename.upper())
        if match:
            master_year = match.group()[:-1]
    master_year = get_master_year(master_year)
    # Master Version
    if file_type == "module":
        match = re.search(r"V\d+[.]\d+[.]\d+", filename.upper())
    else:
        # match = re.search(r'V\d+[.]\d+', filename.upper())
        match = re.search(r"(?:V|REV[.])\d+[.]\d+", filename.upper())
    if match:
        if str(match.group()).find("REV") != -1:
            master_version = match.group()[4:]
        else:
            master_version = match.group()[1:]
        if file_type != "module":
            try:
                master_version = round(float(master_version), 1)
            except Exception as ex:
                logger.error(ex)
                master_version = 1.0
    else:
        master_version = 1.0
    logger.info(f"parse_master_year_version: master_year={str(master_year)}, master_version={str(master_version)}")

    return master_year, str(master_version)


def make_power_map_data(master_year, master_version, db_util, upload_master="consumer_master"):
    logger.info("make_power_map_data")

    if upload_master == "consumer_master":
        sql = "SELECT * FROM consumer_master WHERE year={0} and version={1} ORDER BY id ASC".format(
            master_year, master_version)
    else:
        # sql = 'SELECT * FROM consumer_master WHERE year={0} and version=(SELECT MAX(version) from consumer_master WHERE year={0})'.format(master_year)
        sql = "SELECT * FROM consumer_master WHERE year={0} ORDER BY version DESC, id ASC".format(master_year)

    logger.info(f"make_power_map_data: sql={sql}")
    df_consumer = pd.read_sql(sql=sql, con=db_util.db_engine())
    df_consumer = df_consumer.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df_consumer.dropna(subset=["power_power_p_n"], inplace=True)
    df_consumer = df_consumer.groupby(["consumer_series_name", "tool_name", "inch_number"]).first().reset_index()

    # if upload_master == 'consumer_master':
    #     sql = '''
    #         SELECT * FROM dev_master WHERE product_type='{0}' AND year={1}
    #         '''.format(PRODUCT_COMMERCIAL, master_year)
    # else:
    #     sql = '''
    #         SELECT * FROM dev_master WHERE product_type='{0}' AND year={1} AND version={2}
    #         '''.format(PRODUCT_COMMERCIAL, master_year, master_version)
    sql = """
        SELECT * FROM dev_master WHERE product_type='{0}' AND year={1} AND version=(SELECT MAX(version) from dev_master WHERE year={1} and product_type='{0}')
        """.format(
        PRODUCT_COMMERCIAL, master_year
    )
    logger.info(f"make_power_map_data: sql={sql}")
    df_dev = pd.read_sql(sql=sql, con=db_util.db_engine())
    df_dev = df_dev.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    df_dev["inch_number"] = df_dev["inch_number"].map(pd.to_numeric, errors="coerce")
    df_dev["inch_number"] = df_dev["inch_number"].fillna(0.0).astype(int)
    df_consumer["inch_number"] = df_consumer["inch_number"].map(pd.to_numeric, errors="coerce")
    df_consumer["inch_number"] = df_consumer["inch_number"].fillna(0.0).astype(int)

    cols = ["consumer_series_name", "tool_name", "inch_number"]
    df_merge = pd.merge(df_dev, df_consumer, on=cols, how="inner")

    df_merge.dropna(subset=["power_power_p_n_y"], inplace=True)
    # df_merge.drop(df_merge[df_merge['power_power_p_n_x'] == df_merge['power_power_p_n_y']].index, inplace=True)
    df_merge.fillna("", inplace=True)
    df_group = df_merge.groupby(["id_x"]).first().reset_index()
    # df_group['master_year'] = master_year
    # df_group['master_version'] = master_version

    # common_utils.save_data_to_excel(df_group, OUTPUT_PATH, 'dev_consumer_power_map', True)
    return df_group


def update_dev_consumer_power_map(master_year, master_version, db_util, upload_master="consumer_master"):
    logger.info("update_dev_consumer_power_map")

    df_group = make_power_map_data(master_year, master_version, db_util, upload_master)
    # common_utils.save_data_to_excel(df_group, OUTPUT_PATH, 'dev_consumer_power_map', True)

    logger.info("save to mysql table=dev_consumer_power_map")
    sql_query = []
    for _, row in df_group.iterrows():
        # self.logger.debug('save_data_to_db: row_number='+str(row_number))
        sql_query.append(
            """
            INSERT INTO dev_consumer_power_map (
                consumer_master_id, consumer_series_name, model_name, seq, consumer_year, consumer_version, dev_master_year, dev_master_version, dev_master_id
            )
            VALUES
                ({0},'{1}','{2}',{3},{4},'{5}',{6},'{7}',{8})
            ON DUPLICATE KEY UPDATE
                consumer_master_id={0}, model_name='{2}', seq={3}, dev_master_year={6}, dev_master_version='{7}'
            """.format(
                row["id_y"],
                row["consumer_series_name"],
                row["model_name_x"],
                row["seq"],
                row["year_y"],
                row["version_y"],
                row["year_x"],
                row["version_x"],
                row["id_x"],
            )
        )

    for sql in sql_query:
        try:
            db_util.execute(sql)
        except Exception as ex:
            logger.error(f"sql query={sql}")
            logger.error(ex)
            continue


def save_doc_to_excel(df_temp, file_loc, sheet_name):
    logger.info(f"save_doc_to_excel: file_loc={file_loc}, sheet_name={sheet_name}")

    if not os.path.isfile(file_loc):
        df_temp.to_excel(file_loc, sheet_name=sheet_name, header=True, index=False)
    else:
        book = load_workbook(file_loc)
        writer = pd.ExcelWriter(file_loc, engine="openpyxl")
        writer.book = book
        df_temp.to_excel(writer, sheet_name=sheet_name, header=True, index=False)
        writer.save()
        writer.close()


def make_es_index(e_search, index_name):
    logger.info(f"make_es_index: index_name={index_name}")
    if e_search.indices.exists(index=index_name):
        # es.indices.delete(index=index_name)
        return

    e_search.indices.create(index=index_name)


def do_es_bulk(e_search, filename, doc_data, index_name, folder_path=""):
    logger.info(f"do_bulk: index_name={index_name}")
    make_es_index(e_search, index_name)
    # update or insert by filename
    query = {
        "bool": {"must": [{"match": {"filename": filename}}, {"match": {"folder_path": folder_path}}]},
    }
    res = e_search.search(index=index_name, query=query)
    hits = res["hits"]["hits"]
    if len(hits) > 0:
        doc = hits[0]
        doc_id = doc["_id"]
        e_search.update(index=index_name, id=doc_id, doc=doc)
    else:
        e_search.index(index=index_name, body=doc_data)


def get_logger(filename=None, name=None, level=logging.DEBUG, only_message=False, save_log_file=True, send_warning_log=False):
    _logger = logging.getLogger(name)

    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(message)s")
    if only_message is False:
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] [%(filename)s:%(lineno)s] >> %(message)s")

    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)

    if save_log_file:
        if not os.path.exists("logs"):
            os.makedirs("logs")

        if filename is None:
            filename = os.path.join(".", "logs", "default.log")
        else:
            filename = os.path.join(".", "logs", Path(filename).stem + ".log")

        file_handler = handlers.RotatingFileHandler(filename, maxBytes=(
            1024 * 1024 * 10), backupCount=10, encoding="UTF-8")
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)

    if send_warning_log:
        email_handler = handlers.SMTPHandler(("lgekrhqmh01.lge.com", 25), "iddx@lge.com",
                                             "iddx-task@lge.com", "[WARNING][COMMON_UTIL] log alert!")
        email_handler.setFormatter(formatter)
        email_handler.setLevel(logging.WARNING)
        _logger.addHandler(email_handler)

    _logger.setLevel(level)
    return _logger


def upsert_target_index(_logger, e_search, all_hits, index_name):
    _logger.info("upsert_target_index: doc_size=%s" % len(all_hits))
    for num, doc in enumerate(all_hits):
        body = {"query": {"ids": {"values": doc["_id"]}}}
        res = e_search.search(index=index_name, body=body)
        target_hits = res["hits"]["hits"]
        if len(target_hits) > 0:
            target_doc = target_hits[0]
            if doc["_source"]["updated"] == target_doc["_source"]["updated"]:
                continue

        n_doc = doc["_source"]
        n_doc["description_all"] = ""
        try:
            res = e_search.index(index=index_name, id=doc["_id"], body=n_doc)
            _logger.info("upsert_target_index: num=%s/%s, res=%s" % (num + 1, len(all_hits), res))
        except Exception as ex:
            _logger.warning(ex.args)
            continue


def cp_jira_from_dee(_logger, query, target_index):
    _logger.error("cp_jira_from_dee DO NOT USE!!!!: " + target_index)
    return


def handle_save(_logger, all_hits, index_name, e_search, f_name):
    _logger.info("handle_save START : index_name=%s, doc size=%s" % (index_name, len(all_hits)))
    for num, doc in enumerate(all_hits):
        if ((num + 1) % 100 == 0 and num != 0) or num == len(all_hits) - 1:
            _logger.info("INDEX=%s, %s/%s UPDATED" % (index_name, num + 1, len(all_hits)))

        new_doc = doc["_source"]
        f_name(new_doc)
        try:
            e_search.index(index=index_name, id=doc["_id"], body=new_doc)
        except Exception as ex:
            _logger.info("handle_save Error:" + ex.args)
            continue

# index_name을 업데이트해줄 때마다 에러여부와 완료 시각을 로깅하는 함수


def log_index(_logger, index_name, server_name, if_error, complete_datetime):
    _logger.info("log_index START : index_name={}, server_name={}, if_error={}, compelete_datetime={}".format(
        index_name, server_name, if_error, complete_datetime))
    try:
        e_search = None
        ret_val, e_search = connect_es(e_search)
        if ret_val is False:
            _logger.info("log_index Error: Failed to connect Elasticsearch")
            return
        make_es_index(e_search, LOG_INDEX_NAME)
        doc = {
            "server": server_name,
            "if_error": if_error,
            "complete_datetime": complete_datetime
        }
        query = {"match_all": {}}
        res = e_search.search(index=LOG_INDEX_NAME, size=1, query=query)
        hits = res["hits"]["hits"]
        if len(hits) > 0:
            ret_val = e_search.update(index=LOG_INDEX_NAME, id=index_name, doc=doc)
            _logger.debug("Update ES Data: result={}".format(ret_val))
        else:
            e_search.index(index=index_name, document=doc)

    except Exception as ex:
        _logger.info("log_index Error: {}".format(ex.args))


def multiprocess_error(err_value):
    logger.warning(f"multiprocess_error: value={err_value}")


def process_index(_logger, index_name, f_name, custom_body=None, multi_process=False):
    _logger.info("process_index START : index_name=%s, multi_process=%s" % (index_name, multi_process))
    try:
        # e_search = Elasticsearch([IddxConfigs.IDDX_ELASTICSEARCH], timeout=7200)
        # es_logger.setLevel(logging.WARNING)
        e_search = connect_es(None)
    except Exception as ex:
        _logger.info("Failed to connect Elasticsearch: es=%s" % ex.args)
        return

    if custom_body:
        body = custom_body
    else:
        body = {"query": {"match_all": {}}}

    search_size = 9000
    pool = None
    if multi_process:
        search_size = 800
        pool = ThreadPool(processes=10)

    res = e_search.search(index=index_name, body=body, size=search_size, scroll="5m")
    all_hits = res["hits"]["hits"]
    fetched = len(all_hits)
    scroll_ids = []
    if fetched > 0:
        sid = res["_scroll_id"]
        scroll_ids.append(sid)
        if multi_process:
            pool.apply_async(handle_save, (_logger, all_hits, index_name,
                             e_search, f_name), error_callback=multiprocess_error)
            time.sleep(10)
        else:
            handle_save(_logger, all_hits, index_name, e_search, f_name)
        while fetched > 0:
            res = e_search.scroll(scroll_id=sid, scroll="5m")
            all_hits = res["hits"]["hits"]
            fetched = len(all_hits)
            sid = res["_scroll_id"]
            scroll_ids.append(sid)
            if fetched > 0:
                if multi_process:
                    pool.apply_async(handle_save, (_logger, all_hits, index_name,
                                     e_search, f_name), error_callback=multiprocess_error)
                    time.sleep(10)
                else:
                    handle_save(_logger, all_hits, index_name, e_search, f_name)

    if multi_process:
        pool.close()
        pool.join()

    if len(scroll_ids) > 0:
        e_search.clear_scroll(scroll_id=scroll_ids)
    e_search.transport.close()
    logger.info(f"process_index END: {index_name}")


def save_es_index_to_excel(index_name, output_path, filename, cols, query=None):
    def get_personinfo(field_name):
        df_person = pd.DataFrame.from_dict(pd.Series.to_dict(df_temp[field_name]))
        df_person = df_person.T.filter(["org4", "org5", "name"])
        df_person.rename(columns={"org4": field_name + "_org4", "org5": field_name +
                         "_org5", "name": field_name + "_name"}, inplace=True)

        return df_person, df_person.columns.values.tolist()

    try:
        # e_search = Elasticsearch([IddxConfigs.IDDX_ELASTICSEARCH], timeout=7200)
        # es_logger.setLevel(logging.WARNING)
        e_search = connect_es(None)

    except Exception as ex:
        logger.info(f"Failed to connect Elasticsearch: es={ex}")
        return

    if query is None:
        body = {"query": {"match_all": {}}}
    else:
        body = {"query": query}

    df_total = pd.DataFrame()

    scroll_ids = []
    res = e_search.search(index=index_name, body=body, size=IddxConfigs.ES_SEARCH_SIZE, scroll="5m")
    all_hits = res["hits"]["hits"]
    fetched = len(all_hits)
    if fetched > 0:
        sid = res["_scroll_id"]
        scroll_ids.append(sid)
        df_temp = pd.DataFrame.from_dict([document["_source"] for document in all_hits])
        for field_name in ["assignee_userinfo", "creator_userinfo"]:
            if {field_name}.issubset(cols):
                df_person, person_cols = get_personinfo(field_name)
                df_temp = pd.concat([df_temp, df_person], axis=1)
                cols.extend(person_cols)
                cols.remove(field_name)
        df_temp = df_temp.filter(cols, axis=1)
        df_total = df_total.append(df_temp)
        while fetched > 0:
            res = e_search.scroll(scroll_id=sid, scroll="5m")
            all_hits = res["hits"]["hits"]
            fetched = len(all_hits)
            sid = res["_scroll_id"]
            scroll_ids.append(sid)
            if fetched > 0:
                df_temp = pd.DataFrame.from_dict([document["_source"] for document in all_hits])
                for field_name in ["assignee_userinfo", "creator_userinfo"]:
                    if {field_name}.issubset(cols):
                        df_person, person_cols = get_personinfo(field_name)
                        df_temp = pd.concat([df_temp, df_person], axis=1)
                df_temp = df_temp.filter(cols, axis=1)
                df_total = df_total.append(df_temp)

    df_total = df_total.applymap(lambda x: ", ".join(x) if isinstance(x, list) and len(x) > 0 else x)
    if {"created"}.issubset(df_total.columns):
        df_total = df_total.sort_values(by="created")
    save_data_to_excel(df_total, output_path, filename)

    if len(scroll_ids) > 0:
        e_search.clear_scroll(scroll_id=scroll_ids)
    e_search.transport.close()


def get_es_index_data(index_name, cols, query=None):
    try:
        # e_search = Elasticsearch([IddxConfigs.IDDX_ELASTICSEARCH], timeout=7200)
        # es_logger.setLevel(logging.WARNING)
        ret, e_search = connect_es(None)

    except Exception as ex:
        logger.info(f"Failed to connect Elasticsearch: es={ex}")
        return

    if query is None:
        body = {"query": {"match_all": {}}}
    else:
        body = {"query": query}
    # elif query is 1:
    #     body = {"query": {
    #             "bool": {
    #             "must": [],
    #             "filter": [
    #                 {
    #                 "match_all": {}
    #                 },
    #                 {
    #                 "range": {
    #                     "first_date": {
    #                     "gte": "2019-12-31T15:30:00.000Z",
    #                     "lte": "2021-12-31T14:30:00.000Z",
    #                     "format": "strict_date_optional_time"
    #                     }
    #                 }
    #                 }
    #             ],
    #             "should": [],
    #             "must_not": []
    #             }
    #         }}
    # else:
    #     body = {"query": {
    #             "bool": {
    #             "must": [],
    #             "filter": [
    #                 {
    #                 "match_all": {}
    #                 },
    #                 {
    #                 "range": {
    #                     "first_date": {
    #                     "gte": "2021-12-30T15:30:00.000Z",
    #                     "lte": "2023-02-02T08:50:32.664Z",
    #                     "format": "strict_date_optional_time"
    #                     }
    #                 }
    #                 }
    #             ],
    #             "should": [],
    #             "must_not": []
    #             }
    #         }}

    df_total = pd.DataFrame()

    scroll_ids = []
    res = e_search.search(index=index_name, body=body, size=IddxConfigs.ES_SEARCH_SIZE, scroll="5m")
    all_hits = res["hits"]["hits"]
    fetched = len(all_hits)
    if fetched > 0:
        sid = res["_scroll_id"]
        scroll_ids.append(sid)
        df_temp = pd.DataFrame.from_dict([document["_source"] for document in all_hits])
        df_temp = df_temp.filter(cols, axis=1)
        # df_total = df_total.append(df_temp) // append : deprecated
        df_total = pd.concat([df_total, df_temp], ignore_index=True)
        while fetched > 0:
            res = e_search.scroll(scroll_id=sid, scroll="5m")
            all_hits = res["hits"]["hits"]
            fetched = len(all_hits)
            sid = res["_scroll_id"]
            scroll_ids.append(sid)
            if fetched > 0:
                df_temp = pd.DataFrame.from_dict([document["_source"] for document in all_hits])

    df_total = df_total.applymap(lambda x: ", ".join(x) if isinstance(x, list) and len(x) > 0 else x)
    if {"created"}.issubset(df_total.columns):
        df_total = df_total.sort_values(by="created")
    print("df_total\n", df_total)

    if len(scroll_ids) > 0:
        e_search.clear_scroll(body={"scroll_id": scroll_ids})
    e_search.transport.close()
    return df_total


def connect_es(e_search=None, timeout=6000):
    ret_val = True
    if e_search is None or not e_search.ping():
        try:
            e_search = Elasticsearch([IddxConfigs.IDDX_ELASTICSEARCH], timeout=timeout,
                                     max_retries=10, retry_on_timeout=True)
            es_logger.setLevel(logging.WARNING)
        except Exception as ex:
            logger.error(ex.args)
            e_search = None
            ret_val = False
    return ret_val, e_search


def save_documents_to_es_bulk_with_id(e_search, docs, index_name, _id=None):
    if e_search is None or not e_search.ping():
        return
    try:
        if isinstance(_id, list):
            actions = []
            for doc in docs:
                new_id = ""
                for i in _id:  # make _id
                    new_id += doc[i] + "_"
                actions.append({"_index": index_name, "_source": doc, "_id": new_id})
        elif isinstance(_id, str):
            actions = [{"_index": index_name, "_source": doc, "_id": doc[_id]} for doc in docs]
        else:
            actions = [{"_index": index_name, "_source": doc} for doc in docs]
        logger.debug(f"upload start : {len(docs)}")
        for success, info in helpers.parallel_bulk(e_search, actions):
            if not success:
                logger.error(f"Failed to upsert document: {info}")
        logger.debug("upload done")
    except Exception as ex:
        logger.warning(ex)
    finally:
        disconnect_es(e_search)
    return


def disconnect_es(e_search, scroll_ids=None, no_logs=False):
    if e_search is not None:
        if not no_logs:
            print("ElasticSearch Connection Closed!!!")
        try:
            if scroll_ids is not None and len(scroll_ids) > 0:
                if not no_logs:
                    print("ElasticSearch Clear Scroll")
                e_search.clear_scroll(scroll_id=scroll_ids)
        except Exception as ex:
            print(ex.args)
        finally:
            e_search.transport.close()
            e_search = None
    return e_search


def get_region_country(region_country):
    if isinstance(region_country, list):
        if len(region_country) == 2:
            return region_country[0], region_country[1]
        elif len(region_country) == 1:
            return region_country[0], "None"
        else:
            return "None", "None"

    region_country = region_country.strip()
    region = "None"
    country = "None"
    if region_country.find(",") != -1:
        region_country = region_country.split(",")
        region = region_country[0].strip()
        country = region_country[1].strip() if len(region_country) > 1 else "None"
    else:
        region = region_country

    if region == "Common":
        region = "Global"
        country = "Global"
    elif region == "Unknown":
        region = "None"
        country = "None"
    elif region in ["Korea", "Japan", "China"]:
        country = region
        region = "Asia"
    elif country in [
        "North America",
        "Europe",
        "Asia",
        "MEA",
        "CIS",
        "South America",
        "Global",
        "Central Asia",
        "Central and South America",
        "Middle East Asia",
        "Global",
    ]:
        region, country = country, region

    cr_dict = {"Dubai": "MEA", "Brazil": "South America", "Israel": "Central Asia", "Chile": "South America"}
    if region.title() in cr_dict.keys():
        country = region
        region = cr_dict[region.title()]

    return region, country


def get_df_dup_rows(df, col_name):
    dup = df.duplicated([col_name], keep=False)
    df_dup = pd.concat([df, dup], axis=1)
    df_dup.rename(columns={0: "duplicated"}, inplace=True)
    return df_dup[df_dup["duplicated"] == True]


def send_msg_teams_channel(msg, channel_name, title=None, url=None, color=None):
    if msg == "" or channel_name == "":
        return False
    teams_message = pymsteams.connectorcard(channel_name)
    teams_message.text(msg)
    if color:
        teams_message.color(color)
    if title:
        teams_message.title(title)
    if url:
        teams_message.addLinkButton("Link to check", url)
    try:
        teams_message.send()
    except Exception as ex:
        logger.error(ex.args)
