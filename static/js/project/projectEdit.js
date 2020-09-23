const commentsChangeBtn = document.getElementById("comments-change-btn");
const supportAddBtn = document.getElementById("support-add-btn");

commentsChangeBtn.addEventListener("click", () => {
  const projectComments = document.getElementById("comments");
  projectComments.disabled = false;
});

supportAddBtn.addEventListener("click", () => {
  const projectSupportHistory = document.getElementById("supports");
  projectSupportHistory.disabled = false;
});
