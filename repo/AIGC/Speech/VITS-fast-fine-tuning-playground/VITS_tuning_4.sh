#@markdown ##STEP 3.5 


#@markdown 运行该单元格会生成划分好训练/测试集的最终标注，以及配置文件  

#@markdown Running this block will generate final annotations for training & validation, as well as config file.

#@markdown 选择是否加入辅助训练数据：/ Choose whether to add auxiliary data: 
ADD_AUXILIARY = True #@param {type:"boolean"}
#@markdown 辅助训练数据是从预训练的大数据集抽样得到的，作用在于防止模型在标注不准确的数据上形成错误映射。

#@markdown Auxiliary data is to prevent overfitting when the audio samples are small or with low quality. 

#@markdown 以下情况请勾选：  

#@markdown 总样本少于100条/样本包含角色只有1人/样本质量一般或较差/样本来自爬取的视频  

#@markdown 以下情况可以不勾选：  

#@markdown 总样本量很大/样本质量很高/希望加速训练/只有二次元角色

#@markdown 样本仅包含单说话人会导致报错，请勾选ADD_AUXILIARY或加入几个dummy speaker绕过去  

#@markdown Feeding voice samples containing single speaker will result in error. Please select ADD_AUXILIARY or add several dummy speakers to bypass.

# assert(not (ADD_AUXILIARY and PRETRAINED_MODEL = "CJE")), "add auxiliary data is available only available for CJE model"
if ADD_AUXILIARY:
  python preprocess_v2.py --add_auxiliary_data True --languages "{PRETRAINED_MODEL}"
else:
  python preprocess_v2.py --languages "{PRETRAINED_MODEL}"

  #@markdown #STEP 4 (>=20 min)
#@markdown 开始微调模型，在40轮训练后会自动结束。
#@markdown 训练时长取决于你录入/上传的音频总数。

#@markdown 根据声线和样本质量的不同，所需的训练epochs数也不同。但是一般建议设置为40 epochs，  

#@markdown Model fine-tuning ends after 40 epochs. 
#@markdown Total time cost depends on the number of voices you recorded/uploaded.   

#@markdown Best epoch number varies depending on different uploaded voices / sample quality. Normally, 40 epochs is suggested.

#@markdown You can also preview synthezied audio in Tensorboard, it's OK to shut down training manually if you find the quality is satisfying.
Maximum_epochs = "40" #@param [20, 30, 40, 50, 60]
python finetune_speaker_v2.py -m "./OUTPUT_MODEL" --max_epochs "{Maximum_epochs}" --drop_speaker_embed True

#@markdown ### 微调完成后，在这里尝试效果。
#@markdown ### Try out TTS & VC quality here after fine-tuning is finished.
cp ./configs/modified_finetune_speaker.json ./finetune_speaker.json
python VC_inference.py --model_dir ./OUTPUT_MODEL/G_latest.pth