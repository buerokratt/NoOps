FROM eclipse-temurin:17-jdk AS build
WORKDIR /workspace/app

COPY gradlew .
COPY gradlew.bat .
COPY gradle gradle
COPY build.gradle .
COPY src src
COPY .env .env
COPY scripts scripts
COPY DSL DSL

RUN chmod 754 ./gradlew
RUN ./gradlew -Pprod clean bootJar
RUN mkdir -p build/libs && (cd build/libs; jar -xf *.jar)

FROM eclipse-temurin:17-jdk
VOLUME /build/tmp

ARG DEPENDENCY=/workspace/app/build/libs
COPY --from=build ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY --from=build ${DEPENDENCY}/META-INF /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes /app
RUN mkdir -p /DSL
COPY scripts /app/scripts/
COPY constants.ini /app/constants.ini
RUN chmod a+x /app/scripts/*

ENV application.config-path=/DSL

COPY .env /app/.env
RUN echo BUILDTIME=`date +%s` >> /app/.env

# Install Python 3, venv, curl, git, nano, helm and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    git \
    nano \
    apt-transport-https \
    ca-certificates \
    && apt-get clean

# Download and install kubectl
RUN curl -LO "https://dl.k8s.io/release/v1.27.4/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl

# Install Helm directly from GitHub
RUN curl -fsSL https://get.helm.sh/helm-v3.9.4-linux-amd64.tar.gz -o helm.tar.gz \
    && tar -zxvf helm.tar.gz \
    && mv linux-amd64/helm /usr/local/bin/helm \
    && rm -rf helm.tar.gz linux-amd64

# Create and activate virtual environment
RUN python3 -m venv /app/python_virtual_env
ENV PATH="/app/python_virtual_env/bin:$PATH"

# Copy requirements and install them in virtual environment
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN useradd cronmanager
RUN chown -R cronmanager:cronmanager /app
RUN chown -R cronmanager:cronmanager /DSL
USER cronmanager

EXPOSE 9010

ENTRYPOINT ["java","-cp","app:app/lib/*","ee.buerokratt.cronmanager.CronManagerApplication"]