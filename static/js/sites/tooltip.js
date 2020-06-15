$(document).ready(function () {
  $('[data-toggle="popover"]').on("click", function () {
    const selectedPopover = $(this);
    const projectId = $(this).data("val");
    const kind = $(this).data("info");
    const documentId = $(this).data("document-id");
    const middleClass = $(this).data("middle-class");
    url = "/sites/document/attach/" + projectId + "/list/";
    $.ajax({
      type: "GET",
      url: url,
      data: {
        kind: kind,
        documentId: documentId,
        middleClass: middleClass,
      },
      success: function (data) {
        const getData = JSON.parse(data);
        const getDocumentAttachs = getData["document_attach_names"];
        const documentAttachLists = [];
        getDocumentAttachs.forEach((ele) => {
          const documentAttach = `<div><a href="/sites/document/attach/${documentId}/${kind}/${middleClass}/detail/">${ele}</div>`;
          documentAttachLists.push(documentAttach);
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
