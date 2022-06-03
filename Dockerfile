FROM trophime/magnettools:poetry

RUN sudo apt-get update \
    && sudo apt-get install -y libxft2 libglu1 \
    && pip install watchdog
