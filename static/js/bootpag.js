// $(".assets-pagination")
//   .bootpag({
//     total: 5
//   })
//   .on("page", function(event, num) {
//     $(".table").html("Page " + num); // or some ajax content loading...

//     // ... after content load -> change total to 10
//     // $(this).bootpag({ total: 10, maxVisible: 10 });
//   });

const test = haha => {
  console.log(haha);
};

$("#pagination-here").bootpag({
  total: 10,
  page: 1,
  maxVisible: 5,
  leaps: true
});

//page click action
$("#pagination-here").on("page", function(event, num) {
  //show / hide content or pull via ajax etc
  $("#content").html("Page " + num);
});
