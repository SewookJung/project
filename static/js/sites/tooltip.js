$(function() {
  $('[data-toggle="tooltip_wbs"]').tooltip({
    title: "<div>[삼성디스플레이] WBS</div>",
    html: true
  });
  $('[data-toggle="tooltip_confirm"]').tooltip({
    title:
      "<div>[삼성디스플레이] 검수확인서 1.0V</div><div>[삼성디스플레이] 검수확인서 1.1</div>",
    html: true
  });
});

$(document).ready(function() {
  var content = [
    '<div class="timePickerCanvas"><a href="#">NAC 제품소개서</a></div>',
    '<div class="timePickerClock timePickerHours"><a href="#">EDR 제품소개서</a></div>',
    '<div class="timePickerClock timePickerMinutes"><a href="#">GPI 제품소개서</a></div>'
  ].join("");

  $('[data-toggle="popover_presales"]').popover({
    trigger: "focus",
    html: true,
    content: content
  });
});
