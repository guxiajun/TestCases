import os
import re
import sys
import argparse
import collections

sys.path.append('../')

from lib.stats.stats import Stats

class rtc_log_parser:
    class recv_data_t:
        def __init__(self):
            self.video_recv_kbps = collections.OrderedDict()
            self.video_recv_fps = collections.OrderedDict()
            self.video_recv_freeze_300ms = collections.OrderedDict()
            self.video_recv_freeze_600ms = collections.OrderedDict()
            self.video_recv_jitter = collections.OrderedDict()
            self.video_recv_jitter_95 = collections.OrderedDict()
            self.video_recv_jitter_100 = collections.OrderedDict()
            self.video_recv_first_frame_ts = -1
            self.video_recv_total_frozen_time = -1
            self.audio_recv_jitter_95 = collections.OrderedDict()
            self.audio_recv_jitter_100 = collections.OrderedDict()
            self.audio_recv_frame_lossrate = collections.OrderedDict()
            self.audio_recv_network_transport_delay = collections.OrderedDict()
            self.audio_recv_jitterbuffer_delay = collections.OrderedDict()
            self.audio_recv_total_frozen_time = -1

            ### Calc & Avg
            self.video_recv_avg_kbps = -1
            self.video_recv_avg_fps = -1
            self.video_recv_avg_jitter = -1
            self.video_recv_avg_jitter_95 = -1
            self.video_recv_avg_jitter_100 = -1
            self.video_recv_freeze_ratio_300ms = -1
            self.video_recv_freeze_ratio_600ms = -1
            self.video_recv_first_frame_delay = -1
            self.audio_recv_avg_jitter_95 = -1
            self.audio_recv_avg_jitter_100 = -1
            self.video_recv_duration_ms = -1
            self.audio_recv_duration_ms = -1

    ## Patterns
    # __extra_info_pattern = re.compile(r'AGORA_SDK.+API call to join channel.+SDK ver(.+),.*device info(.*)')
    __call_join_channel_pattern = re.compile(r'^.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+API call to join channel.+SDK ver(.+),.*device info \'(.*)\'')
    __join_channel_success_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+join channel success.+cname \'(.+)\' uid (\d+) elapsed (\d+)')
    __first_video_packet_received_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+onTracerFirstRemoteVideo uid (\d+) codec (\d+) elapsed (\d+)')
    __first_video_frame_decoded_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+onRemoteFirstFrameDecoded user (\d+).+elapsed (\d+)')
    __first_video_frame_arrived_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+FIRST_FRAME_ARRIVED.+Remote stream \((\d+)\)')
    __send_pattern = re.compile(r'^.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+Sender Side.+Target Kbitrate = (\d+).*Highsend Kbitrate = (\d+).*Fps = (\d+).*QP = (\d+)')
    __send_pattern_old = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+Sender Side.+Bytes = (\d+).*Frames = (\d+).*QP = (\d+)')
    __video_delay_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+SetVideoMinimumDelay.+uid (\d+).*delay_ms (\d+)')
    __recv_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+Receiver Side.+UID = (\d+).+Bytes = (\d+).*Frames = (\d+)')

    __recv_freeze_600ms_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+).+FreezeTime = (\d+)')
    __recv_freeze_300ms_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+).+FreezeTime300 = (\d+)')

    __first_frame_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+onFirstVideoFrame remote.+elapsed (\d+)')
    __mtu_strategy_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+MTU.+Strategy.+max_payload_sent (\d+),.*lostLargePacket (\d+),.*lossSmall (.*),.*coverage_small (.*)\.')
    __pkt_num_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+SendGeneric.+pkt_num\((\d+)\),fec_pkt_num\((\d+)\)')
    __pkt_len_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+SendGeneric.+payload_length\((\d+)\)')
    __fec_kbps_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+video fec_kbps = (\d+)')
    __encode_kbps_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+encode_kbps = (\d+)')
    __rex_pkt_kbps_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+RexferController video rexf_kbps = (\d+).+audio rexf_kbps = (\d+)')
    __recv_fec_rex_kbps_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+video recv rexf_kbps = (\d+).*fec_kbps = (\d+)')
    __recv_video_jitter_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+uid=(\d+).+videoJitter95=(\d+).+videoJitter100=(\d+)')
    __recv_audio_jitter_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+uid=(\d+).+audioJitter95=(\d+).+audioJitter100=(\d+)')
    __recv_audio_frame_lossrate_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+uid=(\d+) audio frame lossrate=(\d+)')
    __recv_audio_stats_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+onRemoteAudioStats uid.+ (\d+) networkTransportDelay (\d+) jitterBufferDelay (\d+) .+ totalFrozenTime (\d+) frozenRate')
    __recv_video_stats_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+onRemoteVideoStats uid.+ (\d+) delay.+totalFrozenTime (\d+) frozenRate')
    __send_audio_bitrate_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+start duration:.+audio bitrate tx=(\d+)')
    __resolution_change_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+) .+MediaCodecVideoEncoder Reconfigure encoder due to frame resolution change (.+)')
    __error_pattern = re.compile(r'.*?: ERROR.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+).+; (.+)')
    __warn_pattern = re.compile(r'.*?: WARN.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+).+; (.+)')
    __parameter_pattern = re.compile(r'.+[ ]?(\d+):[ ]?(\d+):[ ]?(\d+):[ ]*(\d+).+\[rp\] (.+)')

    def __init__(self, log_file):
        self.__log_file = log_file
        print('=== parse : ', self.__log_file)
        self.sdk_version = ''
        self.sdk_build_time = ''
        self.dev_info = ''
        self.uid = -1
        self.channel_name = ''
        self.call_join_channel_ts = -1
        self.join_channel_success_ts = -1
        self.first_video_packet_received_ts = -1
        self.first_video_frame_decoded_ts = -1
        self.video_send_target_kbps = collections.OrderedDict()
        self.video_send_kbps = collections.OrderedDict()
        self.video_send_fps = collections.OrderedDict()
        self.video_send_qp = collections.OrderedDict()
        self.video_encoded_kbps = collections.OrderedDict()
        self.video_send_fec_kbps = collections.OrderedDict()
        self.video_send_rex_kbps = collections.OrderedDict()
        self.audio_send_kbps = collections.OrderedDict()
        self.audio_send_rex_kbps = collections.OrderedDict()
        self.resolution_change = collections.OrderedDict()
        self.parameters = collections.OrderedDict()
        self.warns = collections.OrderedDict()
        self.errors = collections.OrderedDict()
        self.recv_data = collections.OrderedDict()

        ### Calc & Avg
        self.video_send_avg_kbps = -1
        self.video_send_avg_rex_kbps = -1
        self.video_send_avg_fec_kbps = -1
        self.video_send_avg_fps = -1
        self.video_send_avg_qp = -1
        self.video_recv_total_kbps = -1
        self.audio_send_avg_kbps = -1
        self.audio_send_avg_rex_kbps = -1
        self.first_audio_frame_show_elapsed = -1
        self.first_video_frame_show_elapsed = -1
        self.join_channel_success_elapsed = -1

        #self.video_recv_freeze_ratio_300ms = -1
        #self.video_recv_freeze_ratio_600ms = -1


        self.parse()


    def parse_line(self, line_text):
        match = self.__send_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.video_send_target_kbps[ts] = int(match.groups()[4])
            self.video_send_kbps[ts] = int(match.groups()[5])
            self.video_send_fps[ts] = int(match.groups()[6])
            self.video_send_qp[ts] = int(match.groups()[7])
        else :
            match = self.__send_pattern_old.search(line_text)
            if match:
                ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
                self.video_send_kbps[ts] = int(int(match.groups()[4]) / 128)
                self.video_send_fps[ts] = int(match.groups()[5])
                self.video_send_qp[ts] = int(match.groups()[6])
        match = self.__recv_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()
            
            self.recv_data[uid].video_recv_kbps[ts] = int(int(match.groups()[5]) / 128)
            self.recv_data[uid].video_recv_fps[ts] = int(match.groups()[6])


            match = self.__recv_freeze_600ms_pattern.search(line_text)
            if match:
                self.recv_data[uid].video_recv_freeze_600ms[ts] = int(match.groups()[4])

            match = self.__recv_freeze_300ms_pattern.search(line_text)
            if match:
                self.recv_data[uid].video_recv_freeze_300ms[ts] = int(match.groups()[4])
      


        match = self.__recv_video_jitter_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()

            self.recv_data[uid].video_recv_jitter_95[ts] = int(match.groups()[5]) 
            self.recv_data[uid].video_recv_jitter_100[ts] = int(match.groups()[6]) 
        match = self.__recv_audio_jitter_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()
                
            if int(match.groups()[5]) > 0 and int(match.groups()[5]) < 60000:
                self.recv_data[uid].audio_recv_jitter_95[ts] = int(match.groups()[5]) 
                self.recv_data[uid].audio_recv_jitter_100[ts] = int(match.groups()[6]) 
        match = self.__recv_audio_frame_lossrate_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()

            self.recv_data[uid].audio_recv_frame_lossrate[ts] = int(match.groups()[5]) 
        match = self.__video_delay_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()

            self.recv_data[uid].video_recv_jitter[ts] = int(match.groups()[5]) 
        match = self.__fec_kbps_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.video_send_fec_kbps[ts] = int(match.groups()[4]) 
        match = self.__encode_kbps_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.video_encoded_kbps[ts] = int(match.groups()[4]) 
        match = self.__rex_pkt_kbps_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.video_send_rex_kbps[ts] = int(match.groups()[4]) 
            self.audio_send_rex_kbps[ts] = int(match.groups()[5]) 
        match = self.__send_audio_bitrate_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.audio_send_kbps[ts] = int(match.groups()[4])
        match = self.__recv_audio_stats_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()

            self.recv_data[uid].audio_recv_network_transport_delay[ts] = int(match.groups()[5]) 
            self.recv_data[uid].audio_recv_jitterbuffer_delay[ts] = int(match.groups()[6]) 
            self.recv_data[uid].audio_recv_total_frozen_time = int(match.groups()[7]) 
            # print('=== audio stats : ', int(match.groups()[5]), int(match.groups()[6]), int(match.groups()[7]))
        match = self.__recv_video_stats_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()

            self.recv_data[uid].video_recv_total_frozen_time = int(match.groups()[5]) 
            # print('=== video stats : ', int(match.groups()[5]) )
        # match = self.__call_join_channel_pattern.search(line_text)
        # if match:
        #     self.call_join_channel_ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
        match = self.__first_video_frame_arrived_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            uid = int(match.groups()[4])
            if uid == 0:
                return
            if uid not in self.recv_data:
                print('=== rtc log parser : Add remote uid {}'.format(uid))
                self.recv_data[uid] = rtc_log_parser.recv_data_t()
            self.recv_data[uid].video_recv_first_frame_ts = ts
        match = self.__parameter_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.parameters[ts] = match.groups()[4]
        match = self.__resolution_change_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.resolution_change[ts] = match.groups()[4]
        match = self.__error_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.errors[ts] = match.groups()[4]
        match = self.__warn_pattern.search(line_text)
        if match:
            ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
            self.warns[ts] = match.groups()[4]
        if self.call_join_channel_ts == -1:
            match = self.__call_join_channel_pattern.search(line_text)
            if match:
                self.call_join_channel_ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
                self.sdk_version = match.groups()[4]
                self.dev_info = match.groups()[5]
        if self.join_channel_success_ts == -1:
            match = self.__join_channel_success_pattern.search(line_text)
            if match:
                self.join_channel_success_ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
                self.channel_name = match.groups()[4]
                self.uid = int(match.groups()[5])
        if self.first_video_packet_received_ts == -1:
            match = self.__first_video_packet_received_pattern.search(line_text)
            if match:
                self.first_video_packet_received_ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])
        if self.first_video_frame_decoded_ts == -1:
            match = self.__first_video_frame_decoded_pattern.search(line_text)
            if match:
                self.first_video_frame_decoded_ts = int(match.groups()[0]) * 60 * 60 * 1000 + int(match.groups()[1]) * 60 *1000 + int(match.groups()[2]) *1000 + int(match.groups()[3])

    def parse(self):
        with open(self.__log_file, mode = 'r', errors = 'ignore') as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    break
                
                self.parse_line(line)
        
        self.analyse()
    
    def analyse(self):
        self.join_channel_success_elapsed = self.join_channel_success_ts - self.call_join_channel_ts
        self.first_audio_frame_show_elapsed = self.join_channel_success_elapsed + 65
        self.first_video_frame_show_elapsed = self.join_channel_success_elapsed + (self.first_video_frame_decoded_ts - self.first_video_packet_received_ts)
        self.video_send_avg_kbps = Stats.avg(list(self.video_send_kbps.values()))
        self.video_send_avg_rex_kbps = Stats.avg(list(self.video_send_rex_kbps.values()))
        self.video_send_avg_fec_kbps = Stats.avg(list(self.video_send_fec_kbps.values()))
        self.video_send_avg_fps = Stats.avg(list(self.video_send_fps.values()))
        self.video_send_avg_qp = Stats.avg(list(self.video_send_qp.values()))
        self.audio_send_avg_kbps = Stats.avg(list(self.audio_send_kbps.values()))
        self.audio_send_avg_rex_kbps = Stats.avg(list(self.audio_send_rex_kbps.values()))


        print('=== local data : ', 
        'video_send_avg_kbps: ', self.video_send_avg_kbps,
        'video_send_avg_rex_kbps: ', self.video_send_avg_rex_kbps,
        'video_send_avg_fec_kbps: ', self.video_send_avg_fec_kbps,
        'video_send_avg_fps: ', self.video_send_avg_fps,
        'video_send_avg_qp: ', self.video_send_avg_qp,
        'audio_send_avg_kbps: ', self.audio_send_avg_kbps,
        'audio_send_avg_rex_kbps: ', self.audio_send_avg_rex_kbps,

        )

        for uid_, remoter_data in self.recv_data.items():
            # print('=== uid : {}, self {}'.format(uid_, self.uid))
            if uid_ == 0:
                continue

            remoter_data.video_recv_avg_kbps = Stats.avg(list(remoter_data.video_recv_kbps.values()))
            remoter_data.video_recv_avg_fps = Stats.avg(list(remoter_data.video_recv_fps.values()))
            remoter_data.video_recv_avg_jitter = Stats.avg(list(remoter_data.video_recv_jitter.values()))
            remoter_data.video_recv_avg_jitter_95 = Stats.avg(list(remoter_data.video_recv_jitter_95.values()))
            remoter_data.video_recv_avg_jitter_100 = Stats.avg(list(remoter_data.video_recv_jitter_100.values()))

            if len(remoter_data.video_recv_freeze_300ms) > 0:
                remoter_data.video_recv_freeze_ratio_300ms = round(Stats.summation(list(remoter_data.video_recv_freeze_300ms.values())) * 100.0 / (list(remoter_data.video_recv_freeze_300ms.keys())[-1] - self.call_join_channel_ts), 2)

            if len(remoter_data.video_recv_freeze_600ms) > 0:
                remoter_data.video_recv_freeze_ratio_600ms = round(Stats.summation(list(remoter_data.video_recv_freeze_600ms.values())) * 100.0 / (list(remoter_data.video_recv_freeze_600ms.keys())[-1] - self.call_join_channel_ts), 2)
            remoter_data.video_recv_first_frame_delay = remoter_data.video_recv_first_frame_ts - self.call_join_channel_ts
            remoter_data.audio_recv_avg_jitter_95 = Stats.avg(list(remoter_data.audio_recv_jitter_95.values()))
            remoter_data.audio_recv_avg_jitter_100 = Stats.avg(list(remoter_data.audio_recv_jitter_100.values()))
            # remoter_data.audio_recv_duration_ms = max(list(remoter_data.audio_recv_jitter_95.keys())) - min(list(remoter_data.audio_recv_jitter_95.keys()))
            # remoter_data.video_recv_duration_ms = max(list(remoter_data.video_recv_kbps.keys())) - min(list(remoter_data.video_recv_kbps.keys()))
            remoter_data.video_recv_duration_ms = Stats.range(list(remoter_data.video_recv_kbps.keys()))
            print('=== video recv duration({}) : '.format(uid_), remoter_data.video_recv_duration_ms)

            self.video_recv_total_kbps += remoter_data.video_recv_avg_kbps
            self.video_recv_total_kbps = round(self.video_recv_total_kbps, 2)

            self.video_recv_freeze_ratio_300ms = remoter_data.video_recv_freeze_ratio_300ms
            self.video_recv_freeze_ratio_600ms = remoter_data.video_recv_freeze_ratio_600ms

            print('=== remoter data : ',
            'video_recv_avg_kbps ： ', remoter_data.video_recv_avg_kbps,
            'video_recv_avg_fps ： ', remoter_data.video_recv_avg_fps,
            'video_recv_avg_jitter ： ', remoter_data.video_recv_avg_jitter,
            'video_recv_avg_jitter_95 ： ', remoter_data.video_recv_avg_jitter_95,
            'video_recv_avg_jitter_100 ： ', remoter_data.video_recv_avg_jitter_100,
            'video_recv_freeze_ratio_300ms ： ', remoter_data.video_recv_freeze_ratio_300ms,
            'video_recv_freeze_ratio_600ms ： ', remoter_data.video_recv_freeze_ratio_600ms,
            'video_recv_first_frame_delay ： ', remoter_data.video_recv_first_frame_delay,
            'audio_recv_avg_jitter_95 ： ', remoter_data.audio_recv_avg_jitter_95,
            'audio_recv_avg_jitter_100 ： ', remoter_data.audio_recv_avg_jitter_100,
            )

    def dump(self):
        print('=== sdk version : ', self.sdk_version)
        print('=== dev info : ', self.dev_info)
        print('=== cname : ', self.channel_name)
        print('=== uid : ', self.uid)
        print('=== call to join channel ts : ', self.call_join_channel_ts)
        print('=== join channel success ts : ', self.join_channel_success_ts)
        print('=== join channel elapsed : ', self.join_channel_success_elapsed)
        print('=== first video packet ts : ', self.first_video_packet_received_ts)
        print('=== first video frame decoded ts : ', self.first_video_frame_decoded_ts)
        print('=== first video frame elapsed : ', self.first_video_frame_decoded_ts - self.first_video_packet_received_ts)

        print('=== First Audio frame show elapsed : ', self.first_audio_frame_show_elapsed)
        print('=== First Video frame show elapsed : ', self.first_video_frame_show_elapsed)

        # for ts,vsk in self.video_send_kbps.items():
        #     print(ts - self.call_join_channel_ts, vsk)
        # print('\nsend fps:')
        # for ts,vsf in self.video_send_fps.items():

        # print('\nsend kbps:')
        #     print(ts - self.call_join_channel_ts, vsf)
        # print('\nsend qp:')
        # for ts,vsq in self.video_send_qp.items():
        #     print(ts - self.call_join_channel_ts, vsq)

        # print('\n=== peer:')
        # for (_, item) in self.recv_data.items():
        #     print('\nrecv kbps:')
        #     for ts,vrk in item.video_recv_kbps.items():
        #         print(ts - self.call_join_channel_ts, vrk)

        #     print('\nrecv fps:')
        #     for ts,vrf in item.video_recv_fps.items():
        #         print(ts - self.call_join_channel_ts, vrf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--name', help = 'Log file path')
    args = parser.parse_args()

    if args.name:
        name = args.name
    else:
        parser.print_help()
        exit()

    worker = rtc_log_parser(name)
    worker.dump()

    