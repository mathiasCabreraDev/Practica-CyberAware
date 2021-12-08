function setUser(user) {

	setCookie("user", btoa(JSON.stringify(user)));

	$("#signOut").show();
	$("#user-display-name").text(user.name);
}

function setCookie(cname, cvalue, exdays) {

  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function doLogin() {

	var mail = $("#login-mail").val();
	var pass = $("#login-pass").val();

	//FIXME don't use md5
	pass = md5(pass);

	$.ajax({

		url: 'Back/user-auth/SessionLogin.php?mail=' + mail + "&pass=" + pass + "&rand=" + Math.random(),
		type: 'GET',
		success : function (result) {

			if ( result.valid ) {

				setUser(result.user);

				location.reload()
			}
			else {

				alert("Error: " + result.message);
			}
		},
		error : function (result) {

			try {

				if ( result.message ) {

					alert("Error: " + result.message);
					return;
				}
			}
			catch (e) {}

			alert("Error: " + result);
		}
	});

}

function waitForEnterToLogin( event ) {

	if ( event.keyCode == 13 ) {

		doLogin();
	}
}

function waitForEnterToRegister( event ) {

	if ( event.keyCode == 13 ) {

		doRegister();
	}
}

function doRegister() {

	var name = $("#register-name").val();
	var mail = $("#register-mail").val();
	var pass = $("#register-pass").val();
	var confirm = $("#register-pass-confirm").val();

	if ( pass != confirm ) {

		return alert("Las claves no coinciden");
	}

	//FIXME don't use md5 for passwords!!
	pass = md5(pass);

	$.ajax({

		url: 'Back/user-auth/RegisterUser.php?rand=' + Math.random(),
		type: 'POST',
		data : {

			user : name,
			mail : mail,
			pass : pass
		},
		success : function (result) {

			if ( result.valid ) {

				setUser(result.user);

				location.reload();
			}
			else {

				alert("Error: " + result.message);
			}
		},
		error : function (result) {

			try {

				if ( result.message ) {

					alert("Error: " + result.message);
					return;
				}
			}
			catch (e) {}

			alert("Error: " + result);
		}
	});

}
