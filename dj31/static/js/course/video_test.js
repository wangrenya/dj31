 $(function() {

    varsdk = baidubce.sdk; //拿到客户端
    var VodClient = sdk.VodClient; //调用客户端

    var config = {
        endpoint: 'http://vod.bj.baidubce.com', //加载配置
        credentials: {
            ak: '<cebc542a2c474e56952030d4146aca8f>',
            sk: '<29e5b7f8097d421fa70f3ead8549f1d1>'
        }
    };

        var client = new VodClient(config);
          var $file=$('.up'); //拿到UP文件
          $file.change(function () {  //定义一个视频迁移文件
              var video_file = this.files[0]; //拿到视频文件
              console.log(video_file);
              console.log(1)
              var title='步兵测试';
              var desc='这是一个视频';
              var video_type=video_file.type;
              var data=new Blob([video_file],{type:video_type}); //这个是文件对象
              client.createMediaResource(title, desc, data)
    // Node.js中<data>可以为一个Stream、<pathToFile>；在浏览器中<data>为一个Blob对象
    .then(function (response) {
        // 上传完成
        console.log(response.body.mediaId);
        console.log(video_type);
        // http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.m3u8
        // http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.m3u8
        var ym ='kdrdxb00kexev9wg66j.exp.bcevod.com';
        var os =response.body.mediaId;
        var url='http://'+ym+'/'+os+'/'+os+'.m3u8';
        console.log(url)
    })
    .catch(function (error) {
        console.log(error);
        // 上传错误
//监听progress事件 获取上传进度
client.on('progress', function (evt) {
    console.log(evt);
    });

          });
});
});

