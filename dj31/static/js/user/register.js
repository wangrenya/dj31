$(function (){

  let $img = $('.form-item .captcha-graph-img img') ;//获取图像
     let $username = $('#user_name');
     let $mobile   = $(' #mobile ');
     let image_code_uuid = '';
// 标记
    let isUsernameReady = false,
        isPasswordReady = false,
        isMobileReady = false;
        send_flag = true;    // 短信标记



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
          message.showError('这个用户名已被注册，请重新输入用户名！')
        } else {
          message.showInfo( '用户名，能正常使用！')
            isUsernameReady = true;
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });
  }

 //手机号验证逻辑
    $mobile.blur(function () {
    fn_check_mobile();
  });
    function fn_check_mobile(){
        let sMobile = $mobile.val();
        if ( sMobile === ''){
            message.showError('手机号不能为空！');
            return
        }
        if (!(/^1[345789]\d{9}$/).test(sMobile)) {
            message.showError('手机号格式输入错误请重新输入');
            return;

        }
    $.ajax(
        {
            url : '/mobile/' + sMobile + '/',
            type: 'GET',
            dataType: 'json',
        }
    )
        .done(function (res) {
        if (res['count'] ===1) {
          message.showError('此手机号已被注册，请更换手机号码重新输入！')
        } else {
          message.showInfo( '手机号格式正确，能正常使用！')
             isMobileReady = true;
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });


    }





    // 4、发送短信验证码逻辑
  let $smsCodeBtn = $('.form-item .sms-captcha');  // 获取短信验证码按钮元素，需要定义一个id为input_smscode
  let $imgCodeText = $('#input_captcha');  // 获取用户输入的图片验证码元素，需要定义一个id为input_captcha

  $smsCodeBtn.click(function () {
    // 判断手机号是否输入
      if(send_flag){

          send_flag = false;
          // 判断手机号码是否准备好
        if(!isMobileReady){
            fn_check_mobile();
            return
        }
// 13535353535
    // 判断用户是否输入图片验证码
    let text = $imgCodeText.val();  // 获取用户输入的图片验证码文本
    if (!text) {
        message.showError('请填写验证码！');
        return
    }

    if (!image_code_uuid) {
      message.showError('图片UUID为空');
      return
    }

    // 正常
    let SdataParams = {
      "mobile": $mobile.val(),   // 获取用户输入的手机号
      "text": text,   // 获取用户输入的图片验证码文本
      "image_code_id": image_code_uuid  // 获取图片UUID
    };
    // 向后端发送请求
    $.ajax({
      // 请求地址
      url: "/sms_code/",
      // 请求方式
      type: "POST",
      // 向后端发送csrf token
      headers: {
                // 根据后端开启的CSRFProtect保护，cookie字段名固定为X-CSRFToken
                "X-CSRFToken": getCookie("csrftoken")
      },

      data: JSON.stringify(SdataParams),
      // data: JSON.stringify(SdataParams),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })

      .done(function (res) {
          console.log(res);

        if (res.errno === "0") {
          // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
           message.showSuccess('短信验证码发送成功');
          let num = 60;
          // 设置一个计时器
          let t = setInterval(function () {
            if (num === 1) {
              // 如果计时器到最后, 清除计时器对象
              clearInterval(t);
              // 将点击获取验证码的按钮展示的文本恢复成原始文本
              $smsCodeBtn.html("获取验证码");
              send_flag = true;
            } else {
              num -= 1;
              // 展示倒计时信息
              $smsCodeBtn.html(num + "秒");
            }
          }, 1000);
        }
        else {
          message.showError(res.errmsg);
          send_flag = true;
        }
      })

      .fail(function(){
        message.showError('服务器超时，请重试！');
      });
      }

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





});