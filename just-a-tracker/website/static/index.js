function deleteWorkspace(workspaceID, projectName) {
  const deleteWorkspaceMessage = `The workspace '${projectName.toString()}' and any data associated with it will be permanently deleted.
  
  Click 'Ok' if you are really sure you wish to continue.`;

  if (confirm(deleteWorkspaceMessage)) {
    fetch("/delete-workspace", {
      method: "POST",
      body: JSON.stringify({ workspaceID: workspaceID }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
}

function removeUser(
  workspaceID,
  projectName,
  userID,
  username,
  leaving,
  workspaceURL
) {
  let message = "";
  if (leaving == "true") {
    message = `Click ok if you are sure you wish to leave '${projectName}'.`;
  } else {
    message = `Click ok if you are sure you wish to remove '${username}' from the 
    workspace '${projectName}'`;
  }

  if (confirm(message)) {
    fetch("/remove-user", {
      method: "POST",
      body: JSON.stringify({ workspaceID: workspaceID, userID: userID }),
    }).then((_res) => {
      window.location.href = workspaceURL;
    });
  }
}

function markBug(bugID, makeOpen, makeImportant, workspaceURL) {
  fetch("/mark-bug", {
    method: "POST",
    body: JSON.stringify({
      bugID: bugID,
      makeOpen: makeOpen,
      makeImportant: makeImportant,
    }),
  }).then((_res) => {
    window.location.href = workspaceURL;
  });
}

function deleteBug(bugID, bugTitle, workspaceURL) {
  const deleteBugMessage = `The bug ${bugTitle} will be permanently deleted.
  
  If you understand and still want to proceed, click ok.`;

  if (confirm(deleteBugMessage)) {
    fetch("/delete-bug", {
      method: "POST",
      body: JSON.stringify({ bugID: bugID }),
    }).then((_res) => {
      window.location.href = workspaceURL;
    });
  }
}

function deleteComment(commentID, workspaceID, bugReportURL) {
  const deleteCommentMessage = `This comment will be permanently deleted.
  
  If you understand and still want to proceed, click ok.`;

  if (confirm(deleteCommentMessage)) {
    fetch("/delete-comment", {
      method: "POST",
      body: JSON.stringify({ commentID: commentID, workspaceID: workspaceID }),
    }).then((_res) => {
      window.location.href = bugReportURL;
    });
  }
}

function toggleShowClosedBugs(obj) {
  let closedBugs = $(".closed-bug");
  let isHidden = closedBugs.hasClass("d-none");
  let isChecked = $(obj).is(":checked");

  if (isChecked & isHidden) {
    closedBugs.removeClass("d-none");
  } else if (!isChecked & !isHidden) {
    closedBugs.addClass("d-none");
  }
}

window.onload = function () {
  // Workspace page
  if (window.location.pathname.indexOf("/workspace/") != -1) {
    // Adjust whether closed bugs are shown
    toggleShowClosedBugs(document.querySelector("#toggleSwitchClosedBugs"));
  }
};
