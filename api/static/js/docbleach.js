document.body.classList.add('js');
var docbleach_endpoint = "/v1/";

(function () {
  var formElement = document.querySelector("form#uploadForm");
  var labelElement = document.querySelector("form#uploadForm label span");
  var inputElement = document.querySelector("input#file");

  if (window.FileReader) {
    addEventHandler(labelElement, 'dragover', function (e) {
      e.preventDefault();
    });

    addEventHandler(labelElement, 'dragleave', function (e) {
      e.preventDefault();
    });

    addEventHandler(labelElement, 'drop', function (e) {
      e = e || window.event; // get window.event if e argument missing (in IE)
      e.preventDefault();

      var dt = e.dataTransfer;
      var files = dt.files;
      for (var i = 0; i < files.length; i++) {
        var file = files[i];

        var formData = new FormData();
        formData.append("file", file);
        convertFile(formData);
      }
      return false;
    });
  }

  addEventHandler(inputElement, "change", function (e) {
    convertFile(new FormData(formElement));
  }, false);

  function addEventHandler(obj, evt, handler) {
    if (obj === null) {
      return;
    }
    if (obj.addEventListener) {
      // W3C method
      obj.addEventListener(evt, handler, false);
    } else if (obj.attachEvent) {
      // IE method.
      obj.attachEvent('on' + evt, handler);
    } else {
      // Old school method.
      obj['on' + evt] = handler;
    }
  }

  function convertFile(formData) {
    swal({
      title: "Uplading file",
      text: "...",
      type: "info",
      allowOutsideClick: false,
      allowEscapeKey: false
    });
    swal.showLoading();
    $.ajax({
      type: "POST",
      url: docbleach_endpoint + "tasks",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        swal({
          title: "Sanitizing file",
          text: "...",
          type: "info",
          allowOutsideClick: false,
          allowEscapeKey: false
        });
        swal.showLoading();
        var task_id = data["task_id"];
        console.log("Got a task id: " + task_id);
        setTimeout(function () {
          checkFileStatus(task_id);
        }, 250);
      }
    });
  }

  function checkFileStatus(task_id) {
    $.ajax({
      type: "GET",
      url: docbleach_endpoint + "tasks/" + task_id,
      success: function (data) {
        console.log(data);
        console.log("Got a task id state: " + task_id);
        if (data.status === "PENDING") {
          setTimeout(function () {
            checkFileStatus(task_id);
          }, 250);
          return;
        }
        displayResponse(
            {infos: [data.result.output], link: data.result.final_file});
      }
    });
  }
})();

function displayResponse(response) {
  if (response.errors && response.errors.join) {
    console.log(response.errors);
    swal("An error occured", "", "error");
    return;
  }
  if (response.infos && response.infos.join) {
    var htmlCode = parseDocbleach(response.infos.join("\n"));

    var modalData = {
      title: "Results",
      html: htmlCode,
      type: "success",
      allowOutsideClick: true,
      confirmButtonColor: "#73B6D6",
      width: "60%"
    };
    if (response.link) {
      modalData["confirmButtonText"] = "Download the sanitized file";
    } else {
      modalData["timer"] = 2000;
    }
    swal.hideLoading();
    swal(modalData).then(function () {
      if (response.link) {
        download(response.link);
      }
    });
  } else if (response.link) {
    download(response.link);
    swal.hideLoading();
    swal({
      text: "Download started",
      type: "success",
      timer: 2000
    });
  }
}

function parseDocbleach(infos) {
  var parent = document.createElement("div");
  var lines = infos.split(/\r?\n/); // Allow multiple lines per blob

  lines.forEach(function (line) {
    var child = document.createElement("p");

    if (line.indexOf("WARN ") === 0) {
      child.classList.add("docbleach_warning");
      line = line.substring("WARN ".length);
    } else if (line.indexOf("INFO ") === 0) {
      child.classList.add("docbleach_info");
      line = line.substring("INFO ".length);
    } else if (line.indexOf("ERROR ") === 0) {
      child.classList.add("docbleach_severe");
      line = line.substring("ERROR ".length);
    } else if (line.indexOf("FATAL ") === 0) {
      child.classList.add("docbleach_severe");
      line = line.substring("FATAL ".length);
    }
    child.innerText = line;
    parent.appendChild(child);
  });
  return parent.innerHTML;
}

function download(link) {
  var anchor = document.createElement('a');
  anchor.href = link;
  // anchor.target = '_blank';
  anchor.setAttribute("download", "");
  document.body.appendChild(anchor);
  anchor.click();
}