// script.js

document.addEventListener("DOMContentLoaded", function () {
    const h1 = document.getElementById("gesturePal");
  
    h1.innerHTML = h1.textContent.replace(/\S/g, "<span>$&</span>");
  
    const spans = h1.querySelectorAll("span");
  
    spans.forEach((span, index) => {
      span.style.display = "inline-block";
      span.style.fontFamily = "'h', sans-serif"; // Add this line
  
      if (index === 0 || index === 4) {
        // Tilt the first and fifth letters
        span.style.color = "#f80000";
        span.style.transform = "rotate(-10deg)";
      } else if (index === 1 || index === spans.length - 1) {
        span.style.color = "#ff0000";
        span.style.transform = "rotate(10deg)";
      }
  
      // Add animation for the letters
      span.style.transition = "transform 0.5s ease-in-out";
    });
  
    // Add hover effect for the entire text
    h1.addEventListener("mouseover", () => {
      h1.style.transform = "scale(0.8)";
    });
  
    h1.addEventListener("mouseout", () => {
      h1.style.transform = "scale(1)";
    });
  
    // Get the video element
    const video = document.getElementById("myVideo");
  
    // Set the playback speed to 0.85x
    video.playbackRate = 0.85;
  
    // Add event listener to pause the video on button hover
    const btn = document.querySelector(".btn");
    btn.addEventListener("mouseover", () => {
      video.pause();
    });
  
    btn.addEventListener("mouseout", () => {
      video.play();
    });
  
    // Add event listener to pause the video on anchor tag hover
    const anchor = document.querySelector("a");
    anchor.addEventListener("mouseover", () => {
      video.pause();
    });
  
    anchor.addEventListener("mouseout", () => {
      video.play();
    });
  });
  