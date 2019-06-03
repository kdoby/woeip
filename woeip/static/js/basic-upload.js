$(function () {
    /* 1. OPEN THE FILE EXPLORER WINDOW */
    $(".js-upload-documents").click(function () {
      $("#fileupload").click();
    });
  
    uploadButton = $('<button/>')
      .addClass('button uploadButton')
      .prop('disabled', true)
      .text('Processing...')
      .on('click', function () {
          var $this = $(this),
              data = $this.data();
          $this
              .off('click')
              .text('Abort')
              .on('click', function () {
                  $this.remove();
                  data.abort();
              });
          data.submit().always(function () {
              $this.remove();
          });
      });

    $('#fileupload').fileupload({
        dataType: 'json',
        autoUpload: false,
        acceptFileTypes: /(\.|\/)(csv|log)$/i,
        maxFileSize: 100000,
        done: function (e, data) { 
          if (data.result.is_valid) {
            $("#gallery tbody").prepend(
              "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td>" +
              "<td><a class='alert button' href='" + data.result.delete_url + "'>Delete</a></td>" +
              "</tr>"
            )
          }
        },
    }).on('fileuploadadd', function (e, data) {
        console.log(data.files);
        data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<p/>')
                    .append($('<span/>').text(file.name));
            if (!index) {
                node
                    .append(uploadButton.clone(true).data(data));
            }
            node.appendTo(data.context);
        });
    }).on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.error) {
            node
                .append('<br>')
                .append($('<span class="text-danger"/>').text(file.error));
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
    }).on('fileuploadprogressall', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('.progress').css(
            'width',
            progress + '%'
        );
    }).on('fileuploaddone', function (e, data) {
        $.each(data.result.files, function (index, file) {
            if (file.url) {
                var link = $('<a>')
                    .attr('target', '_blank')
                    .prop('href', file.url);
                $(data.context.children()[index])
                    .wrap(link);
            } else if (file.error) {
                var error = $('<span class="text-danger"/>').text(file.error);
                $(data.context.children()[index])
                    .append('<br>')
                    .append(error);
            }
        });
    }).on('fileuploadfail', function (e, data) {
        $.each(data.files, function (index) {
            var error = $('<span class="text-danger"/>').text('File upload failed.');
            $(data.context.children()[index])
                .append('<br>')
                .append(error);
        });
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
  
  });