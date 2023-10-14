document.addEventListener("DOMContentLoaded", () => {
    const localVideo = document.getElementById('localVideo');
    const remoteVideo = document.getElementById('remoteVideo');

    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then((stream) => {
            localVideo.srcObject = stream;

            // Fetch ICE candidates from the server and create RTCPeerConnection
            return fetch('http://localhost:5000/get_ice_candidates');
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then((data) => {
            const configuration = {
                iceServers: Object.values(data).map((iceCandidate) => {
                    return {
                        urls: iceCandidate
                    };
                })
            };

            const pc = new RTCPeerConnection(configuration);

            pc.ontrack = (event) => {
                remoteVideo.srcObject = event.streams[0];
            };

            localVideo.srcObject.getTracks().forEach((track) => pc.addTrack(track, localVideo.srcObject));

            // Additional WebRTC logic here (like handling offer/answer, signaling, etc.)
            // Also includes ICE Candidate Logic
            setupWebRTCLogic(pc);

        })
        .catch((error) => console.error('Error:', error));


    // Send an offer to establish a WebRTC connection
    const createAndSendOffer = () => {
        pc.createOffer()
            .then((offer) => {
                pc.setLocalDescription(offer);
                // Send the offer to the remote peer through the signaling server
                signalingServer.sendOffer(offer);
            })
            .catch((error) => console.error('Error creating offer:', error));
    };

    // When an offer from a remote peer is received via the signaling server
    const handleReceivedOffer = (offer) => {
        pc.setRemoteDescription(new RTCSessionDescription(offer))
            .then(() => pc.createAnswer())
            .then((answer) => {
                pc.setLocalDescription(answer);
                // Send the answer back to the remote peer through the signaling server
                signalingServer.sendAnswer(answer);
            })
            .catch((error) => console.error('Error handling offer:', error));
    };

    // When an answer from a remote peer is received via the signaling server
    const handleReceivedAnswer = (answer) => {
        pc.setRemoteDescription(new RTCSessionDescription(answer))
            .catch((error) => console.error('Error handling answer:', error));
    };

    // When an ICE candidate is received from the remote peer via the signaling server
    const handleReceivedIceCandidate = (iceCandidate) => {
        pc.addIceCandidate(new RTCIceCandidate(iceCandidate))
            .catch((error) => console.error('Error adding received ice candidate:', error));
    };

    // Send local ICE candidate to the remote peer through the signaling server
    pc.onicecandidate = (event) => {
        if (event.candidate) {
            signalingServer.sendIceCandidate(event.candidate);
        }
    };

    // ... [Your additional logic, UI interaction, etc.]

    // Example usage assuming signaling server logic:
    // createAndSendOffer();
    // handleReceivedOffer(offerFromSignaling);
    // handleReceivedAnswer(answerFromSignaling);
    // handleReceivedIceCandidate(iceCandidateFromSignaling);

});
