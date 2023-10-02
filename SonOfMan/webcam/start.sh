#docker run --name=webcam -rm -d --privileged -p 8080:8080 -p 8082:8082 -v /dev/video0:/dev/video0 romankspb/webcam
#docker run --name=webcam --net=host -rm -d --privileged -v /dev/video0:/dev/video0 ubuntu:latest
docker run --rm --privileged -p 8080:8080 -v /dev/video0:/dev/video0 -v $(pwd):/app webcam_feed:latest
