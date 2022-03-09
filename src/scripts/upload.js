import * as Decode from './decode.js';

export function initializeUploads() {

    $('.upload').each(initializeUpload);

}

function initializeUpload() {

    var upload = $(this)[0];

    $(this).upload({
        action: '/upload',
        dataType: 'text',
        label: '',
        postKey: 'file',
    })
    // .on('start.upload', onStart)
    // // .on("filestart.upload", onFileStart)
    // // .on("fileprogress.upload", onFileProgress)
    // // .on("filecomplete.upload", onFileComplete)
    // .on("complete.upload", onComplete);
    // // .on("fileerror.upload", onFileError);
    // // As in the code snippet from the question in https://stackoverflow.com/questions/31865423/formstone-upload-maxqueue-not-working

    // function onStart(event, files) {
    //     console.log(files);
    //     var html = '';
    //     for (var i = 0; i < files.length; i++) {
    //         html += '<li data-index="' + files[i].index + '"><span class="file">' + files[i].name + '</span><span class="progress">Cola</span></li>';
    //     }
    //     console.log(html);
    // }

    // function onComplete(e) {
    //     console.log('done');
    // }

    upload.innerHTML = Decode.decodeUploadContent(upload.id, upload.innerHTML);
    $($(`#${upload.id}-content`).children()[0]).attr('id', `${upload.id}-body`);
    $(`#${upload.id}-body`)[0].innerHTML = Decode.decodeUploadButton();

}
