$(function () {
    let $up_to_server = $('#upload-news-thumbnail');
    let $Image_url = $('#news-thumbnail-url');

    $up_to_server.change(function () {
        let file = this.files[0];

        let oFormData = new FormData();
        oFormData.append('image_files',file);

        $.ajax({
            url :'/admin/newsedit/images/',
            method:'POST',
            data:oFormData,
            processData:false,
            contentType:false
        })
            .done(function (res) {
            if (res.errno==='0'){
                message.showSuccess(res.errmsg);
                let sImageUrl = res['data']['image_url'];
                $Image_url.val(sImageUrl);

            }else{
                message.showError(res.errmsg)
            }







            })

            .fail(function () {
                message.showError('服务器超时，请重试！！')
            })









    });


 // ================== 发布文章 ================
 let $newsBtn = $("#btn-pub-news");
  $newsBtn.click(function () {




    // 判断文章标题是否为空
    let sTitle = $("#news-title").val();  // 获取文章标题
    if (!sTitle) {
        message.showError('请填写文章标题！');
        return
    }
    // 判断文章摘要是否为空
    let sDesc = $("#news-desc").val();  // 获取文章摘要
    if (!sDesc) {
        message.showError('请填写文章摘要！');
        return
    }

    let sTagId = $("#news-category").val();
    if (!sTagId || sTagId === '0') {
      message.showError('请选择文章标签')
      return
    }

    let sThumbnailUrl = $Image_url.val();
    if (!sThumbnailUrl) {
      message.showError('请上传文章缩略图')
      return
    }
    let sContentHtml = $(".markdown-body").html();
    console.log(sContentHtml);
    // let sContentHtml = $("#content").val();
    if (!sContentHtml || sContentHtml === '<p><br></p>') {
        message.showError('请填写文章内容！');
        return
    }

    // 获取news_id 存在表示更新 不存在表示发表
    let newsId = $(this).data("news-id");
    let url = newsId ? '/admin/newsedit/' + newsId + '/' : '/admin/newsedit/pub/';


    let data = {
      "title": sTitle,
      "digest": sDesc,
      "tag": sTagId,
      "image_url": sThumbnailUrl,
      "content": sContentHtml,
    };

    $.ajax({
      // 请求地址
      url: url,
      // 请求方式
      type: newsId ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (res) {
        if (res.errno === "0") {
          if (newsId) {
              message.showSuccess("文章更新成功");
              setTimeout(function () {
                window.location.href='/admin/newsmanage/';
                }, 1000)

          } else {
              message.showSuccess("文章添加成功");
              setTimeout(function () {
              window.location.href='/admin/newsmanage/';
                }, 1000)
          }

        } else {
          fAlert.alertErrorToast(res.errmsg);
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });
  });

  // get cookie using jQuery
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

 });