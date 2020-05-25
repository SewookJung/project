$(document).ready(function () {
  const content = [
    '<div class="timePickerCanvas"><a href="#">NAC 제품소개서</a></div>',
    '<div class="timePickerClock timePickerHours"><a href="#">EDR 제품소개서</a></div>',
    '<div class="timePickerClock timePickerMinutes"><a href="#">GPI 제품소개서</a></div>',
  ].join("");

  $('[data-toggle="popover_presales"]').popover({
    trigger: "focus",
    html: true,
  });
});

$("#presales_popover").on("show.bs.popover", function () {
  console.log("test");
});

$("#progressing_popover").on("show.bs.popover", function () {
  console.log("test");
});

$("#examination_popover").on("show.bs.popover", function () {
  console.log("test");
});

$("#manafacture_popover").on("show.bs.popover", function () {
  console.log("test");
});

$("#etc_popover").on("show.bs.popover", function () {
  console.log("test");
});
