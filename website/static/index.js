function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/note";
    });
  }
function showInfo(emailId) {
    fetch("/note", {
      method: "POST",
      body: JSON.stringify({ emailId: emailId }),
    }).then((_res) => {
      window.location.href = "/note";
    });
  }
