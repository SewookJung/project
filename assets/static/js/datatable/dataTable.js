$(document).ready(function() {
  $("#asset__table").DataTable({
    order: [
      [3, "asc"],
      [0, "asc"]
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›"
      }
    }
  });

  $("#myTable1, #myTable2").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›"
      }
    }
  });
});
