$("select").on("change", function (e) {
  let selectedAllValue = $("#selected_all").is(":checked");
  let selecteBoxValue = this.value;
  let url = "/weekly/" + selecteBoxValue + "/";
  if (selectedAllValue == true) {
    url = url + 1;
  } else {
    url = url + 2;
  }
  location.href = url;
});

$("#selected_all").on("change", function (e) {
  let checkedValue = $(this).prop("checked");
  let selecteBoxValue = $("#selected_id").val();
  let url = "/weekly/" + selecteBoxValue + "/";
  if (checkedValue == true) {
    url = url + 1;
  } else {
    url = url + 2;
  }
  location.href = url;
});
