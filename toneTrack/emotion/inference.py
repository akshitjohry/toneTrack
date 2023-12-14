
import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from Model import TIMNET_Model
import argparse
import librosa
import numpy as np
import json


parser = argparse.ArgumentParser()

parser.add_argument('--mode', type=str, default="test")
parser.add_argument('--model_path', type=str, default='./Models')
parser.add_argument('--result_path', type=str, default='./Results/')
parser.add_argument('--test_path', type=str, default='./10-fold_weights_best_1.hdf5')
parser.add_argument('--data', type=str, default='RAVDE')
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--beta1', type=float, default=0.93)
parser.add_argument('--beta2', type=float, default=0.98)
parser.add_argument('--batch_size', type=int, default=64)
parser.add_argument('--epoch', type=int, default=500)
parser.add_argument('--dropout', type=float, default=0.1)
parser.add_argument('--random_seed', type=int, default=40)
parser.add_argument('--activation', type=str, default='relu')
parser.add_argument('--filter_size', type=int, default=39)
parser.add_argument('--dilation_size', type=int, default=8)# If you want to train model on IEMOCAP, you should modify this parameter to 10 due to the long duration of speech signals.
parser.add_argument('--kernel_size', type=int, default=2)
parser.add_argument('--stack_size', type=int, default=1)
parser.add_argument('--split_fold', type=int, default=10)
parser.add_argument('--gpu', type=str, default='0')
parser.add_argument('--audio_path', type=str, default='./')

args = parser.parse_args()

    
os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True 
session = tf.compat.v1.Session(config=config)
print(f"###gpus:{gpus}")

# CLASS_LABELS_finetune = ("angry", "fear", "happy", "neutral","sad")
# CASIA_CLASS_LABELS = ("angry", "fear", "happy", "neutral", "sad", "surprise")#CASIA
# EMODB_CLASS_LABELS = ("angry", "boredom", "disgust", "fear", "happy", "neutral", "sad")#EMODB
# SAVEE_CLASS_LABELS = ("angry","disgust", "fear", "happy", "neutral", "sad", "surprise")#SAVEE
# RAVDE_CLASS_LABELS = ("angry", "calm", "disgust", "fear", "happy", "neutral","sad","surprise")#rav
# IEMOCAP_CLASS_LABELS = ("angry", "happy", "neutral", "sad")#iemocap
# EMOVO_CLASS_LABELS = ("angry", "disgust", "fear", "happy","neutral","sad","surprise")#emovo
# CLASS_LABELS_dict = {"CASIA": CASIA_CLASS_LABELS,
#                "EMODB": EMODB_CLASS_LABELS,
#                "EMOVO": EMOVO_CLASS_LABELS,
#                "IEMOCAP": IEMOCAP_CLASS_LABELS,
#                "RAVDE": RAVDE_CLASS_LABELS,
#                "SAVEE": SAVEE_CLASS_LABELS}
CLASS_LABELS_dict = {
    "RAVDE": ("angry", "calm", "disgust", "fear", "happy", "neutral","sad","surprise")
}

def extract_mfcc(audio_path, n_mfcc=13, n_fft=2048, hop_length=512, mean_signal_length=110000, embed_len=39):
    feature = None
    signal, fs = librosa.load(audio_path)# Default setting on sampling rate
    s_len = len(signal)
    if s_len < mean_signal_length:
        pad_len = mean_signal_length - s_len
        pad_rem = pad_len % 2
        pad_len //= 2
        signal = np.pad(signal, (pad_len, pad_len + pad_rem), 'constant', constant_values = 0)
    else:
        pad_len = s_len - mean_signal_length
        pad_len //= 2
        signal = signal[pad_len:pad_len + mean_signal_length]
    mfcc =  librosa.feature.mfcc(y=signal, sr=fs, n_mfcc=embed_len)
    feature = np.transpose(mfcc)
    return feature

mfccs = extract_mfcc(args.audio_path)
features = np.array([mfccs])


# data = np.load("./MFCC/"+args.data+".npy",allow_pickle=True).item()
# print(data["x"].shape)
# x_source = data["x"]
# y_source = data["y"]
CLASS_LABELS = CLASS_LABELS_dict[args.data]


model = TIMNET_Model(args=args, input_shape=features.shape[1:], class_label=CLASS_LABELS)
# x_feats, y_labels = model.test(x_source, y_source, path=args.test_path)# x_feats and y_labels are test datas for t-sne
pred = model.inference(features, path= args.test_path)
emotion = CLASS_LABELS[pred]
print(pred, emotion)
output = {'pred': int(pred), 'emotion':emotion, 'filename':args.audio_path}

# Serializing json
# json_object = json.dumps(output, indent=4)
filename = f"{args.audio_path.split('.')[0]}.json"
print(filename, output)
# Writing to sample.json
with open(filename, "w") as outfile:
    # outfile.write(json_object)
    json.dump(output, outfile)

