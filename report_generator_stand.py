# -- coding: utf-8 --
import os
import argparse
import collections
from bokeh.plotting import figure, output_file, show
from bokeh.io import save
from bokeh.layouts import gridplot, column
from bokeh.models import ColumnDataSource, HoverTool, Range1d, BasicTickFormatter, Legend
from rtc_log_parser import rtc_log_parser

import sys
import re

def get_device(log_path):
    try:
        device_info = open(log_path, 'r', encoding='ISO-8859-1')
        line = device_info.read()
        device = re.findall(r'device info.+?(\w+)/', line)

        device = ''.join(device)
        return device
    except Exception as e:
        print(e)
        device = ''
        return device


def get_version(log_path):
    try:
        version_info = open(log_path, encoding='gbk')
        line = version_info.read()
        version = re.findall(r'SDK ver (.+?) build', line)
        version = ''.join(version)
        return version
    except Exception as e:
        print(e)
        version = ''
        return version

'''class report_generator_stand_alone:
    def __init__(self, abs_log_path):
        super().__init__()
        self.__img_width = 1280
        self.__img_height = 200
        self.__img_x_factor = 1.2
        self.__img_y_factor = 1.5
        if not os.path.isfile(abs_log_path):
            print('=== Error : Log file {} not exist, Exit ...',format(abs_log_path))
            exit()
        self.__log_parser = rtc_log_parser(abs_log_path)
        base_name = os.path.basename(abs_log_path)
        print('=== base_name : ', base_name)
        output_dir = abs_log_path.split(base_name)[0]
        print('=== output_dir : ', output_dir)
        file_name_without_ext = os.path.splitext(base_name)[0]
        print('=== file_name_without_ext : ', file_name_without_ext)
        self.__output_file_name = output_dir + file_name_without_ext + '_stand_alone.html'
        print('=== __output_file_name : ', self.__output_file_name)

    def draw(self):
        source_video_send_kbps = ColumnDataSource(
            data = dict(
                video_send_target_kbps_ts = [ts - self.__log_parser.call_join_channel_ts for ts in list(self.__log_parser.video_send_target_kbps.keys())],
                video_send_target_kbps = list(self.__log_parser.video_send_target_kbps.values()),

                video_send_kbps_ts = [ts - self.__log_parser.call_join_channel_ts for ts in list(self.__log_parser.video_send_kbps.keys())],
                video_send_kbps = list(self.__log_parser.video_send_kbps.values()),
            )
        )
        source_encoded_kbps = ColumnDataSource(
            data = dict(
                video_encoded_kbps_ts = [ts - self.__log_parser.call_join_channel_ts for ts in list(self.__log_parser.video_encoded_kbps.keys())],
                video_encoded_kbps = list(self.__log_parser.video_encoded_kbps.values()),
            )
        )

        hover_video_kbps = HoverTool(
            tooltips = [
                ("Target", "@video_send_target_kbps_ts ms : @video_send_target_kbps"),
                ("Send", "@video_send_kbps_ts ms : @video_send_kbps"),
            ]
        )

        ### Video send Kbps
        p_video_kbps = figure(plot_width = self.__img_width, plot_height = self.__img_height, y_axis_label = 'Kbps')
        legend_list = []
        p_video_kbps.left[0].formatter.use_scientific = False
        p_video_kbps.below[0].formatter.use_scientific = False
        y_max = self.__img_y_factor * max([
            max(list(self.__log_parser.video_send_target_kbps.values())) if len(list(self.__log_parser.video_send_target_kbps.values())) > 0 else 1,
            max(list(self.__log_parser.video_send_kbps.values())) if len(list(self.__log_parser.video_send_kbps.values())) > 0 else 1
        ])

        p_video_kbps.y_range = Range1d(0 - y_max / 10, y_max)
        line_target_kbps = p_video_kbps.line(x = 'video_send_target_kbps_ts', y = 'video_send_target_kbps', source = source_video_send_kbps, color = 'green', line_width = 1)
        legend_list.append(('Target Kbps', [line_target_kbps]))
        line_send_kbps = p_video_kbps.line(x = 'video_send_kbps_ts', y = 'video_send_kbps', source = source_video_send_kbps, color = 'red', line_width = 1)
        legend_list.append(('Send kbps', [line_send_kbps]))

        legend_video_kbps = Legend(items = list(legend_list), location = 'top_left')
        p_video_kbps.add_layout( legend_video_kbps, 'right')
        p_video_kbps.add_tools(hover_video_kbps)

        # Set description
        p_video_kbps.title.text = 'Video send avg bitrate : {}kbps'.format(self.__log_parser.video_send_avg_kbps)
        p_video_kbps.title.align = 'left'
        p_video_kbps.title.text_color = "red"
        p_video_kbps.title.text_font_size = "16px"
        # p_video_kbps.title.background_fill_color = "#aaaaee"


        output_file(self.__output_file_name)
        save(
            obj = gridplot(
                children = [
                    p_video_kbps, 
                    #p_fps, 
                    #p_qp, 
                    #p_fec, 
                    #p_rex, 
                    #p_audio_kbps,
                    #p_freeze, 
                    #p_video_jitter, 
                    #p_audio_jitter, 
                ], 
                ncols = 1
            ), 
            filename = self.__output_file_name, 
            title = 'report_uid_{}'.format(self.__log_parser.uid)
        )'''

if __name__ == '__main__':
    print(len(sys.argv))
    parser = argparse.ArgumentParser()
    if len(sys.argv) >= 5 :
        parser.add_argument('-i', '--name', help = 'Abs log file path')
        parser.add_argument('-i3', '--name2', help='Abs log file path')
    if len(sys.argv) >= 9 :
        parser.add_argument('-i2', '--name1', help = 'Abs log file path')
        parser.add_argument('-i4', '--name3', help = 'Abs log file path')

    args = parser.parse_args()
    if len(sys.argv) >= 5:
        if args.name:
            name = args.name
        if args.name2:
            name2 = args.name2
    if len(sys.argv) >= 9:
        if args.name1:
            name1 = args.name1
        if args.name3:
            name3 = args.name3


    if len(sys.argv) >= 5:
        log_parser = rtc_log_parser(name)
        log_parser2 = rtc_log_parser(name2)
        if len(sys.argv) >= 9:
            log_parser1 = rtc_log_parser(name1)
            log_parser3 = rtc_log_parser(name3)
    else:
        parser.print_help()
        exit()

    #worker = report_generator_stand_alone(name)
    #worker.__log_parser.video_encoded_kbps.values()
   # worker = report_generator_stand_alone(name,name1)
    #worker.draw()


    if len(sys.argv) == 9:

        source_video_send_kbps = ColumnDataSource(

            data = dict(
                video_send_kbps_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_kbps.keys())],
                video_send_kbps = list(log_parser.video_send_kbps.values()),

                video_send_kbps_ts1 = [ts - log_parser1.call_join_channel_ts for ts in list(log_parser1.video_send_kbps.keys())],
                video_send_kbps1 = list(log_parser1.video_send_kbps.values()),

                video_send_target_kbps_ts=[ts - log_parser.call_join_channel_ts for ts in
                                           list(log_parser.video_send_target_kbps.keys())],
                video_send_target_kbps=list(log_parser.video_send_target_kbps.values()),

                video_send_target_kbps_ts1=[ts - log_parser1.call_join_channel_ts for ts in
                                           list(log_parser1.video_send_target_kbps.keys())],
                video_send_target_kbps1=list(log_parser1.video_send_target_kbps.values()),
            )
        )

        source_video_send_fps = ColumnDataSource(
            data = dict(
                video_send_fps_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_fps.keys())],
                video_send_fps = list(log_parser.video_send_fps.values()),

                video_send_fps_ts1=[ts - log_parser1.call_join_channel_ts for ts in list(log_parser1.video_send_fps.keys())],
                video_send_fps1=list(log_parser1.video_send_fps.values()),
            )
        )

        source_send_qp = ColumnDataSource(
            data = dict(
                video_send_qp_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_qp.keys())],
                video_send_qp = list(log_parser.video_send_qp.values()),

                video_send_qp_ts1=[ts - log_parser1.call_join_channel_ts for ts in list(log_parser1.video_send_qp.keys())],
                video_send_qp1=list(log_parser1.video_send_qp.values()),
            )
        )



        source_errors = ColumnDataSource(
            data = dict(
                errors_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.errors.keys())],
                errors_value = [-5 for ts in list(log_parser.errors.keys())],
                errors_desc = list(log_parser.errors.values()),

                errors_ts1=[ts - log_parser1.call_join_channel_ts for ts in list(log_parser1.errors.keys())],
                errors_value1=[-5 for ts in list(log_parser1.errors.keys())],
                errors_desc1=list(log_parser1.errors.values()),
            )
        )

        source_resolution_change = ColumnDataSource(
            data = dict(
                resolution_change_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.resolution_change.keys())],
                resolution_change_value = [-10 for ts in list(log_parser.resolution_change.keys())],
                resolution_change_desc = list(log_parser.resolution_change.values()),

                resolution_change_ts1=[ts - log_parser1.call_join_channel_ts for ts in
                                      list(log_parser1.resolution_change.keys())],
                resolution_change_value1=[-10 for ts in list(log_parser1.resolution_change.keys())],
                resolution_change_desc1=list(log_parser1.resolution_change.values()),
            )
        )
    if len(sys.argv) == 5:
        source_video_send_kbps = ColumnDataSource(

            data=dict(
                video_send_kbps_ts=[ts - log_parser.call_join_channel_ts for ts in
                                    list(log_parser.video_send_kbps.keys())],
                video_send_kbps=list(log_parser.video_send_kbps.values()),

                video_send_target_kbps_ts=[ts - log_parser.call_join_channel_ts for ts in
                                           list(log_parser.video_send_target_kbps.keys())],
                video_send_target_kbps=list(log_parser.video_send_target_kbps.values()),
            )
        )

        source_video_send_fps = ColumnDataSource(
            data = dict(
                video_send_fps_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_fps.keys())],
                video_send_fps = list(log_parser.video_send_fps.values()),
            )
        )

        source_send_qp = ColumnDataSource(
            data = dict(
                video_send_qp_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_qp.keys())],
                video_send_qp = list(log_parser.video_send_qp.values()),
            )
        )


        source_errors = ColumnDataSource(
            data = dict(
                errors_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.errors.keys())],
                errors_value = [-5 for ts in list(log_parser.errors.keys())],
                errors_desc = list(log_parser.errors.values()),
            )
        )
        source_resolution_change = ColumnDataSource(
            data = dict(
                resolution_change_ts = [ts - log_parser.call_join_channel_ts for ts in list(log_parser.resolution_change.keys())],
                resolution_change_value = [-10 for ts in list(log_parser.resolution_change.keys())],
                resolution_change_desc = list(log_parser.resolution_change.values()),
            )
        )

    source_recv_freeze_300ms_dict_a = collections.OrderedDict()
    source_recv_freeze_600ms_dict_a = collections.OrderedDict()
    recv_freeze_300ms_max_value_a = 0
    recv_freeze_600ms_max_value_a = 0
    recv_fps_max_value = 0

    source_recv_freeze_300ms_dict_b = collections.OrderedDict()
    source_recv_freeze_600ms_dict_b = collections.OrderedDict()
    recv_freeze_300ms_max_value_b = 0
    recv_freeze_600ms_max_value_b = 0
    recv_fps_max_value1 = 0

    if len(sys.argv) >= 5:

        for uid_, recv_data_ in log_parser2.recv_data.items():
            max_value = max(list(recv_data_.video_recv_freeze_300ms.values())) if len(
                list(recv_data_.video_recv_freeze_300ms.values())) > 0 else 1
            recv_freeze_300ms_max_value_a = max(max_value, recv_freeze_300ms_max_value_a)


            source_recv_freeze_300ms_dict_a[uid_] = ColumnDataSource(
                data=dict(
                    video_recv_freeze_300ms_ts_a=[ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_kbps.keys())],
                    video_recv_freeze_300ms_a=list(recv_data_.video_recv_freeze_300ms.values()),

                )
            )

            max_value = max(list(recv_data_.video_recv_freeze_600ms.values())) if len(
                list(recv_data_.video_recv_freeze_600ms.values())) > 0 else 1
            recv_freeze_600ms_max_value_a = max(max_value, recv_freeze_600ms_max_value_a)
            source_recv_freeze_600ms_dict_a[uid_] = ColumnDataSource(
                data=dict(
                    video_recv_freeze_600ms_ts_a=[ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_kbps.keys())],
                    video_recv_freeze_600ms_a=list(recv_data_.video_recv_freeze_600ms.values()),

                )
            )



        if len(sys.argv) == 9 :
            for uid_, recv_data_ in log_parser3.recv_data.items():
                max_value = max(list(recv_data_.video_recv_freeze_300ms.values())) if len(
                    list(recv_data_.video_recv_freeze_300ms.values())) > 0 else 1
                recv_freeze_300ms_max_value_b = max(max_value, recv_freeze_300ms_max_value_b)

                source_recv_freeze_300ms_dict_b[uid_] = ColumnDataSource(
                    data=dict(
                        video_recv_freeze_300ms_ts_b=[ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_kbps.keys())],
                        video_recv_freeze_300ms_b=list(recv_data_.video_recv_freeze_300ms.values()),

                    )
                )

                max_value = max(list(recv_data_.video_recv_freeze_600ms.values())) if len(
                    list(recv_data_.video_recv_freeze_600ms.values())) > 0 else 1
                recv_freeze_600ms_max_value_b = max(max_value, recv_freeze_600ms_max_value_b)
                source_recv_freeze_600ms_dict_b[uid_] = ColumnDataSource(
                    data=dict(
                        video_recv_freeze_600ms_ts_b=[ts - log_parser.call_join_channel_ts for ts in list(log_parser.video_send_kbps.keys())],
                        video_recv_freeze_600ms_b=list(recv_data_.video_recv_freeze_600ms.values()),

                    )
                )



    hover_video_kbps = HoverTool(
        tooltips = [
            ("Target_A", "@video_send_target_kbps_ts ms : @video_send_target_kbps"),
            ("Send_A", "@video_send_kbps_ts ms : @video_send_kbps"),
            ("Target_B", "@video_send_target_kbps_ts ms : @video_send_target_kbps1"),
            ("Send_B", "@video_send_kbps_ts ms : @video_send_kbps1"),
        ]
    )

    hover_fps = HoverTool(
        tooltips=[
            ("FPS_A", "@video_send_fps_ts ms : @video_send_fps"),
            ("FPS_B", "@video_send_fps_ts ms : @video_send_fps1"),
        ]
    )

    hover_qp = HoverTool(
        tooltips=[
            ("QP_A", "@video_send_qp_ts ms : @video_send_qp"),
            ("Error_A", "@errors_ts ms : @errors_desc"),
            ("Res change_A", "@resolution_change_ts ms : @resolution_change_desc"),

            ("QP_B", "@video_send_qp_ts ms : @video_send_qp1"),
            ("Error_B", "@errors_ts ms : @errors_desc1"),
            ("Res change_B", "@resolution_change_ts ms : @resolution_change_desc1"),
        ]
    )

    ### Video send Kbps
    p_video_kbps = figure(plot_width = 1280, plot_height = 200, y_axis_label = 'Kbps')
    legend_list = []
    p_video_kbps.left[0].formatter.use_scientific = False
    p_video_kbps.below[0].formatter.use_scientific = False
    if len(sys.argv) == 9:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_target_kbps.values())) if len(list(log_parser.video_send_target_kbps.values())) > 0 else 1,
            max(list(log_parser.video_send_kbps.values())) if len(list(log_parser.video_send_kbps.values())) > 0 else 1,
            max(list(log_parser1.video_send_target_kbps.values())) if len(list(log_parser1.video_send_target_kbps.values())) > 0 else 1,
            max(list(log_parser1.video_send_kbps.values())) if len(list(log_parser1.video_send_kbps.values())) > 0 else 1,
        ])
    if len(sys.argv) == 5:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_target_kbps.values())) if len(list(log_parser.video_send_target_kbps.values())) > 0 else 1,
            max(list(log_parser.video_send_kbps.values())) if len(list(log_parser.video_send_kbps.values())) > 0 else 1,

        ])
    p_video_kbps.y_range = Range1d(0 - y_max / 10, y_max)
    # send_kbps a
    line_send_kbps = p_video_kbps.line(x = 'video_send_kbps_ts', y = 'video_send_kbps', source = source_video_send_kbps, color = 'red', line_width = 1)
    legend_list.append(('{} Send kbp_A ({})'.format(get_version(name),get_device(name)), [line_send_kbps]))
    line_target_kbps = p_video_kbps.line(x='video_send_target_kbps_ts', y='video_send_target_kbps',
                                         source=source_video_send_kbps, color='green', line_width=1)
    legend_list.append(('{} Target Kbps_A ({})'.format(get_version(name),get_device(name)), [line_target_kbps]))
    # send_kbps b
    if len(sys.argv) == 9:
        line_send_kbps1 = p_video_kbps.line(x = 'video_send_kbps_ts1', y = 'video_send_kbps1', source = source_video_send_kbps, color = 'blue', line_width = 1)
        legend_list.append(('{} Send kbps_B ({})'.format(get_version(name1),get_device(name1)), [line_send_kbps1]))

        line_target_kbps1 = p_video_kbps.line(x='video_send_target_kbps_ts1', y='video_send_target_kbps1',
                                             source=source_video_send_kbps, color='orange', line_width=1)
        legend_list.append(('{} Target Kbps_B ({})'.format(get_version(name1),get_device(name1)), [line_target_kbps1]))

    legend_video_kbps = Legend(items = list(legend_list), location = 'top_left')
    p_video_kbps.add_layout( legend_video_kbps, 'right')
    p_video_kbps.add_tools(hover_video_kbps)
    # Set description
    if len(sys.argv) == 9:
        p_video_kbps.title.text = 'Video send avg bitrate A: {}kbps   Video send avg bitrate B: {}kbps'.format(log_parser.video_send_avg_kbps,log_parser1.video_send_avg_kbps)
    if len(sys.argv) == 5:
        p_video_kbps.title.text = 'Video send avg bitrate :{}kbps'.format(
            log_parser.video_send_avg_kbps)
    p_video_kbps.title.align = 'left'
    p_video_kbps.title.text_color = "red"
    p_video_kbps.title.text_font_size = "16px"
    # p_video_kbps.title.background_fill_color = "#aaaaee"

    ### Video recv freeze 300
    p_freeze_300 = figure(plot_width=1280, plot_height=200, y_axis_label='ms')
    legend_list = []
    p_freeze_300.left[0].formatter.use_scientific = False
    p_freeze_300.below[0].formatter.use_scientific = False
    y_max = 1.5 * 2000
    p_freeze_300.y_range = Range1d(0 - y_max / 10, y_max)

    for remote_sn, remote_source in source_recv_freeze_300ms_dict_a.items():
        line_freeze_300ms_a = p_freeze_300.line(x='video_recv_freeze_300ms_ts_a', y='video_recv_freeze_300ms_a',
                                          source=remote_source, color='red', line_width=1)

        legend_list.append(['{} Freeze 300ms Recv_A ({})'.format(get_version(name2),get_device(name2)), [line_freeze_300ms_a]])
    if len(sys.argv) == 9:
        for remote_sn, remote_source in source_recv_freeze_300ms_dict_b.items():
            line_freeze_300ms_b = p_freeze_300.line(x='video_recv_freeze_300ms_ts_b', y='video_recv_freeze_300ms_b',
                                              source=remote_source, color='blue', line_width=1)
            legend_list.append(['{} Freeze 300ms Recv_B ({})'.format(get_version(name3),get_device(name3)), [line_freeze_300ms_b]])



    legend_freeze = Legend(items=list(legend_list), location='top_left')
    p_freeze_300.add_layout(legend_freeze, 'right')
    # Set description
    if len(sys.argv) ==9:
        p_freeze_300.title.text = 'Video recv freeze_300ms_A: {} Video recv freeze_300ms_B: {}'.format(log_parser2.video_recv_freeze_ratio_300ms,log_parser3.video_recv_freeze_ratio_300ms)
    if len(sys.argv) == 5:
        p_freeze_300.title.text = 'Video recv freeze_300ms_A: {}'.format(
            log_parser2.video_recv_freeze_ratio_300ms)
    p_freeze_300.title.align = 'left'
    p_freeze_300.title.text_color = "red"
    p_freeze_300.title.text_font_size = "16px"

    ### Video recv freeze 600
    p_freeze_600 = figure(plot_width=1280, plot_height=200, y_axis_label='ms')
    legend_list = []
    p_freeze_600.left[0].formatter.use_scientific = False
    p_freeze_600.below[0].formatter.use_scientific = False
    y_max = 1.5 * 2000
    p_freeze_600.y_range = Range1d(0 - y_max / 10, y_max)
    for remote_sn, remote_source in source_recv_freeze_600ms_dict_a.items():
        line_freeze_600ms_a = p_freeze_600.line(x='video_recv_freeze_600ms_ts_a', y='video_recv_freeze_600ms_a',
                                                source=remote_source, color='red', line_width=1)
        legend_list.append(['{} Freeze 600ms Recv_A ({})'.format(get_version(name2),get_device(name2)), [line_freeze_600ms_a]])
    if len(sys.argv) == 9:
        for remote_sn, remote_source in source_recv_freeze_600ms_dict_b.items():
            line_freeze_600ms_b = p_freeze_600.line(x='video_recv_freeze_600ms_ts_b', y='video_recv_freeze_600ms_b',
                                                    source=remote_source, color='blue', line_width=1)
            legend_list.append(['{} Freeze 600ms Recv_B ({})'.format(get_version(name3),get_device(name3)), [line_freeze_600ms_b]])

    legend_freeze = Legend(items=list(legend_list), location='top_left')
    p_freeze_600.add_layout(legend_freeze, 'right')
    # Set description
    if len(sys.argv) == 9:
        p_freeze_600.title.text = 'Video recv freeze_600ms_A: {} Video recv freeze_600ms_B: {}'.format(
            log_parser2.video_recv_freeze_ratio_600ms, log_parser3.video_recv_freeze_ratio_600ms)
    if len(sys.argv) == 5:
        p_freeze_600.title.text = 'Video recv freeze_600ms_A: {}'.format(
            log_parser2.video_recv_freeze_ratio_600ms)
    p_freeze_600.title.align = 'left'
    p_freeze_600.title.text_color = "red"
    p_freeze_600.title.text_font_size = "16px"

    ### Video send FPS
    p_fps = figure(plot_width=1280, plot_height=200, y_axis_label='fps')
    legend_list = []
    p_fps.left[0].formatter.use_scientific = False
    p_fps.below[0].formatter.use_scientific = False

    if len(sys.argv) == 9:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_fps.values())) if len(list(log_parser.video_send_fps.values())) > 0 else 1,
            max(list(log_parser1.video_send_fps.values())) if len(list(log_parser1.video_send_fps.values())) > 0 else 1,
        ])

    if len(sys.argv) == 5:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_fps.values())) if len(
                list(log_parser.video_send_fps.values())) > 0 else 1,
        ])


    p_fps.y_range = Range1d(0 - y_max / 10, y_max)
    line_fps = p_fps.line(x='video_send_fps_ts', y='video_send_fps', source= source_video_send_fps, color='red',
                          line_width=1)
    legend_list.append(['{} Send FPS_A ({})'.format(get_version(name),get_device(name)), [line_fps]])
    if len(sys.argv) >= 9:
        line_fps1 = p_fps.line(x='video_send_fps_ts1', y='video_send_fps1', source= source_video_send_fps, color='blue',
                              line_width=1)
        legend_list.append(['{} Send FPS_B ({})'.format(get_version(name1),get_device(name1)), [line_fps1]])


    legend_fps = Legend(items=list(legend_list), location='top_left')
    p_fps.add_layout(legend_fps, 'right')
    p_fps.add_tools(hover_fps)
    # Set description
    if len(sys.argv) ==5:
        p_fps.title.text = 'Video send avg FPS_A : {}fps'.format(
            log_parser.video_send_avg_fps)
    if len(sys.argv) ==9:
        p_fps.title.text = 'Video send avg FPS_A : {}fps  Video send avg FPS_B : {}fps'.format(log_parser.video_send_avg_fps,log_parser1.video_send_avg_fps)
    p_fps.title.align = 'left'
    p_fps.title.text_color = "red"
    p_fps.title.text_font_size = "16px"

    ### Video send QP
    p_qp = figure(plot_width=1280, plot_height=200, y_axis_label='QP')
    legend_list = []
    p_qp.left[0].formatter.use_scientific = False
    p_qp.below[0].formatter.use_scientific = False

    if len(sys.argv) == 5:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_qp.values())) if len(
                list(log_parser.video_send_qp.values())) > 0 else 1
        ])

    if len(sys.argv) == 9:
        y_max = 1.5 * max([
            max(list(log_parser.video_send_qp.values())) if len(list(log_parser.video_send_qp.values())) > 0 else 1,
            max(list(log_parser1.video_send_qp.values())) if len(list(log_parser1.video_send_qp.values())) > 0 else 1
        ])
    p_qp.y_range = Range1d(-15, y_max)

    line_qp = p_qp.line(x='video_send_qp_ts', y='video_send_qp', source=source_send_qp, color='orange', line_width=1)
    legend_list.append(['{} QP_A ({})'.format(get_version(name),get_device(name)), [line_qp]])

    circle_errors = p_qp.circle(x='errors_ts', y='errors_value', source=source_errors, color='red', line_width=1)
    legend_list.append(['{} Error_A'.format(get_version(name)), [circle_errors]])

    circle_resolution_change = p_qp.circle(x='resolution_change_ts', y='resolution_change_value',
                                           source=source_resolution_change, color='blue', line_width=1)
    legend_list.append(['{} Resolution change_A'.format(get_version(name)), [circle_resolution_change]])


    if len(sys.argv) == 9:
        line_qp1 = p_qp.line(x='video_send_qp_ts1', y='video_send_qp1', source=source_send_qp, color='green',
                            line_width=1)
        legend_list.append(['{} QP_B ({})'.format(get_version(name1),get_device(name1)), [line_qp1]])

        circle_errors1 = p_qp.circle(x='errors_ts1', y='errors_value1', source=source_errors, color='red', line_width=1)
        legend_list.append(['{} Error_B'.format(get_version(name1)), [circle_errors1]])

        circle_resolution_change1 = p_qp.circle(x='resolution_change_ts1', y='resolution_change_value1',
                                               source=source_resolution_change, color='blue', line_width=1)
        legend_list.append(['{} Resolution change_B'.format(get_version(name1)), [circle_resolution_change1]])

    legend_qp = Legend(items=list(legend_list), location='top_left')
    p_qp.add_layout(legend_qp, 'right')
    p_qp.add_tools(hover_qp)
    # Set description
    if len(sys.argv) == 5:
        p_qp.title.text = 'Video send avg QP_A : {} '.format(log_parser.video_send_avg_qp)
    if len(sys.argv) == 9:
        p_qp.title.text = 'Video send avg QP_A : {}  Video send avg QP_B : {}'.format(log_parser.video_send_avg_qp,log_parser1.video_send_avg_qp)
    p_qp.title.align = 'left'
    p_qp.title.text_color = "red"
    p_qp.title.text_font_size = "16px"
    # p_qp.title.background_fill_color = "#aaaaee"

    base_name = os.path.basename(name)
    print('=== base_name : ', base_name)
    output_dir = name.split(base_name)[0]
    print('=== output_dir : ', output_dir)
    file_name_without_ext = os.path.splitext(base_name)[0]
    print('=== file_name_without_ext : ', file_name_without_ext)
    output_file_name = output_dir + file_name_without_ext + '_stand_alone.html'
    print('=== __output_file_name : ',output_file_name)
    output_file(output_file_name)
    save(
        obj = gridplot(
            children = [
                p_video_kbps,
                p_fps,
                p_freeze_300,
                p_freeze_600,
                p_qp,
                #p_fec, 
                #p_rex, 
                #p_audio_kbps,
                #p_freeze, 
                #p_video_jitter, 
                #p_audio_jitter, 
            ], 
            ncols = 1
        ), 
        filename = output_file_name, 
        title = 'report_uid_{}'.format(log_parser.uid)
    )