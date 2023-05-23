let liked = document.getElementById("liked-posts")
let written = document.getElementById("written-posts")

let likedText = document.getElementById("liked-text")
let writtenText = document.getElementById("written-text")

liked.style.display = "none";
writtenText.style.borderBottom = "2px solid black";

function showliked() {
  written.style.display = "none";
  liked.style.display = "flex";
  writtenText.style.borderBottom = "none";
  likedText.style.borderBottom = "2px solid black";
}
function showWritten() {
  liked.style.display = "none";
  written.style.display = "flex";
  likedText.style.borderBottom = "none";
  writtenText.style.borderBottom = "2px solid black";
}

