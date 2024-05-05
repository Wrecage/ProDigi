function startEditing() {
  var taskId = document.getElementById("task-id").value; // Assuming you have a hidden input field with the task ID
  window.location.href = '/task_detail/' + taskId + '/?editing=true';
}
