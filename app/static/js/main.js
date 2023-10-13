$(document).ready(function () {
  function loader() {
    $("#videoFeed").on("load", function () {
      $(".loading-spinner").hide();
    });
    $(".loading-spinner").show();
  }

  loader();
});

function startTalking() {
  document.getElementById("transcription").textContent = "Listening...";
  fetch("/start_listening", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.transcription) {
        document.getElementById("transcription").textContent =
          "You said: " + data.transcription;
      } else {
        document.getElementById("transcription").textContent =
          "Error: " + data.error;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("transcription").textContent =
        "An error occurred.";
    });
}
