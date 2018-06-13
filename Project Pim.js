function CreateGroup() {
	var groupnamePost = document.getElementById("groupnameinput").value;

    $.ajax({
       url: "https://pim-project-b9c84.firebaseapp.com/new-game",
       type: 'post',
       dataType: 'json',
	   data: { groupname: groupnamePost },
       async: true,
       success: function(data) {
			alert('Groep aanmaken gelukt.');
			location.reload();
			alert(data);
		},
	   error: function(data) {
			alert(data);
		}
    });

}
