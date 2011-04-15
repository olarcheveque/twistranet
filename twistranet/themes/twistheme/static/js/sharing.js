// Share/Like js helpers

jq(function()
{
  jq(".i_like,.i_unlike,.toggle_like").click(function(e)
  {
    if (jq(e.target).is( "a" )) obj = jq(this).parent();
    else obj =this;
    e.preventDefault();
    var ID = jq(obj).attr("id").replace('toggle_like_','');
    jq.ajax({
      type: "GET",
      url: home_url + "share/like_toggle_by_id/" + ID,
      cache: false,
      success: function(data){
        jsondata = eval( "(" + data + ")" );
        if (jsondata.i_like) {
            jq(obj).addClass('i_unlike');
            jq(obj).removeClass('i_like');
        }
        else {
            jq(obj).addClass('i_like');
            jq(obj).removeClass('i_unlike');
        }
      }
    });
    return false;
  })
});
