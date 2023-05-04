###STEP 2.1 上传短音频
### Short audio upload

cp {ZIP_PATH} ./custom_character_voice/custom_character_voice.zip
unzip ./custom_character_voice/custom_character_voice.zip -d ./custom_character_voice/

### STEP 2.2 上传长音频
### Long audio upload

#@markdown Upload option 2: If you have mounted Google drive, you can load your files from Google drive directly. Put all the long audios under one folder, and fill in the path to your folder below:
AUDIO_FOLDER_PATH = "../drive/MyDrive/long_audios/"  #@param {type:"string"}
cp {AUDIO_FOLDER_PATH}/* ./raw_audio/

#@markdown Upload option 2: If you have mounted Google drive, you can load your files from Google drive directly. Put all the videos under one folder, and fill in the path to your folder below:
VIDEO_FOLDER_PATH = "../drive/MyDrive/videos/"  #@param {type:"string"}
cp {VIDEO_FOLDER_PATH}/* ./video_data/


#@markdown 运行该单元格会对所有上传的数据进行自动去背景音&标注。 
#@markdown 由于需要调用Whisper和Demucs，运行时间可能较长。  

#@markdown Running this codeblock will perform automatic vocal seperation & annotation. 
#@markdown Since this step uses Whisper & Demucs, it may take a while to complete.
# 将所有视频（无论是上传的还是下载的，且必须是.mp4格式）抽取音频
python video2audio.py
# 将所有音频（无论是上传的还是从视频抽取的，必须是.wav格式）去噪
python denoise_audio.py
# 分割并标注长音频
python long_audio_transcribe.py --languages "{PRETRAINED_MODEL}" --whisper_size large
# 标注短音频
python short_audio_transcribe.py --languages "{PRETRAINED_MODEL}" --whisper_size large