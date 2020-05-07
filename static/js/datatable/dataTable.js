$(document).ready(function () {
  $("#asset__table").DataTable({
    order: [
      [3, "asc"],
      [0, "asc"],
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#myTable1").DataTable({
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#sites_table").DataTable({
    columnDefs: [
      { orderable: true, targets: [0] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#weekly_table").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [0] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });

  $("#doument_attach").DataTable({
    pageLength: 15,
    lengthMenu: [5, 10, 15, 20, 30, 50, 100],
    columnDefs: [
      { orderable: true, targets: [0, 1] },
      { orderable: false, targets: "_all" },
    ],
    language: {
      paginate: {
        previous: "‹",
        next: "›",
      },
    },
  });
});
