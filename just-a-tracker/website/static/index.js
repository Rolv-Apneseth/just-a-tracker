function deleteWorkspace(workspaceID, projectName) {
  const deleteWorkspaceMessage = `The workspace '${projectName.toString()}' and any data associated with it will be permanently deleted.
  
  If you really sure you wish to delete this workspace, click 'OK'.`;

  if (confirm(deleteWorkspaceMessage)) {
    fetch("/delete-workspace", {
      method: "POST",
      body: JSON.stringify({ workspaceID: workspaceID }),
    }).then((_res) => {
      window.location.href = "/workspace-hub";
    });
  }
}

function removeUser(workspaceID, projectName, userID, username, leaving) {
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
      window.location.href = `/workspace/${workspaceID}`;
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

function toggleShowClosedBugs(obj) {
  if ($(obj).is(":checked")) {
    $(".closed-bug").css("display", "");
  } else {
    $(".closed-bug").css("display", "none");
  }
}

window.onload = function () {
  // Workspace page
  if (window.location.pathname.indexOf("/workspace/") != -1) {
    // Adjust whether closed bugs are shown
    toggleShowClosedBugs(document.querySelector("#toggleSwitchClosedBugs"));
  }
};
