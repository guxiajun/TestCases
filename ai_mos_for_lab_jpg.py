import os
import sys
import cv2
import time
import math
import argparse
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from collections import OrderedDict
from ffmpy import FFmpeg



class IMOS(nn.Module):
    """Neural IMage Assessment model by Google"""
    def __init__(self, base_model,in_features = 12800, num_classes = 10, size = 7):
        super(IMOS, self).__init__()
        self.features = base_model.features
        self.gpool = nn.AdaptiveMaxPool2d(output_size = (size, size))
        self.classifier = nn.Sequential(
            nn.Dropout(p = 0.35),
            nn.Conv2d(in_channels = 512, out_channels = 256, kernel_size = 3, padding = 1),
            nn.ReLU(),
            nn.Conv2d(in_channels = 256, out_channels = 128, kernel_size = 3, padding = 1),
            nn.ReLU(),
            nn.Conv2d(in_channels = 128, out_channels = 64,  kernel_size = 3, padding = 1),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(in_features = 64 * size * size, out_features = 512),
            nn.ReLU(),
            nn.Linear(in_features = 512, out_features = 101), # MOS normalized to 0 - 100, the original is 1 - 5
            nn.Softmax()
        )
        self.index = torch.arange(0, 101.0)


    def forward(self, x):
        out = self.features(x)
        out = self.gpool(out)
        clss = self.classifier(out)
        clss = clss.view(clss.size(0), -1)
        dist = self.fc(clss)
        y = torch.mul(dist, self.index)
        mos = torch.sum(y,dim = 1)
        return dist, mos

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    #argparse.ArgumentParser.add_argument()
    parse.add_argument("-i", "--input",  help = "record file")
    #parse.add
    data = vars(parse.parse_args())
    path = data["input"]


    file_extension = os.path.splitext(path)[1]

    # if (file_extension == '.mov') or (file_extension == '.MOV') \
    #         or (file_extension == '.mp4') or (file_extension == '.MP4') \
    #         or (file_extension == '.flv') or (file_extension == '.FLV') \
    #         or (file_extension == '.m4v') or (file_extension == '.jpg'):

        #use cpu or gpu
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # load model
    base_model = models.vgg19(pretrained = False)
    model = IMOS(base_model)

    state_dice = torch.load('epoch-234.pkl', map_location = device)
    new_dict = OrderedDict()
    for k, v in state_dice.items():
        if 'module.' in k:
         name = k.replace('module.', '')
        else:
            name = k
        new_dict[name] = v

    model.load_state_dict(new_dict)
    model = model.to(device)
    model.index = model.index.to(device)
    model.eval()

    mos = []

    for parent, dirnames, filenames in os.walk(path, followlinks=True):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.jpg':
                PATH = path + '/' + filename

                cap = cv2.VideoCapture(PATH)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                if height % 2 != 0 or width % 2 != 0:
                    height = int(height - height % 2)
                    width = int(width - width % 2)
                    img = cv2.imread(PATH)
                    cropped = img[0:height, 0:width]
                    new_path =  path +'/'+ os.path.splitext(filename)[0]+'_cut'+'.jpg'
                    cv2.imwrite(new_path, cropped)
                    os.remove(PATH)
                    print(new_path)

    time.sleep(2)
    final_score = []
    for parent, dirnames, filenames in os.walk(path, followlinks=True):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.jpg':
                file_path = path + "/" +filename

                cap = cv2.VideoCapture(file_path)
                FPS = cap.get(cv2.CAP_PROP_FPS)
                FPS = math.ceil(FPS)
                FRAME_COUNT= cap.get(cv2.CAP_PROP_FRAME_COUNT)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


                SEC = int(FRAME_COUNT/FPS)
                scaler = 1
                if width >= height and width >= 640:
                    scaler = int(width/640)
                if height > width and height >= 640:
                    scaler = int(height/640)
                scaler = scaler*scaler

                print('FPS', FPS, 'FPS_COUNT', FRAME_COUNT, 'SEC', SEC, 'WIDTH', width, 'HIGHT', height)
                start = time.time()
                Min = 0
                Sec = 0.0
                for i in range(1):
                    if i >= 60:
                        Min = SEC/60
                        Sec = i%60
                    for j in range(1):
                        snaptime = snaptime = '00:' + str(int(Min)) + ':' + str(int(i))+'.'+str(100*j)
                        print(snaptime)
                        yuv = os.path.split(file_path)[0] + '.yuv'
                        #print(yuv)
                        param = ' -i '+ file_path + ' -y'
                        ff = FFmpeg(outputs={yuv: param})
                        print(ff.cmd)
                        ff.run()

                        if yuv == None:
                            print("please set the input yuv!")
                            sys.exit(0)

                        # calculate the frames
                        fp = open(yuv, 'rb')
                        # create the buffer
                        Y = np.zeros(shape = (height, width),           dtype = 'uint8', order = 'C')
                        U = np.zeros(shape = (height // 2, width // 2), dtype = 'uint8', order = 'C')
                        V = np.zeros(shape = (height // 2, width // 2), dtype = 'uint8', order = 'C')

                        # read the frame
                        for m in range(height):
                            for n in range(width):
                                Y[m, n] = ord(fp.read(1))

                        for m in range(height // 2):
                            for n in range(width // 2):
                                U[m, n] = ord(fp.read(1))

                        for m in range(height // 2):
                            for n in range(width // 2):
                                V[m, n] = ord(fp.read(1))

                        # reshape and convert to BGR format
                        image_yuv = np.concatenate((Y.reshape(-1), U.reshape(-1), V.reshape(-1)))
                        image_yuv = image_yuv.reshape((height * 3 // 2, width)).astype('uint8')
                        image_bgr = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR_IYUV)

                        # subsampling
                        #scaler = int(data["scaler"])
                        if scaler > 1:
                            image_bgr = cv2.resize(image_bgr, (image_bgr.shape[1] // scaler, image_bgr.shape[0] // scaler))
                            #cv2.imwrite(str(os.path.split(file_path)[0]) + snaptime  + '.bmp', image_bgr)

                        # predict the mos
                        image_tensor = transforms.ToTensor()(image_bgr)
                        image_tensor = image_tensor.unsqueeze(0)
                        image_tensor = image_tensor.to(device)
                        result = model(image_tensor)
                        value = result[1].data.item()
                        mos.append(round(value, 2))

                        print('processing frame %d and its mos is %f' % ((i + 1), value))

                    #cv2.imwrite('image_%d.jpg' % (i + 1), image_bgr)
                score = np.mean(mos)

                end = time.time()
                #print('it took about ' + str(end - start) + 's' +  ' to finish for ' + file_path + ' and its mos : ' + str(score))
                resultfile = os.path.split(file_path)[0] + '/result.txt'
                fileresult = open(resultfile, 'a+')
                #fileresult.write(str(mos)+'\n')
                # param = 'it took about ' + str(round((end - start),2)) + 's' +  ' to finish for ' + str(os.path.split(file_path)) + ' and its mos : ' + str(round(score,2))+'\n'
                param =  os.path.split(file_path)[1] + ' its mos : ' + str(round(score, 2)) + '\n'
                fileresult.write(param)
                final_score.append(round(score, 2))

    final_param = os.path.split(file_path)[0] + 'average_mos is :'+ str(np.mean(final_score)) + '\n' + 'time :' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n'
    fileresult.write(final_param)
    fileresult.closed
