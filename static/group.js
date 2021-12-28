// toggleDisabled disables the post button if the textarea is empty. Group page.
function toggleDisabled() {
  const button = document.querySelector(".post-btn");
  const input = document.querySelector("textarea");

  if (input.value === "") {
    button.disabled = true;
    button.classList.add("btn-disabled");
  } else {
    button.disabled = false;
    button.classList.remove("btn-disabled");
  }
}

toggleDisabled();
document.querySelector("textarea").addEventListener("keyup", toggleDisabled);

// removeSongFromPostCreation removes a song from the post creation form (jQuery). Group page.
$trackImg = $("#selected-track-img");
$trackImg.on("click", function () {
  $("selected-track-img").hide();
});

$albumImgDiv = $("#feed-post-creation-spotify");
$albumImgDiv.on("click", removeAlbumImg);

function removeAlbumImg() {
  $trackImg.hide();
}

// scroll to bottom of group page
window.onload = () => {
  const groupDiv = document.querySelector(".group-feed");
  groupDiv.scrollTop = groupDiv.scrollHeight;
};
