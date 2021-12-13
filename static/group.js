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

document.querySelector("textarea").addEventListener("keypress", toggleDisabled);
