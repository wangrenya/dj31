$(function (){

  let $img = $('.form-item .captcha-graph-img img') ;//获取图像
     let $username = $('#user_name');



  genre();
  $img.click(genre);
  function genre() {
      image_code_uuid=generateUUID()
      let imageCodeUrl = '/image_code/' + image_code_uuid +'/';
       $img.attr('src', imageCodeUrl)

  }



// 生成图片UUID验证码
  function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
  }

  // 用户用户名
    // 2、用户名验证逻辑
    // blur,触发失去焦点事件


  $username.blur(function () {
    fn_check_username();
  });

  function fn_check_username() {
    let sUsername = $username.val();  // 获取用户名字符串
    if (sUsername === "") {
      message.showError('用户名不能为空！');
      return
    }
    if (!(/^\w{5,20}$/).test(sUsername)) {
      message.showError('请输入5-20个字符的用户名');
      return
    }

    // 发送ajax请求，去后端查询用户名是否存在
    $.ajax({
      url: '/username/' + sUsername + '/',
      type: 'GET',
      dataType: 'json',
    })
      .done(function (res) {
        if (res['count'] ===1) {
          message.showError('已注册，请重新输入！')
        } else {
          message.showInfo( '能正常使用！')
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });
  }
})