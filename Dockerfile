FROM nvcr.io/nvidia/pytorch:21.06-py3

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir jupyter

RUN git clone https://github.com/Banayaki/rcan-it && cd rcan-it && pip install -e .

EXPOSE 8080
WORKDIR /workspace/rcan-it