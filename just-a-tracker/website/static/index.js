function deleteWorkspace(workspaceID) {
  fetch("/delete-workspace", {
    method: "POST",
    body: JSON.stringify({ workspaceID: workspaceID }),
  }).then((_res) => {
    window.location.href = "/workspace-hub";
  });
}
