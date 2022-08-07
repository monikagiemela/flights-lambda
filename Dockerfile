FROM public.ecr.aws/lambda/python@sha256:bffbc925bcc08ee9395d8a460ab68a2e4848eab4bf75d9ab0bce53a77bdf446e as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1012728%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:bffbc925bcc08ee9395d8a460ab68a2e4848eab4bf75d9ab0bce53a77bdf446e
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

RUN pip install selenium
RUN pip install beautifulsoup4

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

COPY lambda_function.py ./
COPY  MyFlights.py ./
COPY BaseCall.py ./
ADD EmailSender.py ./
COPY params.py ./

CMD [ "lambda_function.lambda_handler" ]