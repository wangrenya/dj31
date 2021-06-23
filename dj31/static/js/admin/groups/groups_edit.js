$(function () {

    let $gBtn = $('#btn-pub-news');
    $gBtn.click(function () {

        //判断组名是否为空
        let sName = $('#news-title').val();
        // alert(sName)
        if(!sName){
            message.showError('组名不能为空！！');
            return
        }
        // 判断权限
        let sGroupPer = $('#group-permissions').val();
        if (!sGroupPer || sName===[]){
            message.showError('请选择你的权限');
            return
        }
        let groId = $(this).data('news-id');
        console.log(groId);

        let url = groId? '/admin/groups/' + groId + '/' : '/admin/groups/add/';

        let data = {
            'name':sName,
            'group_permission':sGroupPer
        };

        $.ajax({
            url: url,
            type:groId ? 'PUT' : 'POST',
            data:JSON.stringify(data),
            contentType:'application/json; charset=utf-8',
            dataType:'json',
        })
        // 回调
        .done(function (res) {
            if(res.errno==='0'){
                if (groId){
                    fAlert.alertNewsSuccessCallback('用户组更新成功',"跳转到用户首页",function () {

                        window.location.href = '/admin/groups/manage/'
                    });

                }         else {
                    fAlert.alertNewsSuccessCallback('用户组发布成功',"跳转到用户首页",function () {
                         console.log(res.message)
                        window.location.href = '/admin/groups/manage/'
                    });
                }
            }
        })
    })
});
