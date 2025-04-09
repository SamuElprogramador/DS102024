FROM mageai/mageai:latest

ARG USER_CODE_PATH=/home/src/mage_etl_elt_class

# Instalar dependencias adicionales para la clase
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt
RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
