FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime

RUN apt update && apt install -y git

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir jupyter

RUN git clone https://github.com/Banayaki/rcan-it && cd rcan-it && pip install -e .

EXPOSE 8080
WORKDIR /workspace/rcan-it