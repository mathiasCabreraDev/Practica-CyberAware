
var coloresUsados = [];

var colores = [

	"rgb(244, 67, 54)",
	"rgb(233, 30, 99)",
	"rgb(154, 91, 165)",
	"rgb(122, 96, 167)",
	"rgb(63, 81, 181)",
	"rgb(0, 188, 212)",
	"rgb(0, 150, 136)",
	"rgb(76, 175, 80)",
	"rgb(214, 150, 6)",
	"rgb(255, 152, 0)",
	"rgb(255, 87, 34)",
	"rgb(96, 125, 139)"
];

function getCookie(cname) {

	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');

	for(var i = 0; i <ca.length; i++) {

		var c = ca[i];

		while (c.charAt(0) == ' ') {

			c = c.substring(1);
		}

		if (c.indexOf(name) == 0) {

			return c.substring(name.length, c.length);
		}
	}

	return "";
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getUser() {

	var user = getCookie("user");

	if ( user ) {

		return JSON.parse( atob(user) );
	}
	else {

		return {

			logged : false
		};
	}
}

function setUser(user) {

	setCookie("user", btoa(JSON.stringify(user)));

	$("#signOut").show();
	$("#user-display-name").text(user.name);
}

function rand(min, max) {

    return Math.floor(Math.random() * (max - min + 1) + min);
}

function getRandomcolor() {

	var color;

	if ( colores.length == 0 ) {

		color = coloresUsados;
		coloresUsados = colores;
		colores = color;
	}

	color = colores.splice(rand(0, colores.length - 1), 1);

	coloresUsados.push( color );

	return color;
}

function getProgressBarColor(x){

	return "bg-" + ["danger", "info", "success", "primary", "primary"][ parseInt( (x+1)/25 ) ];
}

var nodeCount = 0;
var nodeTemplate = "";

function getCard(proyect) {

	var node = nodeTemplate;

	node = node.replace(/proyect-index/g, nodeCount); // more than 1 ocurrences
	node = node.replace("proyect-id", "card-" + (nodeCount++));
	node = node.replace("proyect-title", proyect.name);
	node = node.replace("proyect-description", proyect.description);
	node = node.replace("static/assets/proyect-default-image.jpg", proyect.image);
	node = node.replace("proyect-image-description", proyect.description);
	node = node.replace("proyect-status", proyect.status);
	node = node.replace(/proyect-progress/g, proyect.progress); // more than 1 ocurrences
	node = node.replace("proyect-progress-color", getProgressBarColor);
	node = node.replace("proyect-extra-classes", "text-white");
	node = node.replace("proyect-extra-styles", "background-color: " + getRandomcolor() + ";");
	node = node.replace("proyect-collaborators", proyect.collaborators.length);

	var user = getUser();

	if ( user.logged ) {

		if ( user.type == "root" ) {

			if ( proyect.status == "Finalizado" ) {

				node = node.replace("proyect-display-upload", "display: none;");
			}
			else {

				node = node.replace("proyect-display-upload", "");
			}

			node = node.replace("proyect-display-download", "");
		}
		else if ( user.type == "researcher" || user.type == "" || user.type == "entity" ) {

			node = node.replace("proyect-display-upload", "display: none;");
			node = node.replace("proyect-display-download", "");
		}
		else if ( user.type == "collaborator" ) {

			if ( proyect.status == "Finalizado" ) {

				node = node.replace("proyect-display-upload", "display: none;");
			}
			else {

				node = node.replace("proyect-display-upload", "");
			}

			node = node.replace("proyect-display-download", "display: none;");
		}
		else {

			node = node.replace("proyect-display-upload", "display: none;");
			node = node.replace("proyect-display-download", "display: none;");
		}
	}
	else {

		node = node.replace("proyect-display-upload", "display: none;");
		node = node.replace("proyect-display-download", "display: none;");
	}

	return $(node);
}

var proyects;

function loadProyectList() {

	$.ajax({
		url: "Back/management/ProyectList.php?rand=" + Math.random(),
		success: function(result){

			var container = $("#cards-container").empty();

			if ( result.empty ) {

				container.html('<div class="col"><h1 class="mb-4">' + result.message + '</h1></div>');
				return;
			}

			proyects = result.list;
			result.list.map( x => getCard(x).appendTo(container) );
		},
		error : function (result) {

			alert("error");
		}
	});
}

function IsJsonString(str) {

    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function poolPreview() {

	var URL = $("#poolURL").val();

	if ( URL.startsWith("http") ) {

		URL = btoa(URL);
	}
	else {

		return alert("Enter valid url");
	}

	$.ajax({

		url: "Back/data-retrieve/URLPreview.php?url=" + URL,
		dataType: 'json',
		success: function(result) {

			$("#contentPreview2").html( "<pre>" + JSON.stringify(result, null, 2) + "</pre>" );
		},

		error : function(jqXHR, exception) {

            if (jqXHR.status === 0) {
                alert('Not connect.\n Check if servert has CORS enabled or Check your Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
	});
}

function getData(event, index) {

	setProyect(index);

	window.open("Back/data-provide/?proyectID=" + selectedProyect.id + "&filter=None&groupBy=None&format=.json");

}

var selectedProyect;

function setProyect(index) {

	selectedProyect = proyects[index];
}

function verCollaborators(index) {

	setProyect(index);

	$("#verCollaboratorsModalTitle").html( "Listado de colaboradores<br>" + selectedProyect.name );

	if ( selectedProyect.collaborators.length == 0 ) {

		$("#verCollaboratorsModalBody").text("No hay colaboradores");
	}
	else {

		var listado = "";

		for (var i=0; i<selectedProyect.collaborators.length; i++) {
			//TODO: romina quiere que los nombres de los colaboradores sean linkeables
			// se podria implementar un modulo "perfil" de usuario para ver a otros usuarios
			// ver que proyectos colaboran (separar en public y private para mostar solo los publicos)
			listado += "<div>" + selectedProyect.collaborators[i] + "</div>";
		}

		$("#verCollaboratorsModalBody").html(listado);
	}

	$("#verCollaboratorsModal").modal("show");
}

function processImage(input) {

	if ( input.files && input.files[0] ) {

		var reader = new FileReader();

		reader.onload = function(e) {

			$('#image-preview').empty().append( $(new Image()).attr('class', 'card-img-top rounded-0').attr('src', e.target.result) );
		}

		reader.readAsDataURL(input.files[0]);
	}
}

function createProyect() {

	var name = $("#np-name").val();
	var description = $("#np-description").val();
	var imageUpload = document.getElementById("np-image");

	var formData = new FormData();
	formData.append('name', name);
	formData.append('description', description);

	if ( imageUpload.files && imageUpload.files[0] ) {

		formData.append('image', imageUpload.files[0]);
	}

	$.ajax({

		url: 'Back/management/ProyectAdd.php',
		type: 'POST',
		data: formData,
		contentType: false,
		processData: false,
		success : function (result) {

			if ( result.created ) {

				loadProyectList();
				$('#image-preview').empty().append( $(new Image()).attr('class', 'card-img-top rounded-0').attr('src', 'static/assets/proyect-default-image.jpg') );
				$('#createProyectForm').trigger("reset");
				$('#addProyectModal').modal('hide');
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

var fullCounterCount = 0;

function updateFullCounter() {

	fullCounterCount--;

	if ( !fullCounterCount ) {

		alert("Susccesfully Shared");
		$("ModalShareDataFinish").modal("hide");
	}
}

function finishMeBaby() {

	if ( originalSheet ) {

		fullCounterCount = originalSheet.options.data.length;

		for (var i=0; i<originalSheet.options.data.length; i++) {

			var row = originalSheet.options.data[i];

			// Compartir?	Sensor	Valor	Tipo	Unidad
			// [0]		[1]	[2]	[3]	[4]

			if ( row[0] === true ) {

				$.ajax({

					url: "Back/management/AddSensor.php?station=" + selectedStation + "&field=" + row[1] + "&type=" + row[3] + "&unit=" + row[4],
					dataType: 'json',
					success: function(result) {

						updateFullCounter();
					},

					error : function(jqXHR, exception) {

				    if (jqXHR.status === 0) {
					alert('Not connect.\n Check if servert has CORS enabled or Check your Network.');
				    } else if (jqXHR.status == 404) {
					alert('Requested page not found. [404]');
				    } else if (jqXHR.status == 500) {
					alert('Internal Server Error [500].');
				    } else if (exception === 'parsererror') {
					alert('Requested JSON parse failed.');
				    } else if (exception === 'timeout') {
					alert('Time out error.');

				    } else if (exception === 'abort') {
					alert('Ajax request aborted.');
				    } else {
					alert('Uncaught Error.\n' + jqXHR.responseText);
				    }
				}
				});
			}
		}
	}
	else {

		alert("Error");
	}
}

var uploadedSheet;

function handleUpload( input ) {

	if ( input.files && input.files[0] ) {

		var formData = new FormData();
		formData.append('file', input.files[0] );

		$.ajax({
		       url : 'Back/data-transform/upload.php',
		       type : 'POST',
		       data : formData,
		       processData: false,
		       contentType: false,
		       success : function(data) {

				if ( data.status !== "success" ) {

					return alert("error");
				}

				$("#my-csv").empty();
				$("#my-csv").style="max-height:600px;padding-top:0px !important;";

				// create jexcel objet with new url
				uploadedSheet = jexcel(document.createElement('div'), {

					csv : 'Back/data-transform/' + data.file,
					csvDelimiter : prompt('Enter CSV delimiter: ', ';'),
					onload : function () {
						var data = [];
						var headers = uploadedSheet.getHeaders().split(";");

						for (var i=0; i<headers.length; i++) {

							data.push( [headers[i], true] );
						}

						uploadedSheet = jexcel(document.getElementById('my-csv'), {

							data : data,
							columns : [

								{ type : 'text', title : 'Dato', width : 180 },
								{ type : 'checkbox', title : 'Compartir?', width : 180 }
							],
							onload : function () {

								$('#my-csv').append($('<button onclick="ginebra()" class="btn btn-primary pl-5 pr-5 mb-3 mt-3">Compartir Datos Seleccionados</button>'));
							}
						});
					}
				});



				$("#ModalShareData").modal("hide");
				$("#ModalTransformData").modal("show");
		       }
		});
	}

}

function ginebra() {

	$("#ModalTransformData").modal("hide");
}

function syncromatica() {

	var URL = $("#station-url").val().trim();

	if ( URL.startsWith("http") ) {

		URL = btoa(URL);
	}
	else {

		return alert("Enter valid url");
	}

	$.ajax({

		url: "Back/data-retrieve/URLPreview.php?url=" + URL,
		dataType: 'json',
		success: function(result) {

			$("#station-preview").empty().html( "<pre class='text-left'>" + JSON.stringify(result, null, 2) + "</pre>" );
		},

		error : function(jqXHR, exception) {

            if (jqXHR.status === 0) {
                alert('Not connect.\n Check if servert has CORS enabled or Check your Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
	});
}

function getSelectBonito(index) {

	var datatypes = ['Ignorar este campo', 'DATE', 'INT','FLOAT','DOUBLE','BOOLEAN','DATETIME','TIMESTAMP','STRING'];

	var select = '<select id="select-bonito-'+index+'">';

	select += '<option value="0" selected>' + datatypes[0] + '</option>';

	for (var i=1; i<datatypes.length; i++) {

		select += '<option value="'+i+'">' + datatypes[i] + '</option>';
	}

	return select + '</select>';
}

var selectedStation;

function wachinango() {

	var preview = $("#station-url");

	if ( preview.val() == "" ) {

		return alert("Enter URL");
	}
	else {

		selectedStation = $("#selectedStationDesu").children("option:selected").val();

		$.ajax({

			url: 'Back/management/UpdateStationURL.php?station=' + selectedStation + '&URL=' + preview.val(),
			type: 'GET',
			success : function (result) {

				alert(result.message);

				if ( result.updated ) {

					$("#ModalSyncData").modal("hide");
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
}

function weee(obj) {
	//FIXME UNUSED
	for (let [key, value] of Object.entries(obj)) {

		if ( typeof value == "object" ) {

			weee(value);
		}
		else {

			$("#data-define-content").append($('<div class="charanco"><span>' + key + '</span> (' + value + ') ' + getSelectBonito(key) +'</div>'));
		}
	}
}

function solis() {

	var station = $("#selectedStationDesu").children("option:selected").val();

	$(".charanco").each(function (a, b) {

		var field = $(b).children(":first").text();
		var type = $(b).children(":last").children("option:selected").val();

		if ( type > 0 ) {

			$.ajax({

				url: 'Back/management/AddSensor.php?field=' + field + '&type=' + type + "&station=" + station,
				type: 'GET',
				success : function (result) {

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
	});
}

var originalSheet;

function forAzeroth() {

	$.ajax({

		url: "Back/data-retrieve/ForAzeroth.php?stationID=" + selectedStation,
		dataType: 'json',
		success: function(result) {

			$("#ModalShareDataFinish").modal('show');

			var data = [];

			for ( a in result ) {

				data.push([true, a, result[a], 'String', 'None']);
			}

			console.log( data );

			$("#wew").empty();

			originalSheet = jexcel(document.getElementById('wew'), {

				data : data,
				columns: [
					{ type: 'checkbox', title:'Compartir este sensor', width:180 },
					{ type: 'text', title:'Sensor', width:180 },
					{ type: 'text', title:'Valor', width:180 },
					{ type: 'dropdown', title:'Tipo de Dato', source : ['String', 'Date', 'Int', 'Float'], width:180 },
					{ type: 'text', title:'Unidad de medicion', width:180 }
				]
			});
		},

		error : function(jqXHR, exception) {

            if (jqXHR.status === 0) {
                alert('Not connect.\n Check if servert has CORS enabled or Check your Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');

            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
	});
}

function nextStepBaby() {

	try {

		selectedStation = $("#selectedStation").children("option:selected").val();

		if ( selectedStation == undefined ) {

			alert("Necesitas tener registrada al menos 1 estacion");
		}
		else {

			$("#ModalShareData").modal('hide');
			forAzeroth();
		}
	}
	catch (e) {

		alert("Necesitas tener registrada al menos 1 estacion");
	}
}

function TellMeBaby() {

	$.ajax({

		url: 'Back/management/StationList.php?rand='+Math.random(),
		type: 'GET',
		success : function (result) {

			if ( result.empty ) {

				alert("Necesitas registrar una estacion primero");
			}
			else {

				var select = '<select id="selectedStationDesu">';

				for (var i=0; i<result.list.length; i++) {

					select += '<option value="'+result.list[i].id+'">'+result.list[i].name+'</option>'
				}

				select += '</select>';

				$("#listadoEstacionesDesu").empty().html(select);

				$('#ModalSyncData').modal('show');
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

function preShare(index) {

	$("#listadoEstaciones").empty().html('<div class="spinner-border text-info" role="status"></div>');

	setProyect(index);

	$("#collab-with").text( selectedProyect.name );
	$("#collab-with-2").text( selectedProyect.name );

	$.ajax({

		url: 'Back/management/StationList.php?rand='+Math.random(),
		type: 'GET',
		success : function (result) {

			if ( result.empty ) {

				$("#listadoEstaciones").empty().html('<h5 class="small text-danger">'+result.message+'</h5>');
			}
			else {

				var select = '<select id="selectedStation">';

				for (var i=0; i<result.list.length; i++) {

					select += '<option value="'+result.list[i].id+'">'+result.list[i].name+'</option>'
				}

				select += '</select>';

				$("#listadoEstaciones").empty().html(select);
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

function createStation() {

	var name = $("#station-name").val().trim();
	var lat = $("#station-lat").val().trim();
	var lng = $("#station-lng").val().trim();
	var description = $("#station-description").val().trim();

	if ( name == "" || lat == "" || lng == "" || description == "") {

		return alert("Empty fields");
	}

	$.ajax({

		url: 'Back/management/AddStation.php?name='+name+"&lat="+lat+"&lng="+lng+"&description="+description,
		type: 'GET',
		success : function (result) {

			if ( result.created ) {

				alert("Success");
				$('#FormAddStation').trigger("reset");
				$('#ModalAddStation').modal('hide');
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

function checkSession() {

	var user = getUser();

	if ( user.logged ) {

		$.ajax({

			url: 'Back/user-auth/SessionValidate.php?token=' + user.token + "&rand=" + Math.random(),
			type: 'GET',
			success : function (result) {

				if ( result.valid ) {

					setUser(result.user);

					updateOptions();
					loadProyectList();
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
	else {

		updateOptions();
		loadProyectList();
	}
}

function logout() {

	setCookie("user", "");
	updateOptions();
	loadProyectList();
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

				updateOptions();
				loadProyectList();
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

function updateOptions() {

	var user = getUser();

	if ( user.type == "root" ) {

		$(".peasant-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).show();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).show();
		});
		$(".admin-opt").each(function (a, b) {

			$(b).show();
		});
	}
	else if ( user.type == "entity" ) {

		$(".admin-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".peasant-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).show();
		});
	}
	else if ( user.type == "collaborator" ) {

		$(".admin-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".peasant-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).show();
		});
	}
	else if ( user.type == "citizen" ) {

		$(".admin-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".peasant-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).show();
		});
	}
	else if ( user.type == "researcher" || user.type == "developer" ) {

		$(".admin-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".peasant-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".researcher-opt").each(function (a, b) {

			$(b).show();
		});
	}
	else {

		$(".admin-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".entity-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".collaborator-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".citizen-opt").each(function (a, b) {

			$(b).hide();
		});
		$(".peasant-opt").each(function (a, b) {

			$(b).show();
		});
	}
}

function goDownloads() {

	//setProyect(index);
alert(ok);
	window.open("descargar.php");

}


/*******************************************************************************************************************/
/******************************************************  START  ****************************************************/
/*******************************************************************************************************************/

window.onload = function() {

	nodeTemplate = $("#proyect-id").prop("outerHTML");
	checkSession();
	$("#haruhime").show();
}
