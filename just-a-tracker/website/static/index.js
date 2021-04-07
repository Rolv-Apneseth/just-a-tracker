function deleteWorkspace(workspaceID, projectName) {
  console.log(projectName);
  var deleteWorkspaceMessage = `The workspace '${projectName.toString()}' and any data associated with it will be permanently deleted.
  
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
