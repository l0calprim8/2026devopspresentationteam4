function addMore() {
    const container = document.getElementById("images");
    const div = document.createElement("div");
    div.innerHTML = '<input type="file" name="images" accept="image/*" required>';
    container.appendChild(div);
  }
  