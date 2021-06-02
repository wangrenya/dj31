
$(function () {
  var $course_data = $(".course-data");
  var sVideoUrl = $course_data.data('video-url');
  var sCoverUrl = $course_data.data('cover-url');

  var player = cyberplayer("course-video").setup({
    width: '100%',
    height: 650,
    file: sVideoUrl,
    image: sCoverUrl,
    autostart: false,
    stretching: "uniform",
    repeat: false,
    volume: 100,
    controls: true,
    ak: '412a628a1025456d83fdae14a459f076'
  });

});
