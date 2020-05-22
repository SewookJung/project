$(document).ready(function () {
  const content = [
    '<div class="timePickerCanvas"><a href="#">NAC 제품소개서</a></div>',
    '<div class="timePickerClock timePickerHours"><a href="#">EDR 제품소개서</a></div>',
    '<div class="timePickerClock timePickerMinutes"><a href="#">GPI 제품소개서</a></div>',
  ].join("");

  $('[data-toggle="popover_presales"]').popover({
    trigger: "focus",
    html: true,
    content: content,
  });
});
