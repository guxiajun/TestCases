#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR + "/libpycmd.so"
print(path)


def needterms():
    return "2"
def categories():
    return "communication"
def shortDesc():
    return "(通信)进入频道，两个主播通信360P400K，无弱网一分钟限制带宽300K20%一分钟去除弱网一分钟，visualReport"
def detailDesc():
    return "(通信)A B设备一直在同一个频道内，设置设备的上行丢包策略，通过log计算播放侧的卡顿率"

def run():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "impairNet,0")
    lib.ExeCmdCallBack(1, "impairNet,0")

    #lib.ExeCmdCallBack(0, "YUV,globe.yuv,640,360,15,0")

    lib.ExeCmdCallBack(0, "setParameters,{\"rtc.log_filter\":32847}")
    lib.ExeCmdCallBack(1, "setParameters,{\"rtc.log_filter\":32847}")

    lib.ExeCmdCallBack(0, "setParameters,{\"rtc.log_size\":20000000}")
    lib.ExeCmdCallBack(1, "setParameters,{\"rtc.log_size\":20000000}")

    lib.ExeCmdCallBack(0, "setParameters,{\"che.video.LogcatVideoQoS\":1}")
    lib.ExeCmdCallBack(1, "setParameters,{\"che.video.LogcatVideoQoS\":1}")
    lib.ExeCmdCallBack(0, "setParameters,{\"rtc.channel_mode\":0}")

    #lib.ExeCmdCallBack(0, "setExternalVideoSource,true,false,true")
    lib.ExeCmdCallBack(0, "setChannelProfile,0")
    #lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "setVideoEncoderConfiguration,640,360,15,400,0")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1")
    Testchannelname = "Test" + str(random.random())
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil," + Testchannelname + ",nil,1")

    lib.ExeCmdCallBack(1, "setChannelProfile,0")
    #lib.ExeCmdCallBack(1, "setClientRole,1,nil")
    lib.ExeCmdCallBack(1, "setVideoEncoderConfiguration,640,360,15,400,0")
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil," + Testchannelname + ",nil,2")
    
    lib.ExeCmdCallBack(0, "impairNet,0")
    lib.ExeCmdCallBack(0, "SLEEP,60")
    lib.ExeCmdCallBack(0, "impairNet,300 20")
    lib.ExeCmdCallBack(0, "SLEEP,60")
    lib.ExeCmdCallBack(0, "impairNet,0")
    lib.ExeCmdCallBack(0, "SLEEP,60")
    lib.ExeCmdCallBack(0, "impairNet,300 20")
    lib.ExeCmdCallBack(0, "SLEEP,60")
    lib.ExeCmdCallBack(0, "impairNet,0")
    lib.ExeCmdCallBack(0, "SLEEP,60")

    #lib.ExeCmdCallBack(0, "setExternalVideoSource,false,false,true")
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")

    lib.ExeCmdCallBack(0, "getFile")
    lib.ExeCmdCallBack(1, "getFile")

    lib.ExeCmdCallBack(1, "visualReport")
    lib.ExeCmdCallBack(0, "SLEEP,5")

    lib.ExeCmdCallBack(1, "DELAY")

    return "4"



