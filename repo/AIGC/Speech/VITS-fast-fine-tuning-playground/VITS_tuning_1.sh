#https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing#scrollTo=Z5G1jozPFd6p

sudo apt install cmake -y
git clone https://github.com/Plachtaa/VITS-fast-fine-tuning.git
pip install imageio==2.4.1
pip install --upgrade youtube-dl
pip install moviepy
cd VITS-fast-fine-tuning
pip install -r requirements.txt
pip install Cython
# build monotonic align
cd monotonic_align/
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
# download data for fine-tuning
wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
unzip sampled_audio4ft_v2.zip
# create necessary directories
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice