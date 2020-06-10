$(document).ready(function () {
  $('[data-toggle="popover"]').on("click", function () {
    const selectedPopover = $(this);
    const projectId = $(this).data("val");
    const kind = $(this).data("info");
    const documentId = $(this).data("document-id");
    url = "/sites/document/attach/" + projectId + "/list/";
    $.ajax({
      type: "GET",
      url: url,
      data: {
        kind: kind,
        documentId: documentId,
      },
      success: function (data) {
        const getData = JSON.parse(data);
        const getDocumentAttachs = getData["document_attach_names"];
        const documentAttachLists = [];
        getDocumentAttachs.forEach((ele) => {
          const element = `<div><a href="/sites/document/attach/${documentId}/detail/">${ele}</div>`;
          documentAttachLists.push(element);
        });

        if (getData) {
          selectedPopover.popover({
            trigger: "focus",
            html: true,
          });
          selectedPopover.attr("data-content", documentAttachLists.join(""));
          selectedPopover.popover("show");
        }
      },
      error: function (request, status, error) {
        alert("문서현황을 정상적으로 가지고 올 수 없습니다.");
      },
    });
  });
});
