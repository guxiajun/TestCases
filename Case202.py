#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import time
import os
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR+"/libpycmd.so"
print(path)

def needterms():
    return "2"
def categories():
    return "broadcast"
def shortDesc():
    return "(外部源直播)进入频道，两个主播连麦360P800K,限制上行弱网500K+20%丢包，统计设备B侧的卡顿率和延时"
def detailDesc():
    return "(直播)A B设备一直在同一个频道内，设置设备的上行丢包策略，通过log计算播放侧的卡顿率"
def run():
    ll= ctypes.cdll.LoadLibrary
    lib = ll(path)
    lib.ExeCmdCallBack(0, "impairNet,0")
    lib.ExeCmdCallBack(1, "impairNet,0")

    lib.ExeCmdCallBack(0, "Readyuv,agora_720_1280_30.yuv,720,1280,30,0")

    lib.ExeCmdCallBack(0, "setParameters,{\"rtc.log_size\":20000000}")
    lib.ExeCmdCallBack(1, "setParameters,{\"rtc.log_size\":20000000}")

    lib.ExeCmdCallBack(0, "setParameters,{\"che.video.LogcatVideoQoS\":1}")
    lib.ExeCmdCallBack(1, "setParameters,{\"che.video.LogcatVideoQoS\":1}")

    lib.ExeCmdCallBack(0, "setExternalVideoSource,true,false,true")
    lib.ExeCmdCallBack(0, "setChannelProfile,1")
    lib.ExeCmdCallBack(0, "setClientRole,1,nil")
    lib.ExeCmdCallBack(0, "setVideoEncoderConfiguration,640,360,15,800,0")
    lib.ExeCmdCallBack(0, "enableVideo")
    lib.ExeCmdCallBack(0, "setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(0, "setupRemoteVideo,2,2,-1")
    Testchannelname = "Test"+str(random.random())
    lib.ExeCmdCallBack(0, "joinChannelByKey,nil,"+Testchannelname+",nil,1")
    
    lib.ExeCmdCallBack(1, "setChannelProfile,1")
    lib.ExeCmdCallBack(1, "setClientRole,1,nil")
    lib.ExeCmdCallBack(1, "setVideoEncoderConfiguration,640,360,15,800,0")
    lib.ExeCmdCallBack(1, "enableVideo")
    lib.ExeCmdCallBack(1, "setupLocalVideo,2,-1")
    lib.ExeCmdCallBack(1, "setupRemoteVideo,1,2,-1")
    lib.ExeCmdCallBack(1, "joinChannelByKey,nil,"+Testchannelname+",nil,2")
    time.sleep(10)
    lib.ExeCmdCallBack(0, "impairNet,500 20")

    lib.ExeCmdCallBack(0, "SLEEP,180")
    
    lib.ExeCmdCallBack(0, "setExternalVideoSource,false,false,true")
    lib.ExeCmdCallBack(0, "leaveChannel")
    lib.ExeCmdCallBack(1, "leaveChannel")
    lib.ExeCmdCallBack(0, "impairNet,0")

    lib.ExeCmdCallBack(0, "getFile")
    lib.ExeCmdCallBack(1, "getFile")

    lib.ExeCmdCallBack(1, "DELAY")
    
    return "4"