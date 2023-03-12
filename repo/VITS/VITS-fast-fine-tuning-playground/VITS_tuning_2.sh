#@title STEP 1.5 选择预训练模型
#@markdown ###STEP 1.5 选择预训练模型  
#@markdown ###Choose pretrained model to start  
#@markdown CJE为中日英三语模型，CJ为中日双语模型  

cd VITS-fast-fine-tuning
#@markdown CJE for Chinese, Japanese & English model，CJ for Chinese & Japanese model
PRETRAINED_MODEL = "C" #@param ["CJE","CJ"]
if PRETRAINED_MODEL == "CJ":
  wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/D_0-p.pth -O ./pretrained_models/D_0.pth
  wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/G_0-p.pth -O ./pretrained_models/G_0.pth
  wget https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/config.json -O ./configs/finetune_speaker.json
elif PRETRAINED_MODEL == "CJE":
  wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/D_trilingual.pth -O ./pretrained_models/D_0.pth
  wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth -O ./pretrained_models/G_0.pth
  wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/configs/uma_trilingual.json -O ./configs/finetune_speaker.json
elif PRETRAINED_MODEL == "C": # Bad generalizability to other voices
  wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-bb/D_0.pth -O ./pretrained_models/D_0.pth
  wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-bb/G_0.pth -O ./pretrained_models/G_0.pth
  wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-bb/config.json -O ./configs/finetune_speaker.json