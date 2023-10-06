FROM tensorflow/tensorflow:latest-gpu

# Install Graphviz software
RUN apt-get update 
RUN apt-get install -y graphviz 
RUN apt-get install git -y
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*

# Install necessary Python libraries
RUN pip install pydot
RUN pip install opencv-python
RUN pip install git+https://github.com/julianfl0w/sinode

# Set the working directory
WORKDIR /app

CMD ["python", "resnet_visualize.py"]
