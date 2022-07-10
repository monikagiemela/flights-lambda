FROM public.ecr.aws/lambda/python@sha256:7dc57014be6dbf28f4d1f269194878a298ee55505a7b800b4b6041dccd753ce3 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1002910%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:7dc57014be6dbf28f4d1f269194878a298ee55505a7b800b4b6041dccd753ce3
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y
RUN pip install selenium
RUN pip install beautifulsoup4
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/
COPY lambda_function.py ./
COPY AtlMco.py ./
COPY BaseCall.py ./
COPY DfwOrd.py ./
COPY LaxJfk.py ./
COPY LgaOrd.py ./
ADD EmailSender.py ./
COPY params.py ./
CMD [ "lambda_function.lambda_handler" ]