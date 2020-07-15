function clientSearchFunction() {
  let input = document.getElementById("client-search");
  let filter = input.value.toUpperCase();
  let ul = document.getElementById("clientUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function mnfactureSearchFunction() {
  let input = document.getElementById("mnfacture-search");
  let filter = input.value.toUpperCase();
  let ul = document.getElementById("mnfactureUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function productSearchFunction() {
  let input = document.getElementById("product-model-search");
  let filter = input.value.toUpperCase();
  let ul = document.getElementById("productModelUL");
  let li = ul.getElementsByTagName("li");
  let i, txtValue;

  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "block";
    } else {
      li[i].style.display = "none";
    }
  }
}

function similarWords() {
  const words = document.querySelectorAll(".similar-word");
  words.forEach((ele) => (ele.style.display = "none"));
}
similarWords();
