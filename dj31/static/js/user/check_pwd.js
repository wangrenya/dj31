$(function (){

          let $mobile   = $(' #mobile ');

// 标记
    let isUsernameReady = false,
        isPasswordReady = false,
        isMobileReady = false;





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
        if (res['count'] ===0) {
          message.showError('此手机号没有在本平台注册！')
        } else {
           message.showSuccess('此手机号可以正常修改密码')
                       isMobileReady = true;
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });


    }



  // 注册逻辑
    let $register = $('.form-contain');  // 获取注册表单元素

    $register.submit(function (e) {
    // 阻止默认提交操作
    e.preventDefault();



    let old_Password = $("input[name=old_password]").val();

    let new_Password = $("input[name=new_password]").val();
    let sMobile = $mobile.val();  // 获取用户输入的手机号码字符串


    // 判断手机号是否为空，是否已注册
    if (!isMobileReady) {
        fn_check_mobile();
      return
    }



    // 判断用户输入的密码是否为空
    if ((!old_Password) || (!new_Password)) {
      message.showError('密码或确认密码不能为空');
      return
    }

    // const reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[\x21-x7e]{6,18}$/
    // 以首字母开头，必须包含数字的6-18位
    // 判断用户输入的密码和确认密码长度是否为6-20位
      if (!(/^[0-9A-Za-z]{6,20}$/).test(new_Password)){
         message.showError('请输入6到20位密码');
          return
      }


    // 判断用户输入的密码和确认密码是否一致
    if (new_Password === old_Password) {
      message.showError('旧密码和新密码不能相同');
      return
    }




    // 发起修改请求
    // 1、创建请求参数
    let SdataParams = {

      "old_password": old_Password,
      "new_password": new_Password,
      "mobile": sMobile,

    };

    // 2、创建ajax请求
    $.ajax({
      // 请求地址
      url: "/user/check_pwd/",  // url尾部需要添加/
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
        if (res.errno === "0") {
          // 修改成功
          message.showSuccess('密码修改成功');
           setTimeout(() => {
            // 注册成功之后重定向到主页
            window.location.href = '/user/login/';
          }, 1500)
        } else {
          // 注册失败，打印错误信息
          message.showError(res.errmsg);

        }
      })
      .fail(function(){
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








});